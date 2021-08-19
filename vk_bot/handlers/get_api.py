import vk

from vk_bot.utils import get_random_id
from .settings.keyboard_settings import VKKeyboards
from mybot.settings import (
    ACCESS_TOKEN,
    API_VERSION,
    GROUP_ID,
)


class VKApi:
    def __init__(self):
        self.session = vk.Session()
        self.api = vk.API(self.session, v=API_VERSION)
        self.token = ACCESS_TOKEN
        self.group_id = GROUP_ID
        self.default_keyboard = VKKeyboards.MAIN

    def send_message(self, user_id, message, keyboard=None, attachment=""):
        if keyboard is None:
            keyboard = self.default_keyboard

        self.api.messages.send(
            access_token=self.token,
            user_id=user_id,
            message=message,
            attachment=attachment,
            keyboard=keyboard,
            random_id=get_random_id()
        )

    def get_user_first_name(self, user_id):
        return self.api.users.get(
            access_token=self.token,
            user_id=user_id)[0]['first_name']

    def get_user_last_name(self, user_id):
        return self.api.users.get(
            access_token=self.token,
            user_id=user_id)[0]['last_name']
