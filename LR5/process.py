import re


class Data:
    def __init__(self, t0, tw, m, p_start, t_start):
        self.t0 = t0
        self.tw = tw
        self.m = m
        self.p_start = p_start
        self.t_start = t_start


def check_float(text):
    match = re.fullmatch(r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)', text)
    return bool(match)


def check_int(text):
    match = re.fullmatch(r'[-+]?\d+', text)
    return bool(match)


def get_data():
    while True:
        t0 = input('\nВведите To:')
        if check_int(t0):
            t0 = int(t0)
            break
        else:
            print('\nНекорректный ввод')

    while True:
        tw = input('\nВведите Tw:')
        if check_int(tw):
            tw = int(tw)
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

    while True:
        p_start = input('\nВведите Pнач:')
        if check_int(p_start):
            p_start = int(p_start)
            break
        else:
            print('\nНекорректный ввод')

    while True:
        t_start = input('\nВведите Tнач:')
        if check_int(t_start):
            t_start = int(t_start)
            break
        else:
            print('\nНекорректный ввод')
    return Data(t0, tw, m, p_start, t_start)


def count_t(data, z):
    return data.t0 + (data.tw - data.t0) * pow(z, data.m)


def count_nt(p, t):
    return (7242 * p) / t


def fill_nt(p, h, data):
    z = 0
    nt_array = []
    for i in range(40):
        t = count_t(data, z)
        nt_array.append(count_nt(p, t))
        z += h
    return nt_array


def integral()


