# LLM-Debug-Assistant

## Table of Contents

- [Client](#client)
- [Server](#server)
- [Notebooks](#notebooks)

## Client

The Visual Studio Code extension that provides the user interface for the LLM Debug Assistant, allowing one to get assistance with coding.

### Warning

Running the extension and Python server simultaneously may take up a lot of resources. 
We tested this project on a computer running Ubuntu 22.04 with 16GM of RAM and an Intel 12th Gen i7-12700H CPU.

If you find that the Python server process is stopping unexpectedly, you may need to free up memory on your computer.

### Instructions

First start the Python server. See the [Server](#server) section for instructions on how to do this.

Ensure you have Node.js and npm installed on your computer.
Open the client directory in VS Code and run the following commands. 
```bash
# Install dependencies for both the extension and webview UI source code
npm run install:all

# Build webview UI source code
npm run build:webview
```

To run the extension, press `F5` or go to Run -> Start Debugging.

Click the speech bubble icon in the activity bar to open the Debug Assistant.
It will be named "Debug Assistant".

Start entering text in the input box to chat with the LLM.
Click "New Chat" to clear the messages.

## Server

The server that connects the Visual Studio Code extension to the LLM model hosted on Hugging Face.

The Hugging Face model can be accessed [here](https://huggingface.co/bgsmagnuson/tiny-llama-code-feedback).

### Instructions

Ensure you have Python 3.8 or higher installed on your computer.

Navigate to the server directory.

If you would like to run the server in a virtual environment, run the following commands.
```bash
python3 -m venv venv
source venv/bin/activate
```
If on Windows, replace `source venv/bin/activate` with `.\venv\Scripts\activate`.

Install the necessary dependencies by running the following command:
```bash
pip install -r requirements.txt
```

Start the server by running the following command:
```bash
python3 server.py
```

The server will be running on `http://localhost:12345`.

Wait for the message that reads:
```
Listening for client...
```

## Notebooks

Jupyter notebooks that were used to train the LLM model and run tensorboard.

### Warning

Fine-tuning the LLM model requires a large amount of memory and may take a long time to complete. 
The bgsmagnuson/tiny-llama-code-feedback model was fine-tuned on a computer running Ubuntu 22.04 with 16GB of RAM and an Intel 12th Gen i7-12700H CPU and took approximately 3 hours to fine-tune.

### Instructions

These instructions are designed for running the notebooks on VS Code. Other IDEs and methods of running Jupyter notebooks may require different steps.

Ensure you have Python 3.8 or higher installed on your computer.

Open the notebooks directory in VS Code.

Install the necessary dependencies by running the following command in the terminal.
```bash
pip install -r requirements.txt
```
Note: This may take a few minutes in areas with slow internet connections.

Open `main.ipynb` and run the cells in order to fine-tune the LLM model.

`eval.ipynb` contains information on running the model through tensorboard.
