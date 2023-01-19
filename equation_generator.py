import numpy as np
import equation as eq
import sympy as smp


# Возвращает true с переданной вероятностью [0:1].
def true_with_chance(chance):
    return np.random.choice([True, False], p=[chance, 1 - chance])


# Возвращает результат применения случайного бинарного оператора.
def rnd_op(a, b):
    return np.random.choice([a + b, a - b, a * b, a / b, a ** b])


# Возвращает случайную тригонометрическую функцию (как насчет гаверсинуса?).
def rnd_trig_func():
    return np.random.choice([smp.sin, smp.cos, smp.tan, smp.cot])


# Возвращает случайную алгебраическую функцию.
def rnd_func():
    return np.random.choice([rnd_trig_func(), smp.sqrt, smp.exp, smp.log, smp.cbrt])


# Генерирует выражение зависящее от t.
# depth - максимальная глубина рекурсии(размер выражения на выходе.
def rnd_expr(depth, sym):
    if depth <= 0:
        return sym
    # Выбираем:
    #   Добавить слагаемое / множитель
    #   Увеличить вложенность
    #   Добавить и увеличить
    #   Ничего не делать
    # Теоретически это даст возможность получить любые комбинации выражений с глубиной вложенности не больше заданной
    dive = true_with_chance(0.5)
    operator = true_with_chance(0.5)

    # Возможно это все достаточно неприлично.
    if dive and not operator:
        return (rnd_func())(rnd_expr(depth - 1, sym))
    if not dive and operator:
        return rnd_op((rnd_func())(sym), rnd_expr(depth - 1, sym))
    if dive and operator:
        return rnd_op((rnd_func())(rnd_expr(depth - 1, sym)), rnd_expr(depth - 1, sym))
    if not operator and not dive:
        return rnd_func()(sym)


# Составление уравнения по частному решению и переменным коэффициентам
def make_from_y(y, hy, gt):
    dy = smp.simplify(smp.diff(y))
    ft = smp.simplify((dy - gt) / hy.subs('y', y))
    return eq.Equation(y, ft, hy, gt)


# Генерация случайного дифференциального уравнения первого порядка
def gen(depth):
    y = smp.simplify(rnd_expr(depth, smp.Symbol('t')))
    hy = smp.simplify(rnd_expr(depth, smp.Symbol('y')))
    gt = smp.simplify(rnd_expr(depth, smp.Symbol('t')))
    return make_from_y(y, hy, gt)
