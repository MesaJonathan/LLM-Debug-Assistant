import socket
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer, pipeline
from threading import Thread


# Initialize the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("bgsmagnuson/tiny-llama-stack-overflow")
model = AutoModelForCausalLM.from_pretrained("bgsmagnuson/tiny-llama-stack-overflow")

# Set up socket
host = 'localhost'
port = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
print("Listening for client...")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")

try:
    while True:
        # Receive prompt from client
        data = conn.recv(1024)
        if not data or data.decode('utf-8').lower() == 'exit':
            break
        
        question = data.decode('utf-8')

        # Setup generation and streaming
        question = f"<s>[INST] {question} [/INST]"
        streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, timeout=3)

        generator = pipeline("text-generation", model="bgsmagnuson/tiny-llama-stack-overflow")

        generation_kwargs = dict(text_inputs=question, streamer=streamer, max_length=20)
        thread = Thread(target=generator, kwargs=generation_kwargs)
        thread.start()

        # Stream the generated text to the client
        generated_text = ""
        for new_text in streamer:
            generated_text += new_text
            conn.sendall(generated_text.encode('utf-8'))

        conn.sendall("<END>".encode('utf-8'))

finally:
    conn.close()
    server_socket.close()
