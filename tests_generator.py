import os
import equation_generator as eg
import solver as slv
import multiprocessing
from configs import *
from Process import *


def make_folders(set_n):
    general_path = "tests"
    if not os.path.exists(general_path):
        os.makedirs(general_path)
    if not os.path.exists(os.path.join(general_path, f"set{set_n}", "tests")):
        os.makedirs(os.path.join(general_path, f"set{set_n}", "tests"))
    if not os.path.exists(os.path.join(general_path, f"set{set_n}", "answers")):
        os.makedirs(os.path.join(general_path, f"set{set_n}", "answers"))


def output_test(cfg, set_n, test_n, equation):
    with open(os.path.join("tests", f"set{set_n}", "tests", f"test{test_n}.test"), 'w') as ost:
        ost.write(f"{equation}\n")
        ost.write(f"{cfg['iters']}\n")
        ost.write(f"{cfg['t0']} {cfg['y0']}\n")
        ost.write(f"{cfg['tk']}")


def output_answer(set_n, test_n, answer):
    with open(os.path.join("tests", f"set{set_n}", "answers", f"test{test_n}.answer"), 'w') as ost:
        ost.write(f"{answer}\n")


def gen(cfg, set_n, test_n):
    equation = eg.gen(cfg["depth"])
    picard = slv.picard(cfg["iters"], equation.right_part(), cfg["t0"],
                        cfg["y0"])

    answer = float(picard.subs('t', cfg["tk"]).evalf())  # conversion exception
    if abs(answer) > cfg["max"]:
        raise Exception(f"Too big answer value, regenerating equation...")

    output_test(cfg, set_n, test_n, equation)
    output_answer(set_n, test_n, answer)

    print(f"{test_n + 1})")
    print(f"\tEquation: {equation}")
    print(f"\ty({cfg['t0']}) = {cfg['t0']}")
    print(f"\tIterations: {cfg['iters']}")
    print(f"\ty_{cfg['iters']} = {picard}")
    print(f"\ty_{cfg['iters']}({cfg['tk']}) = {answer}")


if __name__ == '__main__':
    print(f"Generating ({len(configs)}) sets of tests.")
    for set_n in range(len(configs)):
        print(f"\nTest set #{set_n + 1}")
        make_folders(set_n)
        test_n = 0
        while True:
            try:
                generation = Process(target=gen, args=(configs[set_n], set_n, test_n))
                generation.start()
                generation.join(timeout=configs[set_n]['timeout'])
                if generation.exception:
                    raise Exception(generation.exception[0])
                if generation.is_alive():
                    generation.terminate()
                    raise Exception("Too long generation, regenerating equation...")
            except Exception as e:
                print(e)
                continue
            test_n += 1
            if test_n == configs[set_n]["count"]:
                break
