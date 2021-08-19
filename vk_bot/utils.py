import random
import copy


def get_random_id():
    return random.getrandbits(64)


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def sum_dict_values(dict_):
    dict_copy = copy.deepcopy(dict_)
    res = list(dict_copy.values())[0]

    for i in list(dict_copy.values())[1:]:
        res += i

    return res


def upper_first(word):
    return word[0].upper() + word[1:]


def upper_first_in_list(word_list):
    return [upper_first(word) for word in word_list]
