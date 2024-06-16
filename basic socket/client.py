import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Ip, Tcp
my_socket.connect(('127.0.0.1', 8820)) #get ip taple, port
print("Connected\n")

message = input()
while (message != "EXIT"):
    my_socket.send(message.encode()) #send bytestring
    data = my_socket.recv(1024).decode()
    print(data)

    message = input()
my_socket.close()
