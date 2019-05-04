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

    while True:
        p_start = input('\nВведите Pнач:')
        if check_float(p_start):
            p_start = float(p_start)
            break
        else:
            print('\nНекорректный ввод')

    while True:
        t_start = input('\nВведите Tнач:')
        if check_float(t_start):
            t_start = float(t_start)
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
    for i in range(41):
        t = count_t(data, z)
        nt_array.append(count_nt(p, t))
        z += h
    return nt_array


def integral(p, data):
    h = 1 / 40
    nt_array = fill_nt(p, h, data)
    result = 0
    z = h
    i = 1
    while i < 40:
        result += 4.0 * nt_array[i] * z
        i += 1
        z += h
        if i < 40:
            result += 2.0 * nt_array[i] * z
        z += h
        i += 1
    result += nt_array[40]
    result *= (h / 3)
    return result


def func(coef, data, p):
    return coef - 2.0 * integral(p, data)


def find_p(data):
    coef = 7242 * (data.p_start / data.t_start)
    left = 3
    right = 25
    middle = (left + right) / 2
    f_left = func(coef, data, left)
    f_right = func(coef, data, right)
    f_middle = func(coef, data, middle)
    while abs(f_middle) > 10e-4:
        if f_left * f_middle < 0:
            right = middle
        elif f_right * f_middle < 0:
            left = middle
        else:
            break
        middle = (left + right) / 2
        f_left = func(coef, data, left)
        f_right = func(coef, data, right)
        f_middle = func(coef, data, middle)
    return middle
