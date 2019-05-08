import re


class Data:
    def __init__(self, t0, tw, m):
        self.t0 = t0
        self.tw = tw
        self.m = m


def check_float(text):
    match = re.fullmatch(r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)', text)
    return bool(match)


def check_int(text):
    match = re.fullmatch(r'[-+]?\d+', text)
    return bool(match)


def get_data():
    while True:
        t0 = input('\nВведите To:')
        if check_float(t0):
            t0 = float(t0)
            break
        else:
            print('\nНекорректный ввод')

    while True:
        tw = input('\nВведите Tw:')
        if check_float(tw):
            tw = float(tw)
            break
        else:
            print('\nНекорректный ввод')

    while True:
        m = input('\nВведите m:')
        if check_int(m):
            m = int(m)
            break
        else:
            print('\nНекорректный ввод')
    return Data(t0, tw, m)
