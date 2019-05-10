def count_diffs(table, x, n):
    length = len(table[0])
    middle = False
    for i in range(length):
        if table[0][i] > x:
            middle = True
            break
    if not middle and i == length - 1:
        res_table = [table[0][length - n - 1:], table[1][length - n - 1:]]
    elif not middle and i == 0:
        res_table = [table[0][:n + 1], table[1][:n + 1]]
    else:
        low = i - 1
        high = i
        res_table = [list(), list()]
        while len(res_table[0]) != n + 1:
            if low >= 0:
                res_table[0].insert(0, table[0][low])
                res_table[1].insert(0, table[1][low])
                low -= 1
            if high < length and len(res_table[0]) != n + 1:
                res_table[0].append(table[0][high])
                res_table[1].append(table[1][high])
                high += 1
    main_diffs = list()
    buff_diffs = res_table[1][:]
    count = n
    step = 1
    for i in range(n):
        for j in range(count):
            buff_diffs[j] = (buff_diffs[j] - buff_diffs[j + 1]) / \
                            (res_table[0][j] - res_table[0][j+step])
        count -= 1
        step += 1
        main_diffs.append(buff_diffs[0])
    res_table.append(main_diffs)
    return res_table


def interpolate(table, x, n):
    res_table = count_diffs(table, x, n)
    res = res_table[1][0]
    k = 1
    for i in range(len(res_table[2])):
        k *= x - res_table[0][i]
        res += res_table[2][i] * k
    return res
