import pandas as pd

from vk_bot.handlers.settings.schedule_settings import (
    DAY_SCHEDULE_TEMPLATE,
    SCHEDULE_ERROR_TEMPLATE,
    SCHEDULE_NO_PAIR_TEMPLATE,
    SCHEDULE_NO_PAIR,
    SCHEDULE_SEP,
)


class Schedule:
    def __init__(self, path, course):
        self.df = pd.ExcelFile(path).parse(str(course))
        self._set_no_pair()
        self.day_col = self.df.columns[0]
        self.time_col = self.df.columns[1]

    def _set_no_pair(self):
        self.df.fillna(SCHEDULE_NO_PAIR, inplace=True)

    def get_group_list(self):
        return self.df.keys()[2:].tolist()

    def get_day_schedule(self, group, day):
        df_day = self.df[self.df[self.day_col] == day]
        day_schedule = f"{day.title()}\n"

        for time, cell in zip(df_day[self.time_col], df_day[group]):
            cell_values = cell.split(SCHEDULE_SEP)

            if len(cell_values) == 5:
                day_schedule += DAY_SCHEDULE_TEMPLATE.format(
                    time, *cell_values)

            elif cell_values[0] == SCHEDULE_NO_PAIR:
                day_schedule += SCHEDULE_NO_PAIR_TEMPLATE.format(time)

            else:
                day_schedule += SCHEDULE_ERROR_TEMPLATE.format(time)

        return day_schedule
