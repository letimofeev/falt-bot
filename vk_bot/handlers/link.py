import pandas as pd


class LessonLink:
    def __init__(self, path):
        self.df = pd.read_csv(path)

    def _lower_subj_names(self):
        subj_name_key = self.df.columns[0]
        return [subj.lower() for subj in self.df[subj_name_key]]

    def get_subj_list(self, lowercase=False):
        if lowercase:
            return self._lower_subj_names()

        name_key = self.df.columns[0]
        subj_list = self.df[name_key].tolist()

        return subj_list

    def get_subj_link(self, subj_name):
        subj_name = subj_name.lower()

        name_key = self.df.columns[0]
        link_key = self.df.columns[1]

        df = self.df.copy()
        df[name_key] = self._lower_subj_names()

        return df[df[name_key] == subj_name][link_key].iloc[0]
