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

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(label="Chat with Girma's Resume")
    state = gr.State([])  # conversation history

    msg = gr.Textbox(
        placeholder="Type your question here...",
        label="Your Message"
    )

    msg.submit(respond, inputs=[msg, state], outputs=[chatbot, state, msg])

if __name__ == "__main__":
    demo.launch()
