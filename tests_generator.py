import os
import numpy as np
import equation_generator as eg


def make_folders(config):
    if not os.path.exists(config["tests_path"]):
        os.makedirs(config["tests_path"])
    if not os.path.exists(config["answers_path"]):
        os.makedirs(config["answers_path"])


def output_test(cfg, test_n, equation):
    with open(os.path.join(cfg["tests_path"], f"test{test_n}.test"), 'w') as ost:
        ost.write(f"{equation}\n")
        ost.write(f"{cfg['t0']} {equation.y.subs('t', cfg['t0']).evalf()}")


def output_answer(cfg, test_n, equation):
    with open(os.path.join(cfg["answers_path"], f"test{test_n}.answer"), 'w') as ost:
        ost.write(f"y = {equation.y} \n")
        ost.write(f"{equation}\n")
        ost.write(f"{cfg['t0']} {equation.y.subs('t', cfg['t0']).evalf()}")


# Проверка вычислимости функции на диапазоне и соответствия ограничению на значения.
def valid_function(cfg, y):
    try:
        for t in np.linspace(cfg['t0'], cfg['tn'], cfg['points']):
            if float(y.subs('t', t)) > cfg['max_value']:
                return False
        return True
    except:
        return False


# Вернет уравнение, решение которого вычислимо на диапазоне.
def valid_equation(cfg):
    equation = eg.gen(cfg['depth'])
    while not valid_function(cfg, equation.y):
        equation = eg.gen(cfg['depth'])

    return equation


# В дальнейшем будет в отдельном файле.
test_configs = [
    {
        "count": 1,
        "depth": 2,
        "t0": 0,
        "tn": 20,
        "points": 101,
        "max_value": 10 ** 6,
        "tests_path": "tests",
        "answers_path": os.path.join("tests", "answers"),
    }
]

if __name__ == '__main__':
    for cfg in test_configs:
        make_folders(cfg)
        for test_n in range(0, cfg["count"]):
            equation = valid_equation(cfg)
            output_test(cfg, test_n, equation)
            output_answer(cfg, test_n, equation)
