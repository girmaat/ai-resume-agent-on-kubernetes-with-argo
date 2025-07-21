# ------------------------------------------------------------------------------
# Purpose: Basic Gradio chatbot UI that connects to ResumeAssistant class.
#
# How to Run:
#   python app/ui/gradio_minimal.py
#
# Expected Output:
#   A browser window with a textbox and chat history.
#   User types a question, sees assistant's response.
# ------------------------------------------------------------------------------

import gradio as gr
from app.assistant.minimal_assistant import ResumeAssistant

assistant = ResumeAssistant()

# UI logic function
def respond(message, history):
    history.append({"role": "user", "content": message})
    reply = assistant.chat(message)
    history.append({"role": "assistant", "content": reply})

    # Convert history into Gradio chat format
    chat_display = []
    for m in history:
        if m["role"] == "user":
            chat_display.append((m["content"], None))
        elif m["role"] == "assistant":
            chat_display.append((None, m["content"]))

    return chat_display, history, ""
theme_css = """
/* Full page background */
html, body, .gradio-container {
    background-color: #0a172b !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    margin: 0;
    padding: 0;
}

/* Chat area styling (right panel) */
.right-panel {
    background-color: #0f172a;
    border-radius: 16px;
    padding: 24px;
    box-sizing: border-box;
    height: 100%;
}

/* Chatbot bubbles */
.gr-chatbot {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.gr-chatbot .message {
    border-radius: 16px;
    padding: 12px 18px;
    font-size: 16px;
    line-height: 1.6;
    margin: 8px 0;
}

.gr-chatbot .user {
    background-color: #1e293b;
    color: #ffffff;
    align-self: flex-end;
    margin-left: auto;
}

.gr-chatbot .assistant {
    background-color: #1e293b;
    color: #ffffff;
    align-self: flex-start;
    margin-right: auto;
}

/* Input bar and send button */
.input-bar {
    margin-top: 16px;
    display: flex;
    gap: 8px;
    align-items: center;
}

.gr-textbox {
    background-color: transparent;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 12px;
    flex: 1;
    color: #ffffff;
}

.gr-button {
    background-color: #38bdf8;
    border: none;
    border-radius: 6px;
    color: white;
    font-weight: 600;
    padding: 10px 16px;
    cursor: pointer;
}

"""

with gr.Blocks(css=theme_css) as demo:
    with gr.Row():
        # LEFT column (leave untouched for now)
        with gr.Column(scale=1):
            gr.Markdown("<!-- Placeholder for left column -->")

        # RIGHT column (chat UI)
        with gr.Column(scale=2, elem_classes="right-panel"):
            chatbot = gr.Chatbot(label="Ask me anything about Girma")
            msg = gr.Textbox(placeholder="Type your message and here and hit enter to get response...", show_label=False)
            state = gr.State([])

            def respond(message, history):
                history.append({"role": "user", "content": message})
                reply = assistant.chat(message)
                history.append({"role": "assistant", "content": reply})
                chat_display = []
                for m in history:
                    if m["role"] == "user":
                        chat_display.append((m["content"], None))
                    elif m["role"] == "assistant":
                        chat_display.append((None, m["content"]))
                return chat_display, history, ""

            msg.submit(respond, inputs=[msg, state], outputs=[chatbot, state, msg])


if __name__ == "__main__":
    demo.launch()
