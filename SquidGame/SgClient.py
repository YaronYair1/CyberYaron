import socket
import re


def is4Digits(input_string):
    # Check if the input string is 4 digits long
    if len(input_string) != 4:
        return False
    if not re.fullmatch(r'\d{4}', input_string):
        return False
    return True


if __name__ == '__main__':
    data = ""
    # Create a TCP client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the server
    client_socket.connect(("127.0.0.1", 8820))

    while True:
        # Read input from the user
        key = input("Input 4 numbers: ")
        if not is4Digits(key):
            print("Error, put 4 numbers!!!")
        else:
            client_socket.send(str(key).encode())
            # Receive data from the server
            data = client_socket.recv(1024).decode()
            if data == "WON":
                print("You WON The Game\nThe Target Was: " + str(key))
                break
            elif data == "LOST":
                print("You LOST The Game")
                break
            # Print the received data
            print("The server sent:\n" + data)
