import { window } from 'vscode';

/**
 * A function that returns the text of the currently selected range in the active text editor.
 * 
 * @returns The text of the currently selected range in the active text editor. If there is no active text editor, returns null.
 */
export function getSelectedText() {
  const editor = window.activeTextEditor;

  if (editor) {
    const document = editor.document;
    const selection = editor.selection;

    // Get the text of the selected range
    const text = document.getText(selection);
    return text;
  } else {
    // No active text editor
    return null;
  }
}
