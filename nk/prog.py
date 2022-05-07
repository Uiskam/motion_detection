import sys


def main():
    if len(sys.argv) == 2:
        src = sys.argv[1]

    elif len(sys.argv) == 3:
        src = sys.argv[1]
        mask_sensitivity = sys.argv[2]

    elif len(sys.argv) == 4:
        src = sys.argv[1]
        mask_sensitivity = sys.argv[2]
        motion_sensitivity = sys.argv[3]

    elif len(sys.argv) == 4:
        src = sys.argv[1]
        mask_sensitivity = sys.argv[2]
        motion_sensitivity = sys.argv[3]
        debug = sys.argv[4]


if __name__ == "__main__":
    main()
