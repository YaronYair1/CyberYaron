
import time

if __name__ == '__main__':

    # Create a TCP client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the server
    client_socket.connect(("127.0.0.1", 8820))
    print("press 4 to go Left:\n"
          "press 2 to go Down:\n"
          "press 6 to go Right:\n"
          "press 8 to go Up:\n"
          "'S' to show status\n"
          "'N' to show cop or treasure next to you: ")

    while True:
        # Read input from the user
        key = input("Press: ")
        # Check if the user entered 'quit'
        if key.lower() == "s":
            client_socket.send("STATUS".encode())
            # Receive data from the server
        if key.lower() == "n":
            client_socket.send("NEAR".encode())
            # Receive data from the server
        elif key == "8":
            print("Up")
            client_socket.send("UP".encode())
        elif key == "2":
            print("client send: Down")
            client_socket.send("DOWN".encode())
        elif key == "4":
            print("Left")
            client_socket.send("LEFT".encode())
        elif key == "6":
            print("Right")
            client_socket.send("Right".encode())
        else:
            print("valid key")
        # Print the entered text
        # print("You entered:", key)

        data = client_socket.recv(1024).decode()
        if data == "WON":
            break
        # Print the received data
        print("The server sent:\n" + data)

