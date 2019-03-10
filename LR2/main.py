import process
import os

if __name__ == '__main__':

    # process.autofill('in_2.txt')

    while True:
        filename = input('Введите название файла:')
        if os.path.exists(filename) and os.path.isfile(filename):
            break
        else:
            print('Указанный файл не существует, введите еще раз')

    args = list()
    values = list()
    file = open(filename, 'r')
    for line in file:
        x, y = line.split()
        if (not process.check_float(x)) or (not process.check_float(y)):
            print('Файл имеет некорректный формат')
            exit()
        args.append(float(x))
        values.append(float(y))
    file.close()
    table = [args, values]
    process.print_table(table)
    while True:
        x = input('\nВведите x:')
        if process.check_float(x):
            break
        else:
            print('\nНекорректный ввод')
    x = float(x)
    res = process.splines(table, x)
    if x > table[0][len(table[0]) - 1] or x < table[0][0]:
        print('Произошла экстраполяция')
    else:
        print('Результат равен', res)
