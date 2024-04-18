import socket
import threading
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def generate_and_stream(model, input_ids, tokenizer, conn):
    chat_history_ids = input_ids
    model.eval()  # Make sure the model is in evaluation mode

    with torch.no_grad():  # Disable gradient calculation for generation
        for _ in range(200):  # Assuming a max length of 200 tokens
            outputs = model(chat_history_ids)
            next_token_logits = outputs.logits[:, -1, :]
            next_token = torch.argmax(next_token_logits, dim=-1).unsqueeze(-1)
            chat_history_ids = torch.cat([chat_history_ids, next_token], dim=1)

            # Decode and send the token
            next_token_str = tokenizer.decode(next_token[0], skip_special_tokens=True)
            if next_token_str == tokenizer.eos_token:
                conn.sendall("END".encode("utf-8"))  # Send a special end token to signify end of message
                break

            conn.sendall(next_token_str.encode("utf-8"))

def client_thread(conn, addr, model, tokenizer):
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

            input_ids = tokenizer.encode(request, return_tensors='pt')
            generate_and_stream(model, input_ids, tokenizer, conn)

    except Exception as e:
        print(f"Error handling {addr}: {e}")
    finally:
        conn.close()
        print(f"Closed connection with {addr}")

def run_server():
    server_ip = '127.0.0.1'
    server_port = 8000
    model_path = "CustomLLM"
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
