import socket

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        server_ip = '127.0.0.1'
        server_port = 8000
        client.connect((server_ip, server_port))

        while True:
            msg = input("Enter message: ")
            if msg.lower() == "exit":
                client.sendall("close".encode("utf-8"))
                break
            client.sendall(msg.encode("utf-8"))
            print("Awaiting response...")
            while True:
                token = client.recv(1024).decode("utf-8")
                if token == "END":
                    print("\nResponse complete.")
                    break
                print(token, end='')

run_client()
