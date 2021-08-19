from typing import NamedTuple

from .handlers.schedule import Schedule


# File locations
class FilePath(NamedTuple):

    LINKS = {
        1: "vk_bot/static/1 курс.csv",
        2: "vk_bot/static/2 курс.csv",
        3: "vk_bot/static/3 курс.csv",
        4: "vk_bot/static/4 курс.csv",
    }

    SCHEDULE = "vk_bot/static/schedule_template.xlsx"


class TextAnswer(NamedTuple):

    MAIN_MENU = "Главное меню"

    # registration
    CHOOSE_COURSE = "Для продолжения пройдите краткую регистрацию\nВыберите курс"
    CHOOSE_COURSE_TO_CONTINUE = "Для продолжения выберите курс"
    CHOOSE_GROUP = "Выберите группу"
    CHOOSE_GROUP_TO_CONTINUE = "Для продолжения выберите группу"
    REG_END = 'Вы успешно прошли регистрацию. Для изменения данных введите "Изменить данные"'

    # get_answer_links
    CHOOSE_SUBJ = "Выберите предмет"
    LINKS_UNAVAILABLE = "Ссылки на занятия в данный момент недоступны"

    # get_answer_schedule
    CHOOSE_DAY = "Выберите день недели"
    SCHEDULE_RETURN = "Для выхода из расписания"
    SCHEDULE_UNAVAILABLE = "Расписание в данный момент недоступно"

    # get_other_materials
    OTHER_MATERIALS = "link"

    # error message
    ERROR = "Сообщение об ошибке\nПользователь:{} {}, {}\nОшибка: {}\nDetails:\n{}"


class TextToAnswer(NamedTuple):

    RETURN_MENU = "вернуться в меню"

    # registration
    CHANGE_REG_INFO = "изменить данные"

    # get_answer_links
    LINKS = "ссылки на занятия"

    # get_answer_schedule
    SCHEDULE = "расписание"

    # get_other_materials
    OTHER_MATERIALS = "другие материалы"


COURSES = {
    '1 курс': 1,
    '2 курс': 2,
    '3 курс': 3,
    '4 курс': 4,
}

GROUPS = {
    1: Schedule(FilePath.SCHEDULE, 1).get_group_list(),
    2: Schedule(FilePath.SCHEDULE, 2).get_group_list(),
    3: Schedule(FilePath.SCHEDULE, 3).get_group_list(),
    4: Schedule(FilePath.SCHEDULE, 4).get_group_list(),
}

DAYS = [
    "понедельник",
    "вторник",
    "среда",
    "четверг",
    "пятница",
    "суббота",
]








