def f(x, a0=1, a1=2, a2=3):
    return a0 * x / (a1 + a2 * x)


def f_der(x, a0=1, a1=2, a2=3):
    return a0 * a1 / ((a1 + a2 * x) ** 2)


# ksi(x) = 1 / x
# eta(y) = 1 / y = (a1 + a2*x) / (a0*x) = a2/a0 + a1/a0 * 1/x = a + b*ksi
# eta'|y = 1 / (y * y)
# ksi'|x = 1 / (x * x)
# eta'|ksi = (a + b*ksi)' = b = a1/a0

def eta_ksi_der(a0=1, a1=2):
    return a1 / a0


def eta_y_der(y):
    return 1 / (y * y)


def ksi_x_der(x):
    return 1 / (x * x)


def fill_table(x_start, x_end, step):
    x_table = [i for i in range(x_start, x_end, step)]
    y_table = [f(i) for i in x_table]
    return x_table, y_table


def print_table(mes, table):
    print("{:15}".format(mes))
    for a in table:
        if a is None:
            print("{:^10} ".format("----"), end='')
        else:
            print("{:10.6f} ".format(a), end='')
    print("\n")


def left_side_form(y, h):
    y_len = len(y)
    result = [None] * y_len
    for i in range(1, y_len):
        result[i] = (y[i] - y[i - 1]) / h
    return result


def right_side_form(y, h):
    y_len = len(y)
    result = [None] * y_len
    for i in range(0, y_len - 1):
        result[i] = (y[i + 1] - y[i]) / h
    return result


def central_form(y, h):
    y_len = len(y)
    result = [None] * y_len
    for i in range(1, len(y) - 1):
        result[i] = (y[i + 1] - y[i - 1]) / (2 * h)
    return result


def calculate_bound_results(y, h):
    y_len = len(y)
    result = [None] * y_len
    result[0] = (-3 * y[0] + 4 * y[1] - y[2]) / (2 * h)
    result[y_len - 1] = (y[y_len - 3] - 4 * y[y_len - 2] + 3 * y[
        y_len - 1]) / (2 * h)
    return result


def runge_left_side(y, h):
    y_len = len(y)
    r = 2
    p = 1
    zn = r ** p - 1

    y_h = left_side_form(y, h)
    y_h[0] = (y[1] - y[0]) / h

    y_rh = [None] * y_len
    for i in range(2, y_len):
        y_rh[i] = (y[i] - y[i - 2]) / (r * h)
    for i in range(2):
        y_rh[i] = (y[i + 2] - y[i]) / (r * h)
    result = [None] * y_len
    for i in range(y_len):
        result[i] = y_h[i] + (y_h[i] - y_rh[i]) / zn
    return result


def align_variable(x, y):
    y_len = len(y)
    result = [0] * y_len
    for i in range(0, y_len):
        if x[i] == 0:
            result[i] = None
        else:
            result[i] = (ksi_x_der(x[i]) / eta_y_der(y[i])) * eta_ksi_der()
    return result


def real_der(x):
    return [f_der(i) for i in x]


if __name__ == "__main__":
    h = 1
    x, y = fill_table(1, 11, 1)
    print_table("x:", x)
    print_table("y:", y)
    print_table("real:", real_der(x))
    print_table("left side:", left_side_form(y, h))
    print_table("right side:", right_side_form(y, h))
    print_table("bounds:", calculate_bound_results(y, h))
    print_table("central:", central_form(y, h))
    print_table("Runge:", runge_left_side(y, h))
    print_table("Align variables:", align_variable(x, y))
