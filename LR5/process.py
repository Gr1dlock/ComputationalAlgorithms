import interpolation
from math import exp, log

POINTS = 3
Q_TABLE = [[2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 18000, 20000,
            22000, 24000, 26000],
           [1, 1, 1, 1.0001, 1.0025, 1.0198, 1.0895, 1.2827, 1.6973, 2.4616,
            3.6552, 5.3749, 7.6838],
           [4, 4, 4.1598, 4.3006, 4.4392, 4.5661, 4.6817, 4.7923, 4.9099,
            5.0511, 5.2354, 5.4841, 5.8181],
           [5.5, 5.5, 5.5116, 5.9790, 6.4749, 6.9590, 7.4145, 7.8370, 8.2289,
            8.5970, 8.9509, 9.3018, 9.6621],
           [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11],
           [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]]
E_TABLE = [12.13, 20.98, 31.00, 45.00]
Z_TABLE = [0, 1, 2, 3, 4]
P_INIT = 0.5
T_INIT = 300
V_INIT = -1
X_INIT = [2, -1, -10, -25, -35]
ALPHA_INIT = 0
GAMMA_INIT = 0
COEF_ALPHA = 0.285 * 10e-11
COEF_K = 7242
POLYNOMIAL_DEGREE = 2
EPS = 10e-4


class Result:
    def __init__(self, v, x):
        self.x = [0 for i in range(5)]
        for i in range(5):
            self.x[i] = x[i]
        self.v = v

    def add_del(self, cur_del):
        for i in range(5):
            self.x[i] += cur_del[i + 1]
        self.v += cur_del[0]

    def count_nt(self):
        nt = 0
        for i in range(5):
            nt += exp(self.x[i])
        return nt


def check_finish(cur_del, res):
    flag = False
    for i in range(4):
        if abs(cur_del[i + 1] / res.x[i]) >= EPS:
            flag = True
    if abs(cur_del[0] / res.v) >= EPS:
        flag = True
    return flag


def func_gamma(gamma, res, T):
    cur_sum = exp(res.v) / (1 + 0.5 * gamma)
    for i in range(2, 6):
        cur_sum += ((exp(res.x[i - 1]) * Z_TABLE[i - 1] ** 2) /
                    (1 + Z_TABLE[i - 1] ** 2 * gamma * 0.5))
    coef = 5.87 * 10e10 / T**3
    return gamma ** 2 - coef * cur_sum


def count_gamma(res, T):
    left = 0
    right = 3
    middle = (left + right) / 2
    f_left = func_gamma(left, res, T)
    f_right = func_gamma(right, res, T)
    f_middle = func_gamma(middle, res, T)
    while abs(f_middle) > EPS:
        if f_left * f_middle < 0:
            right = middle
        elif f_right * f_middle < 0:
            left = middle
        else:
            break
        middle = (left + right) / 2
        f_left = func_gamma(left, res, T)
        f_right = func_gamma(right, res, T)
        f_middle = func_gamma(middle, res, T)
    return middle


def gauss(matrix, right_vector):
    length = len(matrix)
    result = [0 for i in range(6)]
    for i in range(length):
        matrix[i].append(right_vector[i])
    for k in range(length):
        max_elem = 0.0
        max_index = 0
        for i in range(k, length):
            if abs(matrix[i][k]) >= max_elem:
                max_elem = abs(matrix[i][k])
                max_index = i
        if max_index != k:
            for i in range(length + 1):
                matrix[k][i], matrix[max_index][i] = matrix[max_index][i], \
                                                     matrix[k][i]
        for i in range(k + 1, length):
            coef = -(matrix[i][k] / matrix[k][k])
            for j in range(k, length + 1):
                matrix[i][j] += coef * matrix[k][j]
    for i in range(length - 1, -1, -1):
        for j in range(length - 1, i, -1):
            matrix[i][length] -= result[j] * matrix[i][j]
        result[i] = matrix[i][length] / matrix[i][i]
    return result


def count_alpha(gamma, T):
    alpha = COEF_ALPHA * (gamma * T) ** 3
    return alpha


def count_right(x, v, K, alpha, coef):
    res_right = []
    for i in range(4):
        res_right.append(-(v + x[i + 1] - x[i] - log(K[i])))
    cur_right = -exp(v)
    for i in range(1, 5):
        cur_right += Z_TABLE[i] * exp(x[i])
    res_right.append(cur_right)
    cur_right = coef + exp(v) - alpha
    for i in range(5):
        cur_right += exp(x[i])
    res_right.append(cur_right)
    return res_right


def count_del_E(T, gamma):
    coef = 8.61 * 10e-5 * T
    gamma *= 0.5
    res_E = []
    for i in range(4):
        cur_E = coef * log(((1 + Z_TABLE[i + 1] ** 2 * gamma) * (1 + gamma)) /
                           (1 + Z_TABLE[i] ** 2 * gamma))
        res_E.append(cur_E)
    return res_E


def count_Q(T):
    res_Q = []
    for i in range(5):
        cur_Q = interpolation.interpolate([Q_TABLE[0], Q_TABLE[i + 1]], T,
                                          POLYNOMIAL_DEGREE)
        res_Q.append(cur_Q)
    return res_Q


def count_K(T, gamma):
    cur_K = []
    coef = 4.83 * 10e-3
    coef_E = -11603.0 / T
    coef_T = pow(T, 1.5)
    cur_Q = count_Q(T)
    del_E = count_del_E(T, gamma)
    for i in range(4):
        cur_K.append(coef * (cur_Q[i + 1] / cur_Q[i]) * coef_T *
                     exp((E_TABLE[i] - del_E[i]) * coef_E))

    return cur_K


def count_A(x, v):
    A = [[0 for i in range(6)] for j in range(6)]
    j = 1
    for i in range(4):
        A[i][0] = 1
        A[i][j] = -1
        A[i][j + 1] = 1
        j += 1
    A[4][0] = exp(v)
    for i in range(2, 6):
        A[4][i] = -Z_TABLE[i - 1] * exp(x[i - 1])
    A[5][0] = -exp(v)
    for i in range(1, 6):
        A[5][i] = -exp(x[i - 1])
    return A


def count_nt(T, p):
    cur_A = count_A(X_INIT, V_INIT)
    cur_K = count_K(T, GAMMA_INIT)
    coef = -COEF_K * p / T
    cur_right = count_right(X_INIT, V_INIT, cur_K, ALPHA_INIT, coef)
    res = Result(V_INIT, X_INIT)
    flag = True
    while flag:
        cur_del = gauss(cur_A, cur_right)
        res.add_del(cur_del)
        gamma = count_gamma(res, T)
        alpha = count_alpha(gamma, T)
        cur_K = count_K(T, gamma)
        cur_A = count_A(res.x, res.v)
        cur_right = count_right(res.x, res.v, cur_K, alpha, coef)
        if check_finish(cur_del, res):
            flag = False
    nt = res.count_nt()
    print("ne = ", exp(res.v), ", n2 = ", exp(res.x[1]))

    return nt


def count_t(data, z):
    return data.t0 + (data.tw - data.t0) * pow(z, data.m)


def fill_nt(p, h, data):
    z = 0
    nt_array = []
    for i in range(POINTS + 1):
        t = count_t(data, z)
        nt_array.append(count_nt(t, p))
        z += h
    return nt_array


def integral(p, data):
    h = 1 / POINTS
    nt_array = fill_nt(p, h, data)
    result = 0
    z = h
    i = 1
    while i < POINTS:
        result += 4.0 * nt_array[i] * z
        i += 1
        z += h
        if i < POINTS:
            result += 2.0 * nt_array[i] * z
        z += h
        i += 1
    result += nt_array[POINTS]
    result *= (h / 3)
    return result


def func(coef, data, p):
    return coef - 2.0 * integral(p, data)


def find_p(data):
    coef = 7242 * (P_INIT / T_INIT)
    left = -10
    right = 25
    middle = (left + right) / 2
    f_left = func(coef, data, left)
    f_right = func(coef, data, right)
    f_middle = func(coef, data, middle)
    while abs(f_middle) > EPS:
        if f_left * f_middle < 0:
            right = middle
        elif f_right * f_middle < 0:
            left = middle
        else:
            print("No root")
            break
        middle = (left + right) / 2
        f_left = func(coef, data, left)
        f_right = func(coef, data, right)
        f_middle = func(coef, data, middle)
    return middle
