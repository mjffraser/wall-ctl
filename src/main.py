import sys

from config.read_config import get_config
from checks.checks      import run_checks
from loop.loop          import main_loop

def main():
    args = len(sys.argv)
    debug = False
    if args > 1:
        if str(sys.argv[1]) == "-db" or str(sys.argv[1]) == "-debug":
            debug = True
    specs = get_config()

    run_checks(specs)
    main_loop(specs)
    


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
