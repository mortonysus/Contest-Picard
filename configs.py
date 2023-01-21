import sympy as smp

configs = [
    {
        "count": 2,
        "depth": 2,
        "t0": smp.Rational(2),
        "y0": smp.Rational(5),
        "tk": smp.Rational(1),
        "iters": 3,
        "timeout": 10,
        "max": 10 ** 12
    },
    {
        "count": 2,
        "depth": 1,
        "t0": smp.pi,
        "y0": smp.Rational(1),
        "tk": smp.pi * 3,
        "iters": 3,
        "timeout": 5,
        "max": 10 ** 12
    }
]
