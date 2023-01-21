import sympy as smp


# ODE in format: y' = f(t)*y + g(t)
class Equation:
    def __init__(self, f, g):
        self.f = f
        self.g = g

    def right_part(self):
        return smp.simplify(self.f * smp.Symbol('y') + self.g)

    def __str__(self):
        return f"y' = {self.right_part()}"
