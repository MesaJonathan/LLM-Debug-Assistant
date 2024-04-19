import { window, ExtensionContext } from "vscode";
import { DebugAssistantViewProvider } from "./views/DebugAssistantViewProvider";

export function activate(context: ExtensionContext) {
  context.subscriptions.push(
    window.registerWebviewViewProvider(
      DebugAssistantViewProvider.viewType,
      new DebugAssistantViewProvider(context.extensionUri)
    )
  );
}
