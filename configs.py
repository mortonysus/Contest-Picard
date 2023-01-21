import sympy as smp
configs = [
    {
        "count": 2,
        "depth": 1,
        "t0": smp.pi,
        "y0": smp.Rational(1),
        "tk": smp.pi * 3,
        "iters": 5,
        "timeout": 10,
        "max" : 10 **6
    },
    {
        "count": 2,
        "depth": 1,
        "t0": smp.pi,
        "y0": smp.Rational(1),
        "tk": smp.pi * 3,
        "iters": 3,
        "timeout": 5,
        "max": 10 ** 6
    }
]