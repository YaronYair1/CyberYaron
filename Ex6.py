import random
import time
import threading


def calcPi(numberTrials):
    numberInside = 0
    for i in range(numberTrials):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        if x * x + y * y <= 1:
            numberInside += 1
    return 4 * numberInside / numberTrials

def thredsCalcPI(batch, stop_event):
    for i in range(batch):
        trials = 1000000
        count = 0
        for j in range(trials):
            x = random.uniform(0, 1)
            y = random.uniform(0, 1)
            if x*x + y*y <= 1:
                count += 1
        pi = 4 * count / trials
        if stop_event.is_set():
            break
        print("Real value of Pi: 3.14159265358979323846, Calculated value of Pi:", pi, "Number of attempts:", (i+1)*trials,"\n")
    print("Final result: Real value of Pi: 3.14159265358979323846, Calculated value of Pi:", pi, "Number of attempts:", (i+1)*trials, "\n")


def main():
    #Ex1
    numberBatches = int(input("Enter the number of loops: "))
    realPi = 3.141592653589
    numberTrials = 1000000
    for i in range(numberBatches):
        funcPi = calcPi(numberTrials)
        print(f"Real value of Pi: {realPi}, Calculated value of Pi: {funcPi}, Number of attempts:"
              f" {numberTrials * (i + 1)}")
        time.sleep(1)
    #Ex2
    batch = int(input("Enter the number of loops: "))
    stopEvent = threading.Event()
    calculationThread = threading.Thread(target=thredsCalcPI, args=(batch, stopEvent))
    calculationThread.start()

    while True:
        inputValue = input("Press any key to start/stop the calculation: \n")
        if inputValue:
            if stopEvent.is_set():
                stopEvent.clear()
                calculationThread = threading.Thread(target=thredsCalcPI, args=(batch, stopEvent))
                calculationThread.start()
            else:
                stopEvent.set()
                calculationThread.join()
                break


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
