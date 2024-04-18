import socket
import threading
from transformers import pipeline

# Configure the pipeline with the model from Hugging Face
generator = pipeline("text-generation", model="bgsmagnuson/tiny-llama-stack-overflow")

def generate_and_stream(request, conn):
    generated_texts = generator(f"<s>[INST] {request} [/INST]", max_length=500)
    generated_text = generated_texts[0]["generated_text"]
    
    conn.sendall(generated_text.encode("utf-8"))
    conn.sendall("END".encode("utf-8"))  # Signal end of the message

def client_thread(conn, addr):
    print(f"Accepted connection from {addr[0]}:{addr[1]}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            request = data.decode("utf-8").strip()
            print(f"Received: '{request}' from {addr}")

            if request.lower() == "close":
                conn.sendall("closed".encode("utf-8"))
                break

            generate_and_stream(request, conn)

    except Exception as e:
        print(f"Error handling {addr}: {e}")
    finally:
        conn.close()
        print(f"Closed connection with {addr}")

def run_server():
    server_ip = '127.0.0.1'
    server_port = 8000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print(f"Server listening on {server_ip}:{server_port}")

    try:
        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=client_thread, args=(conn, addr)).start()
    finally:
        server_socket.close()
        print("Server shutdown")

# Run the server
run_server()
