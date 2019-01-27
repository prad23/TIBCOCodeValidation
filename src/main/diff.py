import sys
import difflib


def main():
    if len(sys.argv) != 3:
        return

    with open(sys.argv[1]) as f1, open(sys.argv[2]) as f2:
        for diff in difflib.context_diff(f1.readlines(),
                                         f2.readlines(),
                                         fromfile=sys.argv[1],
                                         tofile=sys.argv[2]):
            sys.stdout.write(diff)


if __name__ == "__main__":
    main()