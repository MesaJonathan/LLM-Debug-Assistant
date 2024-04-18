import socket
import threading
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time

class ClientConnection:
    def __init__(self, connection):
        self.conn = connection
        self.last_char = ' '  # Initial space for first token

    def send(self, data):
        self.conn.send(data)

    def recv(self, bufsize):
        return self.conn.recv(bufsize)

    def close(self):
        self.conn.close()

def generate_and_stream(model, tokenizer, text, client):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)

    input_ids = tokenizer.encode(f"### Human: {text} ### Assistant:", return_tensors="pt").to(device)
    model.eval()
    with torch.no_grad():
        for i in range(500):  # Limit to 500 tokens
            outputs = model(input_ids=input_ids)
            next_token_logits = outputs.logits[:, -1, :]
            next_token = torch.argmax(next_token_logits, dim=-1).unsqueeze(-1)
            input_ids = torch.cat([input_ids, next_token], dim=-1)

            # Decode the token to text
            generated_text = tokenizer.decode(next_token.squeeze(), clean_up_tokenization_spaces=True)

            # Ensure proper spacing before sending
            if not generated_text.startswith(' ') and not client.last_char.isspace():
                generated_text = ' ' + generated_text
            
            client.last_char = generated_text[-1]  # Store the last character to handle spacing in the next token

            # Send the generated token's text to the client
            client.send(generated_text.encode("utf-8"))
            time.sleep(0.05)  # Simulate typing speed

    # Mark the end of the response
    client.send("END".encode("utf-8"))

def client_thread(connection, addr, model, tokenizer):
    client = ClientConnection(connection)
    print(f"Accepted connection from {addr[0]}:{addr[1]}")
    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            request = data.decode("utf-8").strip()
            print(f"Received: '{request}' from {addr}")

            if request.lower() == "close":
                client.send("closed".encode("utf-8"))
                break

            generate_and_stream(model, tokenizer, request, client)

    except Exception as e:
        print(f"Error handling {addr}: {e}")
    finally:
        client.close()
        print(f"Closed connection with {addr}")

def run_server():
    server_ip = '127.0.0.1'
    server_port = 8000
    model_path = "PY007/TinyLlama-1.1B-Chat-v0.1"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print(f"Server listening on {server_ip}:{server_port}")

    try:
        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=client_thread, args=(conn, addr, model, tokenizer)).start()
    finally:
        server_socket.close()
        print("Server shutdown")

# Run the server
run_server()
