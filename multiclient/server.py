import socket
import select

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = "0.0.0.0"
def main():
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket who listen to new clients
    server_socket.bind((SERVER_IP, SERVER_PORT)) # bind to the port
    server_socket.listen() # wait for client connection
    print("Listening for clients...")
    client_sockets = [] # list of client sockets who connected
    message_to_send = []
    while True: # keep the server running
        read_list = client_sockets + [server_socket] # which sockets have a reason to read from them
        ready_to_read, ready_to_write, in_error = select.select(read_list, client_sockets, []) # select the sockets that are ready to read, write, and in error

        # read from sockets
        for current_socket in ready_to_read: # iterate over the sockets that are ready to read
            if current_socket is server_socket: # a new client is trying to connect to the server
                client_socket, client_address = current_socket.accept() # accept the new connection
                print("New client joined!", client_address) # print the address of the new client
                client_sockets.append(client_socket) # add the new client to the list of client sockets for future reference
                
            else: # if the current socket is a client socket, then a message is being sent
                data = current_socket.recv(MAX_MSG_LENGTH).decode() # receive the message
                if data == "": # if the message is empty, then the client has disconnected
                    print("Connection closed", ) 
                    client_sockets.remove(current_socket) # remove the client from the list of client sockets
                    current_socket.close() # close the connection
                else: # if the message is not empty, then print the message
                    print(data) # print the message
                    message_to_send.append(data)
        # write to every socket (note: only ones free to read...)
        for message in message_to_send:
            current_socket,data = message.split(" ")
            if current_socket in ready_to_write: # if the current socket is ready to write
                current_socket.send(message.encode())
                message_to_send.remove(message)
    server_socket.close() # close the server socket

if __name__ == "__main__":
    main()