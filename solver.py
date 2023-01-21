import sympy as smp

debug = False


# Возвращает формулу для k-того приближения Пикара
# f_yt - f(y,t)
# y(t0) = y0
def picard(k, f_yt, t0, y0):
    t, a = smp.Symbol('t'), smp.Symbol('a')
    y = y0
    for k in range(1, k + 1):
        y = y0 + smp.integrate(f_yt.subs({t: a, 'y': y.subs(t, a)}), (a, t0, t))
        if debug:
            print(f"y{k} = {y}")
    return smp.simplify(y)


if __name__ == '__main__':
    #debug = True
    with open("picard.in", 'r') as ist:
        equation = ist.readline()
        k = int(ist.readline())
        t0, y0 = [smp.parsing.sympy_parser.parse_expr(i) for i in ist.readline().split()]
        tk = smp.parsing.sympy_parser.parse_expr(ist.readline())

        y_expr = equation.split('=')[1]
        y_expr = smp.parsing.sympy_parser.parse_expr(y_expr)

        if debug:
            print(f"Picard approximation of {equation}:")

        yk = picard(k, y_expr, t0, y0)
        with open("picard.out", 'w') as ost:
            answer = yk.subs('t', tk).evalf()
            ost.write('%.10f' % answer)