from datetime import date

from django.test import TestCase
from vk_bot.models import (
    VKUser,
    VKMessage,
)


class VKUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #  Настройка неизменных объектов, используемых всеми методами тестирования
        VKUser.create(
            id=1000,
            name='Nikita',
            surname='Suslaparov',
            course=2,
            group='Б03-015',
            date=date(2021, 6, 30)
        )

    def test_name(self):
        user = VKUser.get_user(user_id=1000)
        field_name = user.name
        self.assertEquals(field_name, 'Nikita')

    def test_date(self):
        user = VKUser.get_user(user_id=1000)
        field_name = user.date
        self.assertEquals(field_name, date(2021, 6, 30))

    def test_name_label(self):
        user = VKUser.get_user(user_id=1000)
        field_label = user._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        user = VKUser.get_user(user_id=1000)
        max_length = user._meta.get_field('name').max_length
        self.assertEquals(max_length, 64)

    def test_object_name_is_name_space_surname(self):
        user = VKUser.get_user(user_id=1000)
        expected_object_name = '{0} {1}'.format(user.name, user.surname)
        self.assertEquals(expected_object_name, str(user))


class VKMessageModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        VKUser.create(
            id=1000,
            name='Slava',
            surname='Komu',
            date=date(2021, 6, 30)
        )

        user = VKUser.get_user(1000)

        VKMessage.create(
            id=47,
            user=user,
            text='Hello World',
            date=date(2021, 1, 1)
        )

    def test_text(self):
        message = VKMessage.objects.get(id=47)
        field_text = message.text
        self.assertEquals(field_text, 'Hello World')

    def test_user_name(self):
        message = VKMessage.objects.get(id=47)
        field_user_name = message.user.name
        self.assertEquals(field_user_name, 'Slava')

    def test_user_label(self):
        message = VKMessage.objects.get(id=47)
        field_label = message._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')

    def test_message_max_length(self):
        message = VKMessage.objects.get(id=47)
        max_length = message._meta.get_field('text').max_length
        self.assertEquals(max_length, 4096)

    def test_object_name_is_id(self):
        message = VKMessage.objects.get(id=47)
        expected_object_name = '{0}'.format(message.id)
        self.assertEquals(expected_object_name, str(message))
