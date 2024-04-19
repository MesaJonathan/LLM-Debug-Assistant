# LLM Debug Assistant Frontend

This extension is a provides a frontend for our Debug Assistant LLM. 
It provides a UI for the user to chat with the LLM and get assistance with coding.

## Warning

Running the extension and Python server simultaneously may take up a lot of resources. 
We tested this project on a computer running Ubuntu 22.04 with 16GM of RAM and an Intel 12th Gen i7-12700H CPU.

If you find that the Python server process is stopping unexpectedly, you may need to free up some resources on your computer.

## How To Start

First start the Python server. Navigate to the directory where `server.py` is located.

If you would like to set up a Python virtual environment, you can do so by running the following commands:
```bash
python3 -m venv venv
source venv/bin/activate
```
On Windows, you can activate the virtual environment by running the following command:
```
.\venv\Scripts\activate
```

Install the necessary dependencies by running the following command:
```bash
pip install -r requirements.txt
```

Start the server by running the following command:
```bash
python3 server.py
```

Wait for the server to start. You should see the following message:
```
Listening for client...
```

For the VS Code extension, open the project in VS Code and run the following commands. 
Note that you will need to have Node.js installed on your computer.
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
