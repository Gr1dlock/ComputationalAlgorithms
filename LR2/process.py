import re
import math


def check_float(text):
    match = re.fullmatch(r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)', text)
    return bool(match)


def func(x):
    return math.cos(x) - x


def autofill(filename):
    file = open(filename, 'w')
    for i in range(-10, 10, 1):
        file.write(str(i/10) + " " + str(func(i/10)) + "\n")
    file.close()


def print_table(table):
    print('\n', '{:^10}{:^10}'.format('x', 'y(x)'))
    for i in range(len(table[0])):
        print('{:^10.3f}{:^10.3f}'.format(table[0][i], table[1][i]))


def find_place(table, x):
    for i in range(len(table[0])):
        if table[0][i] > x:
            return i
    return len(table[0]) - 1


def splines(table, x):
    length = len(table[0])
    position = find_place(table, x)

    h = [0 for i in range(length)]
    A = [0 for i in range(length)]
    B = [0 for i in range(length)]
    D = [0 for i in range(length)]
    F = [0 for i in range(length)]
    a = [0 for i in range(length)]
    b = [0 for i in range(length)]
    c = [0 for i in range(length + 1)]
    d = [0 for i in range(length)]
    ksi = [0 for i in range(length + 1)]
    eta = [0 for i in range(length + 1)]

    for i in range(1, length):
        h[i] = table[0][i] - table[0][i - 1]

    for i in range(2, length):
        A[i] = h[i - 1]
        B[i] = -2 * (h[i - 1] + h[i])
        D[i] = h[i]
        F[i] = -3 * ((table[1][i] - table[1][i - 1]) / h[i] -
                     (table[1][i - 1] - table[1][i - 2]) / h[i - 1])

    for i in range(2, length):
        ksi[i + 1] = D[i] / (B[i] - A[i] * ksi[i])
        eta[i + 1] = (A[i] * eta[i] + F[i]) / (B[i] - A[i] * ksi[i])

    for i in range(length - 2, -1, -1):
        c[i] = ksi[i + 1] * c[i + 1] + eta[i + 1]
    for i in range(1, length):
        a[i] = table[1][i - 1]
        b[i] = (table[1][i] - table[1][i - 1]) / h[i] - h[i] / 3 * \
               (c[i + 1] + 2 * c[i])
        d[i] = (c[i + 1] - c[i]) / (3 * h[i])
    # print(table[0][position], a, b, c, d, sep='\n')
    res = (a[position] + b[position] * (x - table[0][position - 1]) +
           c[position] * ((x - table[0][position - 1]) ** 2) +
           d[position] * ((x - table[0][position - 1]) ** 3))
    return res

