from typing import NamedTuple

from vk_bot.handlers.link import LessonLink
from vk_bot.utils import (
    chunks,
    upper_first,
    upper_first_in_list,
)

from vk_bot.static_data import (
    COURSES,
    GROUPS,
    FilePath,
    TextToAnswer,
    DAYS,
)

from vk_bot.handlers.keyboard import (
    VKKeyboard,
    VKKeyboardColor,
)


# Keyboards

# Функция для шаблонного создания клавиатур с группами
def get_group_keyboard(course_num):
    return VKKeyboard(inline=True).create_json(
        labels=GROUPS[course_num],
        colors=VKKeyboardColor.GREEN,
        one_color=True
    )


# Функция для шаблонного создания клавиатур с предметами
def get_subject_keyboard(course_num):
    subj_list = LessonLink(
        FilePath.LINKS[course_num]).get_subj_list()
    colors = [VKKeyboardColor.BLUE] * len(subj_list)

    subj_colors = list(chunks(colors, 2))
    subj_chunked = list(chunks(subj_list, 2))

    labels = subj_chunked + [upper_first(TextToAnswer.RETURN_MENU)]
    colors = subj_colors + [VKKeyboardColor.RED]

    return VKKeyboard().create_json(
        labels=labels,
        colors=colors,
    )


class VKKeyboards(NamedTuple):

    # Pycharm выделяет как ошибку выражение со списковым включением внутри NamedTuple
    # При этом код запускается и работает правильно, я не знаю почему
    # GROUPS = [groups[i] for i in COURSES.keys()]
    GROUPS = {
        1: get_group_keyboard(1),
        2: get_group_keyboard(2),
        3: get_group_keyboard(3),
        4: get_group_keyboard(4),
    }

    # Стартовая клавиатура
    MAIN = VKKeyboard().create_json(
        labels=[
            "Расписание",
            "Ссылки на занятия",
            "Другие материалы",
            "Изменить данные",
        ],
        colors=[
            VKKeyboardColor.GREEN,
            VKKeyboardColor.GREEN,
            VKKeyboardColor.GREEN,
            VKKeyboardColor.BLUE,
        ]
    )

    # inline клавиатура со списком курсов
    COURSES = VKKeyboard(inline=True).create_json(
        labels=COURSES.keys(),
        colors=VKKeyboardColor.GREEN,
        one_color=True
    )

    # Словарь клавиатур со списком предметов
    # Ключ - номер курса, значение - клавиатура с предматами
    SUBJECTS = {
        1: get_subject_keyboard(1),
        2: get_subject_keyboard(2),
        3: get_subject_keyboard(3),
        4: get_subject_keyboard(4),
    }

    # клавиатура со списком дней недели
    DAYS = VKKeyboard().create_json(
        labels=upper_first_in_list(DAYS),
        colors=VKKeyboardColor.GREEN,
        one_color=True,
    )

    # inline клавиатура с кнопкой возврата в стартовое меню
    RETURN_MENU = VKKeyboard(inline=True).create_json(
        labels=[upper_first(TextToAnswer.RETURN_MENU)],
        colors=[VKKeyboardColor.RED],
    )

