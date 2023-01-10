import socket
import random
from flask import Flask, request


def checkWin(guess, target):
    bulls = 0
    cows = 0
    bulls, cows = checkCowsAndBulls(guess, target)
    if bulls == 4:
        return True
    return False


def checkCowsAndBulls(guess, target):
    bulls = 0
    cows = 0
    print(guess)
    for i, digit in enumerate(guess):
        if digit == target[i]:
            bulls += 1
        elif digit in target:
            cows += 1
    print('bulls', bulls, 'cows', cows)
    return bulls, cows


if __name__ == '__main__':
    bulls = 0
    cows = 0
    turnLeft = 10
    target = ''.join(str(random.randint(0, 9)) for _ in range(4))
    print(target)
    # Create a TCP server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to a port
    server_socket.bind(("127.0.0.1", 8820))
    # Listen for incoming connections
    server_socket.listen()
    print("Server is up and running")
    while True:
        client_socket, client_address = server_socket.accept()
        while turnLeft > 0:
            # Accept an incoming connection
            # Receive data from the client
            key = client_socket.recv(1024).decode()
            print("Client sent: " + key)
            if checkWin(key, target):
                sentToClient = "WON"
                print(sentToClient)
                client_socket.send(sentToClient.encode())
                # Close the client socket
                client_socket.close()
                break
            else:
                bulls, cows = checkCowsAndBulls(key, target)
                print(bulls, cows)
                # Send data back to the client
                sentToClient = ("Bulls: " + str(bulls) + " Cows: " + str(cows))
                client_socket.send(sentToClient.encode())
            # Print the entered text
            print("You entered:", key)
            turnLeft -= 1
            if turnLeft == 0:
                sentToClient = "LOST"
                print(sentToClient)
                client_socket.send(sentToClient.encode())
                # Close the client socket
                client_socket.close()
                break
