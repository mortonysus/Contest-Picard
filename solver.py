import sympy as smp

debug = True

if __name__ == '__main__':
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

        t, a = smp.Symbol('t'), smp.Symbol('a')
        t0, y0 = [smp.Rational(i) for i in ist.readline().split()]

        y = y0
        for approximation_number in range(1, approx_count + 1):
            y = y0 + smp.integrate(y_expr.subs({t: a, 'y': y.subs(t, a)}), (a, t0, t))
            if debug:
                print(f"y{approximation_number} = {y}")
