import { vscode } from "./utilities/vscode";
import { VSCodeTextArea, VSCodeButton } from "@vscode/webview-ui-toolkit/react";
import React from "react";
import Message from "./Message";
import Loading from "./Loading";
import "./App.css";

function App() {

  const [messages, setMessages] = React.useState<{ author: string, text: string }[]>([]);
  const [inputValue, setInputValue] = React.useState("");

  const [loading, setLoading] = React.useState(false);

  React.useEffect(() => {
    window.addEventListener("message", (event) => {
      const message = event.data;
      if (message.command === "echo") {
        postMessage({ author: message.author, text: message.text });

      } else if (message.command === "partial-response") {
        setLoading(true);
        postMessage({ author: "Assistant", text: message.text });

      } else if (message.command === "end-response") {
        setLoading(false);
      }

    });

    return () => {
      window.removeEventListener("message", () => { });
    }
  }, []);

  function postMessage(message: { author: string, text: string }) {
    setMessages(prev => {
      if (prev[0]?.author === message.author) {
        prev[0].text = message.text;
        return [...prev];
      }
      return [message, ...prev];
    });
  }

  function handleFormSubmit(e?: React.FormEvent<HTMLFormElement>) {
    e && e.preventDefault();
    if (inputValue) {
      postMessage({ author: "You", text: inputValue });
      vscode.postMessage({
        command: "prompt",
        author: "You",
        text: inputValue,
      });
    }
    setInputValue("");
  }

  function handleTextEnter(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter') {
      e.preventDefault();
      setInputValue(prev => prev + '\n');
    }
    if (e.key === 'Enter' && !e.shiftKey) {
      handleFormSubmit();
    }
  }

  function handleResetBtnClick() {
    setMessages([]);
  }

  function renderMessages() {
    return messages.map((message, index) => {
      return <Message key={index} author={message.author} text={message.text} />;
    });
  }

  function renderLoading() {
    return <Loading />;
  }


  return (
    <main>
      <div className="controls">
        <VSCodeButton onClick={handleResetBtnClick}>
          New Chat
        </VSCodeButton>
      </div>
      <div className="messages">
        {renderMessages()}
      </div>
      {loading && renderLoading()}
      <form className="text-entry" onSubmit={handleFormSubmit}>
        <VSCodeTextArea
          resize='vertical'
          cols={120}
          value={inputValue}
          onInput={e => setInputValue((e as React.ChangeEvent<HTMLInputElement>).target.value)}
          placeholder='Ask me anything...'
          onKeyDown={handleTextEnter}
        >
        </VSCodeTextArea>
        <VSCodeButton appearance="icon" type="submit">
          <span className="codicon codicon-send"></span>
        </VSCodeButton>
      </form>
    </main>
  );
}

export default App;
