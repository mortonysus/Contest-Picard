import sympy as smp


# ODE in format: y' = f(t)*h(y) + g(t)
class Equation:
    def __init__(self, y, ft, hy, gt):
        self.ft = ft
        self.gt = gt
        self.hy = hy
        self.y = y
        # Подставляем и проверяем что все сошлось.
        substitute = (self.ft * self.hy + self.gt).subs('y', y) - smp.diff(y, 't')
        if not substitute.equals(smp.sin(0)):
            raise Exception("bad generation")

    def __str__(self):
        y = smp.Symbol('y')
        return f"y' = {smp.simplify(self.ft * self.hy + self.gt)}"
