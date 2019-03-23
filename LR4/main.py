import process
import os

if __name__ == '__main__':

    # process.autofill('in_1.txt')

    while True:
        filename = input('Введите название файла:')
        if os.path.exists(filename) and os.path.isfile(filename):
            break
        else:
            print('Указанный файл не существует, введите еще раз')

    args = list()
    values = list()
    weight = list()
    file = open(filename, 'r')
    for line in file:
        x, y, p = line.split()
        if (not process.check_float(x)) or (not process.check_float(y) or (not process.check_float(p))):
            print('Файл имеет некорректный формат')
            exit()
        args.append(float(x))
        values.append(float(y))
        weight.append(float(p))
    file.close()
    table = [args, values, weight]
    process.print_table(table)
    while True:
        n = input('\nВведите степень полинома:')
        if process.check_int(n):
            n = int(n)
            if n < 0:
                print('\nСтепень не может быть меньше 0')
            else:
                break
        else:
            print('\nНекорректный ввод')
    process.approximate(table, n)
