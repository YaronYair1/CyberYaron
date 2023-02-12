import socket
import random


def checkValidMovment(txt, dot):
    if txt[dot] == " ":
        return 1
    elif txt[dot] == "X":
        return 2
    return 0


def generateNpcs(txt, letter):
    dot = int(random.uniform(1, len(txt) - 1))
    while txt[dot] != " " or txt[dot] == "T" or txt[dot] == "S" or txt[dot] == "X":
        dot = int(random.uniform(1, len(txt) - 1))
        # print("didnt make it")
    txt = txt[:dot] + letter + txt[dot + 1:]
    return txt


def generateCopMove(txt):
    while True:
        dot = int(random.uniform(1, 9))
        if dot == 1:
            dot = modified_text.find("C") + rowLength
        elif dot == 2:
            dot = modified_text.find("C") + rowLength + 1
        elif dot == 3:
            dot = modified_text.find("C") + rowLength + 2
        elif dot == 4:
            dot = modified_text.find("C") - 1
        elif dot == 5:
            dot = modified_text.find("C") + 1
        elif dot == 6:
            dot = modified_text.find("C") - rowLength - 2
        elif dot == 7:
            dot = modified_text.find("C") - rowLength - 1
        elif dot == 8:
            dot = modified_text.find("C") - rowLength
        if txt[dot] != "*":
            txt = txt.replace("C", " ",)
            txt = txt[:dot] + "C" + txt[dot + 1:]
            print(txt)
            return txt
        if txt[dot] == "T":
            print("game ended, cop capture the thives")
            sentToClient = "LOST"
            client_socket.send(sentToClient.encode())
            # Close the client socket
            client_socket.close()
            print(modified_text)
            txt = txt.replace("C", " ")

            txt = txt[:dot] + "C" + modified_text[dot + 1:]
            return txt


def readingBinFile():
    text = ""
    i = 0
    with open('icehockey.bin', 'rb') as file:
        # Read the contents of the file into memory
        # file_content = file.read()
        rowLength = file.read(1)
        rowLength = int.from_bytes(rowLength, 'big')
        # print("The length of the row is:", rowLength)
        byte = file.read(1)
        while byte:
            # print(byte)
            text += str(int.from_bytes(byte, 'big'))
            byte = file.read(1)
            i += 1
            if i == rowLength:
                text += "\n"
                i = 0
        file.close()
        return text, rowLength


if __name__ == '__main__':

    text, rowLength = readingBinFile()
    modified_text = text.replace("1", "*")
    modified_text = modified_text.replace("0", " ")

    modified_text = generateNpcs(modified_text, "T")
    modified_text = generateNpcs(modified_text, "X")
    modified_text = generateNpcs(modified_text, "C")

    # Create a TCP server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to a port
    server_socket.bind(("127.0.0.1", 8820))
    # Listen for incoming connections
    server_socket.listen(1)
    print("Server is up and running")
    while True:
        client_socket, client_address = server_socket.accept()
        while True:
            # Accept an incoming connection
            # Receive data from the client
            key = client_socket.recv(1024).decode()
            print("Client sent: " + key)
            if key == "STATUS":
                client_socket.send(modified_text.encode())
                print(modified_text)
            elif key == "NEAR":
                if modified_text[modified_text.find("C") + rowLength] == "T" or modified_text[
                    modified_text.find("C") + rowLength + 1] == "T" or modified_text[
                    modified_text.find("C") + rowLength - 1] == "T" or modified_text[
                    modified_text.find("C") - rowLength - 1] == "T" or modified_text[
                    modified_text.find("C") - rowLength] == "T" or modified_text[
                    modified_text.find("C") - rowLength + 1] == "T" or modified_text[
                    modified_text.find("C") - 1] == "T" or modified_text[modified_text.find("C") + 1] == "T":
                    sentToClient = "COP NEAR"
                    client_socket.send(sentToClient.encode())
                    print(sentToClient)
                elif modified_text[modified_text.find("T") + rowLength] == "X" or modified_text[
                    modified_text.find("T") + rowLength + 1] == "X" or modified_text[
                    modified_text.find("T") + rowLength - 1] == "X" or modified_text[
                    modified_text.find("T") - rowLength - 1] == "X" or modified_text[
                    modified_text.find("T") - rowLength] == "X" or modified_text[
                    modified_text.find("T") - rowLength + 1] == "X" or modified_text[
                    modified_text.find("T") - 1] == "X" or modified_text[modified_text.find("T") + 1] == "X":
                    entToClient = "COP NEAR"
                    client_socket.send(sentToClient.encode())
                    print(sentToClient)

            else:
                # cop moves random
                modified_text = generateCopMove(modified_text)
                if key == "UP":
                    print("UP")
                    dot = modified_text.find("T") - rowLength - 1
                elif key == "DOWN":
                    print("DOWN")
                    dot = modified_text.find("T") + rowLength + 1
                elif key == "LEFT":
                    print("LEFT")
                    dot = modified_text.find("T") - 1
                elif key == "RIGHT":
                    print("RIGHT")
                    dot = modified_text.find("T") + 1
                if checkValidMovment(modified_text, dot) == 1:
                        modified_text = modified_text.replace("T", " ")
                        modified_text = modified_text[:dot] + "T" + modified_text[dot + 1:]
                        # Send data back to the client
                        sentToClient = "OK"
                        client_socket.send(sentToClient.encode())
                elif checkValidMovment(modified_text, dot) == 2:
                    print("You Won The Game")
                    sentToClient = "WON"
                    client_socket.send(sentToClient.encode())
                    # Close the client socket
                    client_socket.close()

                else:
                    print("valid move")
                    sentToClient = "WALL"
                    client_socket.send(sentToClient.encode())
            # Print the entered text
            print("You entered:", key)
