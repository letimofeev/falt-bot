from datetime import datetime
import traceback

from django.http import HttpResponse

from mybot.settings import (
    VK_ADMIN_ID,
    VK_CONFIRMATION_CODE,
    SCHEDULE_ENABLED,
    LINKS_ENABLED,
)

from vk_bot.models import VKUser
from vk_bot.static_data import (
    TextAnswer,
    TextToAnswer,
    FilePath,
    COURSES,
    GROUPS,
    DAYS,
)

from .get_api import VKApi
from .link import LessonLink
from .schedule import Schedule
from .settings.keyboard_settings import VKKeyboards

from .logger import (
    VKMessageLogger,
    VKUserLogger,
)


class VKMessageHandler:
    def __init__(self):
        self.vk_api = VKApi()

    def handle(self, data):
        # если пришло новое сообщение
        if data['type'] == 'message_new':
            response = self.handle_new_message(
                data["object"]["message"])

        # если нужно подтверждение для вк
        elif data['type'] == 'confirmation':
            response = self.confirmation()

        # другие типы не поддерживаются
        else:
            response = HttpResponse(
                'ok',
                content_type="text/plain",
                status=400
            )

        return response

    def handle_new_message(self, message_object):
        # Считывание данных сообщения из тела запроса
        message_id = message_object["id"]
        user_id = message_object["from_id"]
        message_text = message_object["text"]
        date = datetime.fromtimestamp(int(message_object["date"]))

        # Логирование пользователя
        user_name = self.vk_api.get_user_first_name(user_id)
        user_surname = self.vk_api.get_user_last_name(user_id)
        VKUserLogger.log_user(user_id, user_name, user_surname, date)

        # Получение данных о пользователе в виде объекта
        user = VKUser.get_user(user_id)

        # Логирование полученного сообщения
        VKMessageLogger.log_message(message_id, user, message_text, date)

        # Получение списка ответов на сообщение
        answer_list = MessageResponder(
            VKKeyboards).get_answer(user, message_text)

        # Отправка ответов пользователю
        for answer_dict in answer_list:
            self.send_answer(user.id, answer_dict)

        return HttpResponse('ok', content_type="text/plain", status=200)

    def confirmation(self):
        return HttpResponse(
            VK_CONFIRMATION_CODE, content_type="text/plain", status=200)

    def send_answer(self, user_id, answer_dict):
        try:
            if answer_text := answer_dict.get("answer_text"):
                keyboard = answer_dict.get("keyboard")

                self.vk_api.send_message(
                    user_id=user_id,
                    message=answer_text,
                    keyboard=keyboard,
                )

        except Exception as err:
            error_report = TextAnswer.ERROR.format(
                self.vk_api.get_user_first_name(user_id),
                self.vk_api.get_user_last_name(user_id),
                user_id,
                err,
                traceback.format_exc(),
            )

            self.vk_api.send_message(
                user_id=VK_ADMIN_ID,
                message=error_report,
            )


class MessageResponder:
    def __init__(self, keyboards):
        self.keyboards = keyboards

    def get_answer(self, user, text):
        if answer_reg := self.registration(user, text):
            return answer_reg

        if answer_link := self.get_answer_links(user, text):
            return answer_link

        if answer_schedule := self.get_answer_schedule(user, text):
            return answer_schedule

        if answer_other := self.get_other_materials(user, text):
            return answer_other

        return [{"answer_text": "Шо?"}]

    def registration(self, user, text):
        if (not (user.course and user.group) or
            text.lower() == TextToAnswer.CHANGE_REG_INFO) \
                and user.status == VKUser.ANY:
            VKUser.update(user.id, status=VKUser.REG_COURSE)
            return [{"answer_text": TextAnswer.CHOOSE_COURSE,
                    "keyboard": self.keyboards.COURSES}]

        if user.status == VKUser.REG_COURSE:
            if text.lower() in COURSES.keys():
                course_num = COURSES[text.lower()]
                VKUser.update(user.id, course=course_num,
                              status=VKUser.REG_GROUP)
                return [{"answer_text": TextAnswer.CHOOSE_GROUP,
                        "keyboard": self.keyboards.GROUPS[course_num]}]

            return [{"answer_text": TextAnswer.CHOOSE_COURSE_TO_CONTINUE,
                    "keyboard": self.keyboards.COURSES}]

        if user.status == VKUser.REG_GROUP:
            if text.title() in GROUPS[user.course]:
                VKUser.update(user.id, group=text.title(),
                              status=VKUser.ANY)
                return [{"answer_text": TextAnswer.REG_END}]

            return [{"answer_text": TextAnswer.CHOOSE_GROUP_TO_CONTINUE,
                    "keyboard": self.keyboards.GROUPS[user.course]}]

        return []

    def get_answer_links(self, user, text):
        text = text.lower()

        if text == TextToAnswer.LINKS and user.status == VKUser.ANY:
            if not LINKS_ENABLED:
                return [{"answer_text": TextAnswer.LINKS_UNAVAILABLE}]

            VKUser.update(user.id, status=VKUser.LINK)
            return [{"answer_text": TextAnswer.CHOOSE_SUBJ,
                    "keyboard": self.keyboards.SUBJECTS[user.course]}]

        if user.status == VKUser.LINK:
            link_table = LessonLink(FilePath.LINKS[user.course])
            if text in link_table.get_subj_list(lowercase=True):
                subj_link = link_table.get_subj_link(text)
                return [{"answer_text": subj_link,
                        "keyboard": self.keyboards.SUBJECTS[user.course]}]

            if text.lower() == TextToAnswer.RETURN_MENU:
                VKUser.update(user.id, status=VKUser.ANY)
                return [{"answer_text": TextAnswer.MAIN_MENU}]

            return [{"answer_text": TextAnswer.CHOOSE_SUBJ,
                    "keyboard": self.keyboards.SUBJECTS[user.course]}]

        return []

    def get_answer_schedule(self, user, text):
        text = text.lower()

        if text == TextToAnswer.SCHEDULE and user.status == VKUser.ANY:
            if not SCHEDULE_ENABLED:
                return [{"answer_text": TextAnswer.SCHEDULE_UNAVAILABLE}]

            VKUser.update(user.id, status=VKUser.SCHEDULE)
            return [{"answer_text": TextAnswer.CHOOSE_DAY,
                    "keyboard": self.keyboards.DAYS}]

        if user.status == VKUser.SCHEDULE:
            if text in DAYS:
                schedule = Schedule(
                    path=FilePath.SCHEDULE,
                    course=user.course).get_day_schedule(user.group, text)
                return [{"answer_text": schedule,
                         "keyboard": self.keyboards.DAYS},
                        {"answer_text": TextAnswer.SCHEDULE_RETURN,
                         "keyboard": self.keyboards.RETURN_MENU}]

            if text == TextToAnswer.RETURN_MENU:
                VKUser.update(user.id, status=VKUser.ANY)
                return [{"answer_text": TextAnswer.MAIN_MENU}]

            return [{"answer_text": TextAnswer.CHOOSE_DAY,
                    "keyboard": self.keyboards.DAYS}]

        return []

    def get_other_materials(self, user, text):
        text = text.lower()

        if text == TextToAnswer.OTHER_MATERIALS and \
                user.status == VKUser.ANY:
            return [{"answer_text": TextAnswer.OTHER_MATERIALS}]

        return []
