import random
import time


def create_files(numberOfFiles, amountOfNumber):
    for i in range(numberOfFiles):
        with open("file_{}.txt".format(i), "w") as file:
            for j in range(amountOfNumber):
                file.write(str(random.randint(1, 1000)) + "\n")


def read_files(numberOfFiles, mode):
    total = 0
    lastNumber = 0
    firstNumber = 0
    count = 0
    for i in range(numberOfFiles):
        with open("file_{}.txt".format(i), "r") as file:
            if mode == 1:
                for line in file:
                    last_digit = int(line)
                    lastNumber += int(repr(last_digit)[-1])
                    firstNumber += int(line[0])
                    count += 1
            else:
                for line in file:
                    total += int(line)
                    count += 1
    print("last numbers average :", lastNumber / count)
    print("first numbers average :", firstNumber / count)
    return total / count


def main():
    start = time.time()

    """
    # Ex1 A - C
    create_files(10, 100000)# use this when you make the files
    end = time.time()
    print("Time taken:", end - start, "seconds, time of opening files\n")
    start = time.time()
    average = read_files(10, 0)
    end = time.time()
    print("The average of all the numbers is:", average)
    print("Time taken:", end - start, "seconds, time calc average \n")
    """

    """
    # Ex1 D
    create_files(100, 10000)# use this when you make the files
    end = time.time()
    print("Time taken:", end - start, "seconds, time of opening files\n")
    start = time.time()
    average = read_files(100, 0)
    end = time.time()
    print("The average of all the numbers is:", average)
    print("Time taken:", end - start, "seconds, time calc average \n")
    """

    """
    Ex2 A - C
    create_files(1, 100000)
    end = time.time()
    print("Time taken:", end - start, "seconds, time of opening files\n")
    start = time.time()
    average = read_files(1, 1)
    end = time.time()
    print("Time taken:", end - start, "seconds, time calc average \n")
    """

    """
    Ex4
    """

if __name__ == '__main__':
    main()
