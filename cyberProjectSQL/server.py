import socket
import threading
import sqlite3
import datetime

# specify host and port
host = '127.0.0.1'
port = 55555
clients = []

# create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

# create a database connection
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# create the users table if it does not exist
cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')

# create the messages table if it does not exist
cursor.execute('CREATE TABLE IF NOT EXISTS messages (sender TEXT, receiver TEXT, message TEXT, timestamp TEXT)')

# commit changes and close connection
conn.commit()
conn.close()


# define a function to handle client connections
def handle_client(client_socket, client_address):
    print(f'New connection from {client_address}')

    # send a message to the client requesting the username and password
    client_socket.send('LOGIN'.encode('ascii'))

    # receive the username and password from the client
    username = client_socket.recv(1024).decode('ascii')
    password = client_socket.recv(1024).decode('ascii')

    # authenticate the user
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()

    # if the user is not authenticated, close the connection
    if user is None:
        print(f'Authentication failed for {client_address}')
        client_socket.send('FAIL'.encode('ascii'))
        client_socket.close()
        return

    # if the user is authenticated, send a success message and the message history
    print(f'{username} authenticated from {client_address}')
    client_socket.send('SUCCESS'.encode('ascii'))

    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages WHERE receiver=? ORDER BY timestamp ASC', (username,))
    messages = cursor.fetchall()
    conn.close()

    for message in messages:
        sender, receiver, message_text, timestamp = message
        client_socket.send(f'{sender}: {message_text}'.encode('ascii'))

    # start a loop to receive and broadcast messages
    while True:
        try:
            message = client_socket.recv(1024).decode('ascii')

            # if the message is "QUIT", close the connection and break the loop
            if message == 'QUIT':
                client_socket.close()
                break

            # otherwise, broadcast the message to all connected clients
            print(f'{username}: {message}')
            conn = sqlite3.connect('messages.db')
            cursor = conn.cursor()
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('INSERT INTO messages (sender, receiver, message, timestamp) VALUES (?, ?, ?, ?)',
                           (username, 'all', message, timestamp))
            conn.commit()
            conn.close()
            broadcast_message = f'{username}: {message}'
            for client in clients:
                if client != client_socket:
                    client.send(broadcast_message.encode('ascii'))
        except:
            # if an error occurs, close the connection and break the loop
            print(f'Connection closed for {client_address}')
            client_socket.close()
            break


# define a function to broadcast a message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)




def main():
    # listen for incoming connections
    server.listen()

    print(f'Server running on {host}:{port}')

    while True:
        # accept a new connection
        client, address = server.accept()
        print(f'New connection from {address}')

        # add the new client to the list
        clients.append(client)

        # create a new thread to handle the client
        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.start()


if __name__ == '__main__':
    main()
