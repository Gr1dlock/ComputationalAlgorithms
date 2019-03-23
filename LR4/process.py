import re
import matplotlib.pyplot as plt
import numpy as np

def check_float(text):
    match = re.fullmatch(r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)', text)
    return bool(match)


def check_int(text):
    match = re.fullmatch(r'[-+]?\d+', text)
    return bool(match)


def func(x, k):
    return x ** k


def autofill(filename):
    file = open(filename, 'w')
    for i in range(-3, 3, 1):
        file.write(str(i) + " " + str(func(i, 3)) + " 1" + "\n")
    file.close()


def print_table(table):
    print('\n', '{:^10}{:^10}{:^10}'.format('x', 'y', 'p'))
    for i in range(len(table[0])):
        print('{:^10.3f}{:^10.3f}{:^10.3f}'.format(table[0][i], table[1][i], table[2][i]))


def get_matrix(table, n):
    length = len(table[0])
    matrix = [[0 for i in range(0, n + 1)] for j in range (0, n + 1)]
    col = [0 for i in range(0, n + 1)]

    for m in range(0, n + 1):
        for i in range(0, length):
            tmp = table[2][i] * func(table[0][i], m)
            for k in range(0, n + 1):
                matrix[m][k] += tmp * func(table[0][i], k)
            col[m] += tmp * table[1][i]
    return matrix, col


def gauss(matrix):
    print(matrix)
    length = len(matrix)
    for k in range(length):
        for i in range(k + 1, length):
            coef = -(matrix[i][k] / matrix[k][k])
            for j in range(k, length + 1):
                matrix[i][j] += coef * matrix[k][j]
    a = [0 for i in range(length)]
    print(matrix)
    for i in range(length - 1, -1, -1):
        for j in range(length - 1, i, -1):
            matrix[i][length] -= a[j] * matrix[i][j]
        a[i] = matrix[i][length] / matrix[i][i]
    return a


def print_result(table, a, n):
    dx = 10
    if len(table[0]) > 1:
        dx = (table[0][1] - table[0][0])

    # построение аппроксимирующей функции
    x = np.linspace(table[0][0] - dx, table[0][-1] + dx, 100)
    y = []
    for i in x:
        tmp = 0;
        for j in range(0, n + 1):
            tmp += func(i, j) * a[j]
        y.append(tmp)

    plt.plot(x, y)

    plt.plot(table[0], table[1], 'kD')
    plt.grid(True)
    miny = min(min(y), min(table[1]))
    maxy = max(max(y), max(table[1]))
    dy = (maxy - miny) * 0.03
    plt.axis([table[0][0] - dx, table[0][-1] + dx, miny - dy, maxy + dy])
    plt.show()


def approximate(table, n):
    matrix, col = get_matrix(table, n)
    for i in range(n + 1):
        matrix[i].append(col[i])
    a = gauss(matrix)
    print_result(table, a, n)
