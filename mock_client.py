import socket

# Set up the client socket
host = 'localhost'
port = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

try:
    while True:
        # Send a prompt to the server
        question = input("Enter your question (type 'exit' to quit): ")
        if question.lower() == 'exit':
            client_socket.sendall(question.encode('utf-8'))
            break
        client_socket.sendall(question.encode('utf-8'))

        # Receive and print the streamed data
        response_complete = False
        while not response_complete:
            data = client_socket.recv(1024)  # Adjust buffer size as needed
            data_string = data.decode('utf-8')  # Convert bytes to string
            if '<END>' in data_string:
                print("Found '<END>' in the data.")
                response_complete = True
            else:
                print(data_string)
finally:
    client_socket.close()
