# import socket

# def run_client():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
#         server_ip = '127.0.0.1'
#         server_port = 8000
#         client.connect((server_ip, server_port))

#         while True:
#             msg = input("Enter message: ")
#             if msg.lower() == "exit":
#                 client.sendall("close".encode("utf-8"))
#                 break
#             client.sendall(msg.encode("utf-8"))
#             print("Awaiting response...")
#             while True:
#                 token = client.recv(1024).decode("utf-8")
#                 if token == "END":
#                     print("\nResponse complete.")
#                     break
#                 print(token, end='')

# run_client()

import socket

# Set up the client socket
host = 'localhost'
port = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Receive and print the streamed data
try:
    while True:
        data = client_socket.recv(1024)  # Adjust buffer size as needed
        if not data:
            break
        print(data.decode('utf-8'))
finally:
    client_socket.close()
