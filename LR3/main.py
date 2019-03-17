import process
import os

if __name__ == '__main__':

    process.autofill('in_1.txt', 5, 5)

    while True:
        filename = input('Введите название файла:')
        if os.path.exists(filename) and os.path.isfile(filename):
            break
        else:
            print('Указанный файл не существует, введите еще раз')
    file = open(filename, 'r')
    len_x, len_y = (file.readline()).split()
    if (not process.check_int(len_x)) or (not process.check_int(len_y)):
        print('Файл имеет некорректный формат')
        exit()
    len_x = int(len_x)
    len_y = int(len_y)
    X = list()
    Y = list()
    Z = list()
    for line in file:
        x, y, z = line.split()
        if (not process.check_float(x)) or (not process.check_float(y)) or \
                (not process.check_float(z)):
            print('Файл имеет некорректный формат')
            exit()
        if X.count(float(x)) == 0:
            X.append(float(x))
        if Y.count(float(y)) == 0:
            Y.append(float(y))
        Z.append(float(z))
    file.close()
    table = [Z[i*len_y:i*len_y+len_y] for i in range(len_x)]
    process.print_table(X, Y, table)
    x, nx = process.input_point('x', 'nx', len_x)
    y, ny = process.input_point('y', 'ny', len_y)
    if x < X[0] or x > X[len_x - 1] or y < Y[0]  or y > Y[len_y - 1]:
        print('Произошла экстраполяция')
    res = process.interp(X, Y, table, x, nx, y, ny)
    print('Результат равен', res)
