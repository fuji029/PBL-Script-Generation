import csv
from sys import argv


def to_txt(src, dst1, dst2):
    with open(src, "r") as f:
        csv_data = csv.reader(f)
        col1 = list()
        col2 = list()
        for row in csv_data:
            col1.append(row[0])
            col2.append(row[1])
        with open(dst1, "w") as f:
            for item in col1:
                f.write(item + "\n")
        with open(dst2, "w") as f:
            for item in col2:
                f.write(item + "\n")


def main():
    if (len(argv) < 4):
        print("Error")
        exit(1)

    src = argv[1]
    dst1 = argv[2]
    dst2 = argv[3]

    to_txt(src, dst1, dst2)


if __name__ == "__main__":
    main()
