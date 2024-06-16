import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 8820))
server_socket.listen()
print("Server is up and running")

(client_socket, client_address) = server_socket.accept()
print("client connected")
data = client_socket.recv(1024).decode()
while (data!="EXIT"):
    print("Client sent: " + data)
    reply = "Why " + data + "?"
    client_socket.send(reply.encode())

    data = client_socket.recv(1021).decode()

client_socket.close()
server_socket.close()