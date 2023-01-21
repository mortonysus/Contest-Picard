import os
import shutil
from pathlib import Path
from colorama import init, Fore

if __name__ == '__main__':
    init(autoreset=True)

    sets_path = "tests"
    sets = os.listdir(sets_path)

    successful = 0
    failed = 0
    for set_n in range(len(sets)):
        print(f"Test set #{set_n + 1}")

        tests_path = os.path.join(sets_path, sets[set_n], "tests")
        tests = os.listdir(tests_path)

        answers_path = os.path.join(sets_path, sets[set_n], "answers")
        answers = os.listdir(answers_path)

        if len(tests) != len(answers):
            raise Exception("Tests number not equal Answers number.")

        for test_n in range(1, len(tests) + 1):
            print(f"Test #{test_n}:")

            test_path = os.path.join(tests_path, tests[test_n - 1])
            shutil.copy2(test_path, "picard.in")

            os.system("Python solver.py")

            path_real_answer = Path(os.path.join(answers_path, answers[test_n - 1]))
            path_answer = Path("picard.out")

            real_answer = float(path_real_answer.read_text())
            answer = float(path_answer.read_text())
            delta = abs(real_answer - answer)

            print(f"|{real_answer} - {answer}| = {delta}")
            if delta < 1e-8:
                print(Fore.GREEN + 'OK')
                successful += 1
            else:
                print(Fore.RED + 'FAILED')
                failed += 1
    if failed == 0:
        print(Fore.GREEN + f"All tests passed: {successful}/{successful}")
    else:
        print(Fore.RED + f"Not all tests passed: {successful}/{successful + failed}")

