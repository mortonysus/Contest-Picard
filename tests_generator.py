import os
from Process import *
import equation_generator as eg
import solver as slv
from configs import *


def make_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def make_folders(set_n):
    general_path = "tests"
    make_folder(general_path)
    make_folder(os.path.join(general_path, f"set{set_n}", "tests"))
    make_folder(os.path.join(general_path, f"set{set_n}", "answers"))


def output_test(cfg, set_n, test_n, equation):
    with open(os.path.join("tests", f"set{set_n}", "tests", f"test{test_n}.test"), 'w') as ost:
        ost.write(f"{equation}\n")
        ost.write(f"{cfg['iters']}\n")
        ost.write(f"{cfg['t0']} {cfg['y0']}\n")
        ost.write(f"{cfg['tk']}")


def output_answer(set_n, test_n, answer):
    with open(os.path.join("tests", f"set{set_n}", "answers", f"test{test_n}.answer"), 'w') as ost:
        ost.write('%.10f' % answer)


def gen_test(cfg, set_n, test_n):
    equation = eg.gen(cfg["depth"])
    picard = slv.picard(cfg["iters"], equation.right_part(), cfg["t0"],
                        cfg["y0"])

    answer = float(picard.subs('t', cfg["tk"]).evalf())  # conversion exception
    if abs(answer) > cfg["max"]:
        raise Exception(f"Too big answer value in equation {equation}, regenerating equation...")

    output_test(cfg, set_n, test_n, equation)
    output_answer(set_n, test_n, answer)

    print(f"{test_n})")
    print(f"\tEquation: {equation}")
    print(f"\ty({cfg['t0']}) = {cfg['t0']}")
    print(f"\tIterations: {cfg['iters']}")
    print(f"\ty_{cfg['iters']} = {picard}")
    print(f"\ty_{cfg['iters']}({cfg['tk']}) = {answer}")


def gen_test_wrapper(test_n, set_n):
    gen = Process(target=gen_test, args=(configs[set_n - 1], set_n, test_n))
    gen.start()
    gen.join(timeout=configs[set_n-1]['timeout'])
    if gen.exception:
        raise Exception(gen.exception[0])
    if gen.is_alive():
        gen.terminate()
        raise Exception("Too long generation, regenerating...")


def gen_set(set_n):
    make_folders(set_n)
    test_n = 1
    while test_n != configs[set_n - 1]["count"] + 1:
        try:
            gen_test_wrapper(test_n, set_n)
        except Exception as e:
            print(e)
            continue
        test_n += 1


if __name__ == '__main__':
    print(f"Generating ({len(configs)}) sets of tests.")
    for set_n in range(1, len(configs) + 1):
        print(f"\nTest set #{set_n}")
        gen_set(set_n)
