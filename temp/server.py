__author__ = 'Tamir'
import socket
import select
import threading
import time


def send_waiting_messages():
    while True:
        if messages_to_send:
            for message in messages_to_send:
                client_socket, data = message
                for client in open_client_sockets:
                    if (client_socket is not client) and (client != server_socket):
                        client.send(data)
                        print data
                messages_to_send.remove(message)


if __name__ == "__main__":
    server_socket = socket.socket()
    server_socket.bind(("0.0.0.0", 69))
    server_socket.listen(5)
    open_client_sockets = []
    messages_to_send = []
    threading.Thread(target=send_waiting_messages).start()
    while True:
        rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, [])
        for current_socket in rlist:
            if current_socket is server_socket:
                (new_socket, address) = server_socket.accept()
                open_client_sockets.append(new_socket)
            else:
                data = current_socket.recv(1024)
                if data == "#quit#":
                    open_client_sockets.remove(current_socket)
                    print "Connection with client closed"
                else:
                    if data != "":
                        print data
                        temp_sock_msg = (current_socket, data)
                        messages_to_send.append(temp_sock_msg)



