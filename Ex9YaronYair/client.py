import socket
import threading
import requests
import socket


def handle_udp_connection(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', port))

    while True:
        data, address = server_socket.recvfrom(1024)
        if data.decode() == 'Cyber Himmelfarb':
            server_socket.sendto(b'Victory!', address)
        else:
            server_socket.sendto(b'No Entry', address)


def run_udp_server(port):
    udp_thread = threading.Thread(target=handle_udp_connection, args=(port,))
    udp_thread.start()


def get_port_from_http_server():
    response = requests.get('http://localhost:5000/port')
    return int(response.headers['Port Number'])


def send_udp_message(port, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(message.encode(), ('0.0.0.0', port))
    return client_socket.recv(1024).decode()


if __name__ == '__main__':
    try:
        port = get_port_from_http_server()
        run_udp_server(port)
        response = send_udp_message(port, 'Cyber Himmelfarb')
        print(response)
    except requests.exceptions.RequestException as e:
        print('Error connecting to the HTTP server:', e)
    except socket.error as e:
        print('Error sending UDP message:', e)
