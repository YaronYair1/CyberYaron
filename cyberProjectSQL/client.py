import socket
import threading
import tkinter as tk
from tkinter import messagebox

# specify host and port
host = '127.0.0.1'
port = 55555

# create a socket object and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


# define a function to handle incoming messages from the server
def receive():
    while True:
        try:
            # receive a message from the server
            message = client.recv(1024).decode('ascii')

            # if the message is "LOGIN", prompt the user for their username and password
            if message == 'LOGIN':
                username = username_entry.get()
                password = password_entry.get()

                # send the username and password to the server
                client.send(username.encode('ascii'))
                client.send(password.encode('ascii'))

            # if the message is "FAIL", display an error message and close the connection
            elif message == 'FAIL':
                messagebox.showerror('Error', 'Invalid username or password.')
                client.close()
                break

            # if the message is "SUCCESS", enable the message entry field and display the message history
            elif message == 'SUCCESS':
                message_entry.config(state='normal')
                send_button.config(state='normal')
                username_entry.config(state='disabled')
                password_entry.config(state='disabled')

                # receive and display the message history
                while True:
                    history = client.recv(1024).decode('ascii')
                    if history == 'END':
                        break
                    messages_text.insert(tk.END, f'{history}\n')
                    messages_text.yview(tk.END)

            # otherwise, display the message in the chat window
            else:
                messages_text.insert(tk.END, f'{message}\n')
                messages_text.yview(tk.END)

        except:
            # if an error occurs, close the connection and break the loop
            client.close()
            break


# define a function to send messages to the server
def send():
    message = message_entry.get()
    if message != '':
        client.send(message.encode('ascii'))
        message_entry.delete(0, tk.END)


# create the main window and widgets
root = tk.Tk()
root.title('Chat App')
root.geometry('400x400')

messages_frame = tk.Frame(root)
messages_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

messages_text = tk.Text(messages_frame)
messages_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(messages_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

messages_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=messages_text.yview)

entry_frame = tk.Frame(root)
entry_frame.pack(side=tk.BOTTOM, fill=tk.X)

username_label = tk.Label(entry_frame, text='Username:')
username_label.pack(side=tk.LEFT, padx=5)

username_entry = tk.Entry(entry_frame)
username_entry.pack(side=tk.LEFT, padx=5)

password_label = tk.Label(entry_frame, text='Password:')
password_label.pack(side=tk.LEFT, padx=5)

password_entry = tk.Entry(entry_frame, show='*')
password_entry.pack(side=tk.LEFT, padx=5)

message_entry = tk.Entry(entry_frame)
message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

send_button = tk.Button(entry_frame, text='Send', command=send, state='disabled')
send_button.pack(side=tk.LEFT, padx=5)

message_entry.bind('<Return>', lambda e: send())

# start a thread to handle incoming messages from the server
receive_thread = threading.Thread(target=receive)
receive_thread.start()


# Press the green button in the gutter to run the script.
def main():
    root.mainloop()


if __name__ == '__main__':
    main()
