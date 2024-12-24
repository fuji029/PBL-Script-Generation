from sys import argv


def clean(path_src, path_dst):
    with open(path_src, "r") as f:
        lines = f.read().rstrip().split("\n")
    with open(path_dst, "w") as f:
        for line in lines:
            if ("→" in line):
                line = line.split("→")[1]
            if ("(" in line):
                line = line.split("(")[0]
            if ("（" in line):
                line = line.split("（")[0]
            f.write(line + "\n")


def main():
    path_src = argv[1]
    path_dst = argv[2]

    clean(path_src, path_dst)


if __name__ == '__main__':
    main()
