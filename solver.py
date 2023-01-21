import sympy as smp

debug = False


# Возвращает формулу для n-того приближения Пикара
# f_yt - f(y,t)
# y(t0) = y0
def picard(n, f_yt, t0, y0):
    t, a = smp.Symbol('t'), smp.Symbol('a')
    y = y0
    for k in range(1, n + 1):
        y = y0 + smp.integrate(f_yt.subs({t: a, 'y': y.subs(t, a)}), (a, t0, t))
        if debug:
            print(f"y{k} = {y}")
    return smp.simplify(y)


if __name__ == '__main__':
    debug = True
    test_file_name = "tests/test0.test"
    with open(test_file_name, 'r') as ist:
        equation = ist.readline()
        derivative, y_expr = [i.strip() for i in equation.split('=')]
        order = derivative.count("'")
        y_expr = smp.parsing.sympy_parser.parse_expr(y_expr)
        approx_count = int(ist.readline())

        if debug:
            print(f"Equation {equation}")
            print(f"Picard approximation of {order} order equation:")
            print(f"Approximations count: {approx_count}")

        t0, y0 = [smp.parsing.sympy_parser.parse_expr(i) for i in ist.readline().split()]
        picard(approx_count, y_expr, t0, y0)
