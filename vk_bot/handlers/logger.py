from vk_bot.models import (
    VKUser,
    VKMessage,
)


class VKUserLogger:
    @staticmethod
    def log_user(user_id, name, surname, date):
        VKUser.create_or_pass(
            id=user_id,
            name=name,
            surname=surname,
            date=date,
        )


class VKMessageLogger:
    @staticmethod
    def log_message(message_id, user, text, date):
        VKMessage.create(
            id=message_id,
            user=user,
            text=text,
            date=date,
        )

