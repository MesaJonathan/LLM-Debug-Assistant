# import socket
# from threading import Thread
# from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer, pipeline
# import queue


# model_name = "bgsmagnuson/tiny-llama-stack-overflow"

# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)
# streamer = TextIteratorStreamer(tokenizer, skip_prompt=True)

# generator = pipeline("text-generation", model=model_name)

# def generate_and_stream(request, output_queue):
#     # generated_texts = generator(f"<s>[INST] {request} [/INST]", streamer=streamer, max_length=200)
#     # generated_text = generated_texts[0]["generated_text"]
#     # https://huggingface.co/docs/transformers/main/en/internal/generation_utils#transformers.TextStreamer
    
#     inputs = tokenizer(["An increasing sequence: one,"], return_tensors="pt")

#     generation_kwargs = dict(inputs, streamer=streamer, max_new_tokens=20)
#     thread = Thread(target=model.generate, kwargs=generation_kwargs)
#     thread.start()
#     for new_text in streamer:
#         output_queue.put(new_text)
    
#     output_queue.put("END")  

# def client_thread(conn, addr, output_queue):
#     print(f"Accepted connection from {addr[0]}:{addr[1]}")
#     try:
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             request = data.decode("utf-8").strip()
#             print(f"Received: '{request}' from {addr}")

#             if request.lower() == "close":
#                 conn.sendall("closed".encode("utf-8"))
#                 break

#             # Start the generation thread
#             Thread(target=generate_and_stream, args=(request, output_queue)).start()

#             # Send data as it becomes available in the queue
#             while True:
#                 message = output_queue.get()
#                 if message == "END":
#                     conn.sendall("END".encode("utf-8"))
#                     break
#                 conn.sendall(message.encode("utf-8"))

#     except Exception as e:
#         print(f"Error handling {addr}: {e}")
#     finally:
#         conn.close()
#         print(f"Closed connection with {addr}")


# def run_server():
#     server_ip = '127.0.0.1'
#     server_port = 8000
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((server_ip, server_port))
#     server_socket.listen(5)
#     print(f"Server listening on {server_ip}:{server_port}")
#     output_queue = queue.Queue()

#     try:
#         while True:
#             conn, addr = server_socket.accept()
#             Thread(target=client_thread, args=(conn, addr, output_queue)).start()
#     finally:
#         server_socket.close()
#         print("Server shutdown")

# # Run the server
# run_server()


# import socket
# from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
# from threading import Thread


# # Initialize the tokenizer and model
# tokenizer = AutoTokenizer.from_pretrained("bgsmagnuson/tiny-llama-stack-overflow")
# model = AutoModelForCausalLM.from_pretrained("bgsmagnuson/tiny-llama-stack-overflow")

# # Set up socket
# host = 'localhost'
# port = 12345
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((host, port))
# server_socket.listen(1)
# print("Listening for client...")

# conn, addr = server_socket.accept()
# print(f"Connected by {addr}")

# # Setup generation and streaming
# question = "<s>[INST] How do you loop through an array in Python? [/INST]"
# inputs = tokenizer([question], return_tensors="pt")
# streamer = TextIteratorStreamer(tokenizer, skip_prompt=True)
# generation_kwargs = dict(inputs, streamer=streamer, max_new_tokens=200)
# thread = Thread(target=model.generate, kwargs=generation_kwargs)
# thread.start()

# # Stream the generated text to the client
# generated_text = ""
# for new_text in streamer:
#     generated_text += new_text
#     conn.sendall(generated_text.encode('utf-8'))
#     # print(generated_text)

# conn.close()



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

# Setup generation and streaming
question = "<s>[INST] How do you loop through an array in Python? [/INST]"
inputs = tokenizer([question], return_tensors="pt")
streamer = TextIteratorStreamer(tokenizer, skip_prompt=True)

generator = pipeline("text-generation", model="bgsmagnuson/tiny-llama-stack-overflow")

generation_kwargs = dict(text_inputs=question, streamer=streamer, max_length=100)
thread = Thread(target=generator, kwargs=generation_kwargs)
thread.start()

# Stream the generated text to the client
generated_text = ""
for new_text in streamer:
    generated_text += new_text
    conn.sendall(generated_text.encode('utf-8'))
    print(generated_text)

conn.close()
