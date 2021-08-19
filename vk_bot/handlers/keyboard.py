from typing import NamedTuple
import json

from mybot.settings import (
    MAX_BUTTONS_ON_LINE,
    MAX_INLINE_LINES,
    MAX_DEFAULT_LINES,
)


class VKKeyboardColor(NamedTuple):
    GREEN = 'positive'
    RED = 'negative'
    BLUE = 'primary'
    WHITE = 'secondary'


class VKKeyboard:

    __slots__ = ('one_time', 'lines', 'keyboard', 'inline')

    def __init__(self, one_time=False, inline=False):
        self.one_time = one_time
        self.inline = inline
        self.lines = [[]]

        self.keyboard = {
            'one_time': self.one_time,
            'inline': self.inline,
            'buttons': self.lines
        }

    def add_button(self, label, color=VKKeyboardColor.WHITE):
        current_line = self.lines[-1]

        if len(current_line) > MAX_BUTTONS_ON_LINE:
            raise ValueError(f'Max {MAX_BUTTONS_ON_LINE} buttons on a line')

        button_type = 'text'

        current_line.append({
            'color': color,
            'action': {
                'type': button_type,
                'label': label,
            }
        })

    def add_line(self):
        if self.inline:
            if len(self.lines) > MAX_INLINE_LINES:
                raise ValueError(f'Max {MAX_INLINE_LINES} lines for inline keyboard')
        else:
            if len(self.lines) > MAX_DEFAULT_LINES:
                raise ValueError(f'Max {MAX_DEFAULT_LINES} lines for default keyboard')

        self.lines.append([])

    def create(self, labels, colors, one_color=False):
        if one_color:
            colors = [colors] * len(labels)
        for label, color in zip(labels, colors):
            if type(label) == str:
                print(label, color)
                self.add_button(label, color)
            else:
                if one_color:
                    color = [color] * len(label)
                [self.add_button(i, j) for i, j in zip(label, color)]
            self.add_line()
        self.lines.pop(-1)

        return self.keyboard

    def create_json(self, labels, colors, one_color=False):
        self.create(labels, colors, one_color)
        return self.to_json()

    def to_json(self):
        return json.dumps(self.keyboard)

    def json_to_keyboard(self):
        return self.to_json()

