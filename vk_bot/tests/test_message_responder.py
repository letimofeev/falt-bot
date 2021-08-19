from datetime import date

from django.test import TestCase
from vk_bot.handlers.message import MessageResponder
from vk_bot.models import VKUser
from ..handlers.settings.keyboard_settings import VKKeyboards


class MessageResponderTest(TestCase):

    def setUp(self):
        VKUser.create(
            id=1001,
            name='Anton',
            surname='Epihin',
            date=date(2020, 1, 1)
        )

        VKUser.create(
            id=1002,
            name='Mihail',
            surname='Osin',
            date=date(2020, 1, 1)
        )

        VKUser.create(
            id=1003,
            name='Alexandr',
            surname='Meh',
            course=4,
            group="Б03-864",
            date=date(2020, 2, 2)
        )

        VKUser.create(
            id=1004,
            name='Mem',
            surname='Timofeev',
            course=2,
            group="Б03-015",
            date=date(2020, 2, 2)
        )

    def test_registration(self):
        self.maxDiff = None

        m = MessageResponder(VKKeyboards)

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1001), "123"),
            [{"answer_text": "Для продолжения пройдите краткую регистрацию\nВыберите курс",
             "keyboard": VKKeyboards.COURSES}])

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1001), "1234"),
            [{"answer_text": "Для продолжения выберите курс",
             "keyboard": VKKeyboards.COURSES}])

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1002), "2 курс"),
            [{"answer_text": "Для продолжения пройдите краткую регистрацию\nВыберите курс",
             "keyboard": VKKeyboards.COURSES}])

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1001), "Абоба"),
            [{"answer_text": "Для продолжения выберите курс",
             "keyboard": VKKeyboards.COURSES}])

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1001), "4 Курс"),
            [{"answer_text": "Выберите группу",
             "keyboard": VKKeyboards.GROUPS[4]}])

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1002), "2 куРС"),
            [{"answer_text": "Выберите группу",
             "keyboard": VKKeyboards.GROUPS[2]}])

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1001), "2 курс"),
            [{"answer_text": "Для продолжения выберите группу",
             "keyboard": VKKeyboards.GROUPS[4]}])

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1001), "б03-111"),
            [{"answer_text": "Для продолжения выберите группу",
             "keyboard": VKKeyboards.GROUPS[4]}])

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1001), "б03-864"),
            [{"answer_text": 'Вы успешно прошли регистрацию. Для изменения данных введите "Изменить данные"'}])

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1002), "ИЗМЕНИТЬ данные"),
            [{"answer_text": "Для продолжения выберите группу",
             "keyboard": VKKeyboards.GROUPS[2]}])

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1002), "Б03-011"),
            [{"answer_text": 'Вы успешно прошли регистрацию. Для изменения данных введите "Изменить данные"'}])

        test_user1 = VKUser.get_user(user_id=1001)
        test_user2 = VKUser.get_user(user_id=1002)

        self.assertEqual(test_user1.status, VKUser.ANY)
        self.assertEqual(test_user2.status, VKUser.ANY)

        self.assertEqual(test_user1.course, 4)
        self.assertEqual(test_user2.course, 2)

        self.assertEqual(test_user1.group, 'Б03-864')
        self.assertEqual(test_user2.group, 'Б03-011')

    def test_registration_change_reg_info(self):
        self.maxDiff = None

        m = MessageResponder(VKKeyboards)

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1003), "изменить ДАННЫЕ"),
            [{"answer_text": "Для продолжения пройдите краткую регистрацию\nВыберите курс",
             "keyboard": VKKeyboards.COURSES}])

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1003), "ИЗМЕНИТЬ ДаНнЫе"),
            [{"answer_text": "Для продолжения выберите курс",
             "keyboard": VKKeyboards.COURSES}])

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1004), "изменить данные"),
            [{"answer_text": "Для продолжения пройдите краткую регистрацию\nВыберите курс",
             "keyboard": VKKeyboards.COURSES}])

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1003), ';" DROP TABLE VKUSERS --'),
            [{"answer_text": "Для продолжения выберите курс",
             "keyboard": VKKeyboards.COURSES}])

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1004), '3 КуРС'),
            [{"answer_text": "Выберите группу",
             "keyboard": VKKeyboards.GROUPS[3]}])

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1004), 'изменить данные'),
            [{"answer_text": "Для продолжения выберите группу",
             "keyboard": VKKeyboards.GROUPS[3]}])

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1003), '1 курс'),
            [{"answer_text": "Выберите группу",
             "keyboard": VKKeyboards.GROUPS[1]}])

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1004), "б03-914"),
            [{"answer_text": 'Вы успешно прошли регистрацию. Для изменения данных введите "Изменить данные"'}])

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1003), 'изменить данные'),
            [{"answer_text": "Для продолжения выберите группу",
             "keyboard": VKKeyboards.GROUPS[1]}])

        self.assertEqual(
            m.registration(VKUser.get_user(user_id=1003), "Б03-112"),
            [{"answer_text": 'Вы успешно прошли регистрацию. Для изменения данных введите "Изменить данные"'}])

        test_user1 = VKUser.get_user(user_id=1003)
        test_user2 = VKUser.get_user(user_id=1004)

        self.assertEqual(test_user1.status, VKUser.ANY)
        self.assertEqual(test_user2.status, VKUser.ANY)

        self.assertEqual(test_user1.course, 1)
        self.assertEqual(test_user2.course, 3)

        self.assertEqual(test_user1.group, 'Б03-112')
        self.assertEqual(test_user2.group, 'Б03-914')

    def test_answer_links(self):
        self.maxDiff = None

        m = MessageResponder(VKKeyboards)

        self.assertEqual(
            m.get_answer_links(VKUser.get_user(user_id=1003), "сСылки на Занятия"),
            [{"answer_text": "Выберите предмет",
             "keyboard": VKKeyboards.SUBJECTS[4]}])

        self.assertEqual(
            m.get_answer_links(VKUser.get_user(user_id=1003), "ПреДМЕТ1"),
            [{"answer_text": "Ссылка1",
             "keyboard": VKKeyboards.SUBJECTS[4]}])

        self.assertEqual(
            m.get_answer_links(VKUser.get_user(user_id=1003), "Абоба"),
            [{"answer_text": "Выберите предмет",
             "keyboard": VKKeyboards.SUBJECTS[4]}])

        self.assertEqual(
            m.get_answer_links(VKUser.get_user(user_id=1003), "ПРЕДМЕТ2"),
            [{"answer_text": "Ссылка2",
             "keyboard": VKKeyboards.SUBJECTS[4]}])

        self.assertEqual(
            m.get_answer_links(VKUser.get_user(user_id=1003), "Вернуться в меню"),
            [{"answer_text": "Главное меню"}])

        test_user = VKUser.get_user(user_id=1003)

        self.assertEqual(test_user.status, VKUser.ANY)
