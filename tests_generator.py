import os
import numpy as np
import equation_generator as eg
import sympy as smp
import solver as slv
import multiprocessing


def make_folders(config):
    if not os.path.exists(config["tests_path"]):
        os.makedirs(config["tests_path"])
    if not os.path.exists(config["answers_path"]):
        os.makedirs(config["answers_path"])


def output_test(cfg, test_n, equation):
    with open(os.path.join(cfg["tests_path"], f"test{test_n}.test"), 'w') as ost:
        ost.write(f"{equation}\n")
        ost.write(f"{cfg['iters']}\n")
        ost.write(f"{cfg['t0']} {cfg['y0']}\n")
        ost.write(f"{cfg['tk']}")


def output_answer(cfg, test_n, answer):
    with open(os.path.join(cfg["answers_path"], f"test{test_n}.answer"), 'w') as ost:
        ost.write(f"{answer}\n")


configs = [
    {
        "count": 2,
        "depth": 2,
        "t0": smp.pi,
        "y0": smp.Rational(1),
        "tk": smp.pi * 3,
        "iters": 5,
        "tests_path": "tests",
        "answers_path": os.path.join("tests", "answers"),
        "timeout": 5
    },
    {
        "count": 2,
        "depth": 1,
        "t0": smp.pi,
        "y0": smp.Rational(1),
        "tk": smp.pi * 3,
        "iters": 3,
        "tests_path": "tests",
        "answers_path": os.path.join("tests", "answers"),
        "timeout": 3
    }
]


def gen(cfg, test_n):
    equation = eg.gen(cfg["depth"])
    picard = slv.picard(cfg["iters"], equation.right_part(), cfg["t0"],
                        cfg["y0"])

    answer = picard.subs('t', cfg["tk"]).evalf()
    output_test(cfg, test_n, equation)
    output_answer(cfg, test_n, answer)

    print(f"{test_n + 1})")
    print(f"\tEquation: {equation}")
    print(f"\ty({cfg['t0']}) = {cfg['t0']}")
    print(f"\tIterations: {cfg['iters']}")
    print(f"\ty_{cfg['iters']} = {picard}")
    print(f"\ty_{cfg['iters']}({cfg['tk']}) = {answer}")


if __name__ == '__main__':
    print(f"Generating ({len(configs)}) sets of tests.")
    for cfg in range(len(configs)):
        print(f"\nTest set #{cfg + 1}")
        make_folders(configs[cfg])
        k = 0
        while True:
            p = multiprocessing.Process(target=gen, args=(configs[cfg], k))
            p.start()
            p.join(timeout=configs[cfg]['timeout'])
            if p.is_alive():
                print("Too long generation, regenerating equation...")
                p.terminate()
                continue
            k += 1
            if k == configs[cfg]["count"]:
                break
