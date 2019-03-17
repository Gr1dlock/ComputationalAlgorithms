import re


def check_float(text):
    match = re.fullmatch(r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)', text)
    return bool(match)


def check_int(text):
    match = re.fullmatch(r'[-+]?\d+', text)
    return bool(match)


def func(x, y):
    return x*x + y*y


def autofill(filename, nx, ny):
    file = open(filename, 'w')
    file.write(str(nx) + " " + str(ny) + "\n")
    for i in range(0, nx, 1):
        for j in range(0, ny, 1):
            file.write(str(i) + " " + str(j) + " " + str(func(i, j)) + "\n")
    file.close()


def print_table(x_table, y_table, table):
    print('{:^7}'.format('Y'), end='')
    for i in range(len(y_table)):
        print('{:>8.3f} '.format(y_table[i]), end='')
    print()
    print('{:^6}'.format('X'))
    for i in range(len(x_table)):
        print('{:<8.3f} '.format(x_table[i]), end='')
        for j in range(len(y_table)):
            print('{:^8.3f} '.format(table[i][j]), end='')
        print()


def count_points(table, value, n):
    length = len(table)
    middle = False
    for i in range(length):
        if table[i] > value:
            middle = True
            break
    if not middle and i == length - 1:
        start_point = length - n - 1
        end_point = length
    elif not middle and i == 0:
        start_point = 0
        end_point = n + 1
    else:
        start_point = i
        end_point = i
        while end_point - start_point != n + 1:
            if start_point > 0:
                start_point -= 1
            if end_point < length and end_point - start_point != n + 1:
                end_point += 1
    return start_point, end_point


def count_diffs(arg_table, val_table, n):
    main_diffs = list()
    buff_diffs = val_table[:]
    count = n
    step = 1
    for i in range(n):
        for j in range(count):
            buff_diffs[j] = (buff_diffs[j] - buff_diffs[j + 1]) / \
                            (arg_table[j] - arg_table[j+step])
        count -= 1
        step += 1
        main_diffs.append(buff_diffs[0])
    return main_diffs


def polynomial(arg_table, val_table, diffs_table, x):
    res = val_table[0]
    k = 1
    for i in range(len(diffs_table)):
        k *= x - arg_table[i]
        res += diffs_table[i] * k
    return res


def interp(x_table, y_table, z_table, x, nx, y, ny):
    x_start, x_end = count_points(x_table, x, nx)
    y_start, y_end = count_points(y_table, y, ny)
    res_table = list()
    for i in range(x_start, x_end):
        diffs_table = count_diffs(y_table[y_start:y_end],
                                  z_table[i][y_start:y_end], ny)
        #print(z_table[i][y_start:y_end])
        tmp_res = polynomial(y_table[y_start:y_end],
                             z_table[i][y_start:y_end],
                             diffs_table, y)
        res_table.append(tmp_res)
    diffs_table = count_diffs(x_table[x_start:x_end], res_table, nx)
    res = polynomial(x_table[x_start:x_end], res_table, diffs_table, x)
    return res


def input_point(point, n, length):
    while True:
        p = input('\nВведите ' + point + ': ')
        if check_float(p):
            break
        else:
            print('\nНекорректный ввод')
    p = float(p)
    while True:
        np = input('\nВведите степень полинома ' + n + ': ')
        if check_int(np):
            np = int(np)
            if np > length - 1:
                print('\nВ таблице недостаточно точек')
            elif np < 0:
                print('\nСтепень не может быть меньше 0')
            else:
                break
        else:
            print('\nНекорректный ввод')
    return p, np


