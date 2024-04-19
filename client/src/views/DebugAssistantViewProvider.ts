import { Disposable, Webview, WebviewView, WebviewViewProvider, window, Uri } from "vscode";
import { getUri } from "../utilities/getUri";
import { getNonce } from "../utilities/getNonce";
import { getSelectedText } from "../utilities/getSelectedText";
import { connect, Socket } from "net";

export class DebugAssistantViewProvider implements WebviewViewProvider {
  public static readonly viewType = 'debugAssistant.view';

  private _view?: WebviewView;

  constructor(
    private readonly _extensionUri: Uri,
  ) { }

  public resolveWebviewView(
    webviewView: WebviewView,
  ) {
    this._view = webviewView;

    let socket: Socket | null = connect({ port: 12345 });

    socket.on('data', (data) => {

      const message = data.toString();

      if (message.endsWith('<END>')) {
        webviewView.webview.postMessage({
          command: "end-response",
        });
        // console.log('End of message');
      } else {
        webviewView.webview.postMessage({
          command: "partial-response",
          author: "Assistant",
          text: message,
        });
        // console.log('Received:', message);
      }
    });

    socket.on('error', (error: any) => {
      console.error('Socket error:', error);
    });

    webviewView.webview.options = {
      enableScripts: true,
    };

    webviewView.webview.html = this._getWebviewContent(webviewView.webview, this._extensionUri);

    webviewView.onDidDispose(() => {
      if (socket) {
        socket.end();
        socket = null;
      }
    });

    webviewView.webview.onDidReceiveMessage(message => {
      const command = message.command;

      if (command === 'echo') {
        const selectedText = getSelectedText();
        let text = message.text;
        if (selectedText) {
          text = `\`\`\`\n${selectedText}\n\`\`\`\n${text}`;
        }
        setTimeout(() => {
          webviewView.webview.postMessage({
            command: "echo",
            author: "VS Code",
            text,
          });
        }, 1000);

      } else if (command === 'prompt') {
        const selectedText = getSelectedText();
        let text = message.text;
        if (selectedText) {
          text = `\`\`\`\n${selectedText}\n\`\`\`\n${text}`;
        }

        socket?.write(text);
      }
    });
  }

  /**
   * Defines and returns the HTML that should be rendered within the webview panel.
   *
   * @remarks This is also the place where references to the React webview build files
   * are created and inserted into the webview HTML.
   *
   * @param webview A reference to the extension webview
   * @param extensionUri The URI of the directory containing the extension
   * @returns A template string literal containing the HTML that should be
   * rendered within the webview panel
   */
  private _getWebviewContent(webview: Webview, extensionUri: Uri) {
    // The CSS file from the React build output
    const stylesUri = getUri(webview, extensionUri, ["webview-ui", "build", "assets", "index.css"]);

    const codiconsUri = webview.asWebviewUri(Uri.joinPath(extensionUri, 'node_modules', '@vscode/codicons', 'dist', 'codicon.css'));
    // The JS file from the React build output
    const scriptUri = getUri(webview, extensionUri, ["webview-ui", "build", "assets", "index.js"]);

    const nonce = getNonce();

    // Tip: Install the es6-string-html VS Code extension to enable code highlighting below
    return /*html*/ `
      <!DOCTYPE html>
      <html lang="en">
        <head>
          <meta charset="UTF-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1.0" />
          <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src ${webview.cspSource}; font-src ${webview.cspSource}; script-src 'nonce-${nonce}';">
          <link rel="stylesheet" type="text/css" href="${stylesUri}">
          <link href="${codiconsUri}" rel="stylesheet" />
          <title>LLM Debug Assistant</title>
        </head>
        <body>
          <div id="root"></div>
          <script type="module" nonce="${nonce}" src="${scriptUri}"></script>
        </body>
      </html>
    `;
  }

}
