import gradio as gr
from app.assistant.minimal_assistant import ResumeAssistant
from app.assistant.config.non_ai import config
import time
import re
import os

assistant = ResumeAssistant()

def get_ui_config():
    """Helper to get current UI config"""
    return config.UI

initial_text = config.UI["chat"]["initial_message"]
def clean_message(message):
    """Remove any project path prefixes from messages"""
    if message and ("Personal Folder:" in message or "|" in message):
        return message.split("|")[-1].strip()
    return message

def type_message(message, delay=config.CHAT["typing_delay"]):
    message = clean_message(message)
    typed_message = ""
    for char in message:
        typed_message += char
        yield typed_message
        time.sleep(config.CHAT["response_delay"])

def clean_response(response):
    # Only replace when the full name appears (not first name alone)
    full_name = config.PERSONAL['name']
    if full_name in response:
        response = response.replace(f"{full_name}'s", f"{config.first_name}'s")
        response = response.replace(full_name, config.first_name)
    return re.sub(r'\s+', ' ', response).strip()

def respond(message, history):
    ui_config = get_ui_config()
    history = history or []
    
    # 1. Display original user message exactly as typed
    history.append((message, ""))  # No processing of user input
    yield history, history
    
    # 2. Show thinking indicator
    history[-1] = (message, ui_config["chat"]["thinking_message"])
    yield history, history
    
    # 3. Get and clean AI response (only affects bot's replies)
    response = assistant.chat(message)  # Pass original message unchanged
    
    clean_response = clean_message(response)
    clean_response = (
        clean_response
        .replace(f"{config.PERSONAL['name']}'s", f"{config.first_name}'s")
        .replace(f"{config.PERSONAL['name']} ", f"{config.first_name} ")
        .replace("  ", " ")
        .strip()
    )
    
    # 4. Type out response
    full_response = ""
    for char in clean_response:
        full_response += char
        history[-1] = (message, full_response)  # Keep original user message
        yield history, history
        time.sleep(ui_config["chat"]["typing_delay"])
           
def load_initial_message():
    ui_config = get_ui_config()
    initial_text = ui_config["chat"]["initial_message"]
    initial_text = clean_message(initial_text)
    for partial in type_message(initial_text):
        yield [(None, partial)]
    return [(None, initial_text)]
    
def get_resume_path(self):
    """Return the path to the resume PDF file"""
    path = config.PERSONAL["resume_pdf"]
    if not os.path.exists(path):
        raise FileNotFoundError(f"Resume file not found at {path}")
    return path


custom_css = """
:root {    
    --primary: #0ea5e9;
    --primary-dark: #0284c7;  
    --background: #0f172a;
    --surface: #1e293b;
    --text: #ffffff;
    --border: #334155;
    --divider: #334155;
    --placeholder: #000000;
    --bot-bg: rgba(0, 0, 0, 0.3);  
    --user-bg: #1e293b;
}

/* Base Layout */
body, .gradio-container {
    margin: 0;
    padding: 0;
    height: 100vh;
    width: 100vw;
    overflow: hidden;
    font-family: 'Inter', sans-serif;
    background: var(--surface);
    color: var(--text);
}

/* Main Row Layout */
.gr-row {
    display: flex;
    height: 100vh;
    margin: 0;
    padding: 0;
    overflow: hidden;
}

/* Left Profile Panel - Fixed Width */
.left-panel {
    width: 350px;
    min-width: 350px;
    height: 100vh;
    background: var(--background);
    border-right: 1px solid var(--border);
    padding: 30px;
    box-sizing: border-box;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
}

/* Profile Column - Ensures vertical stacking */
.profile-column {
    display: flex !important;
    flex-direction: column !important;
    gap: 20px !important;
    width: 100% !important;
}

.profile-image-container {
    display: flex !important;
    justify-content: center !important;
}

.profile-image {
    width: 150px !important;
    height: 150px !important;
    border-radius: 50% !important;
    object-fit: cover !important;
    border: 4px solid rgba(255, 255, 255, 0.1) !important;
    display: block !important;
}

.profile-content {
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
    width: 100% !important;
}

.profile-name {
    font-size: 1.8rem !important;
    margin: 0 !important;
    font-weight: 600 !important;
    text-align: center !important;
    color: #ffffff !important;
}

.profile-title {
    font-size: 1.2rem !important;
    margin: 0 !important;
    color: rgba(255, 255, 255, 0.8) !important;
    font-weight: 400 !important;
    text-align: center !important;
}

.profile-description {
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    margin: 0 !important;
    color: rgba(255, 255, 255, 0.7) !important;
    text-align: center !important;
}

/* Download Button */
.download-btn {
    background: var(--primary) !important;
    color: white !important;
    border: none !important;
    padding: 12px 24px !important;
    border-radius: 25px !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    width: 100% !important;
    margin: 20px 0 !important;
    transition: all 0.2s ease !important;
    text-align: center !important;
}

.download-btn:hover {
    background: #0284c7 !important;
    transform: translateY(-2px) !important;
}

/* Divider Section */
.divider-section {
    border: 1px solid var(--divider) !important;
    border-radius: 8px !important;
    padding: 20px !important;
    margin: 20px 0 !important;
    width: 100% !important;
    box-sizing: border-box !important;
}

.divider-title {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    margin: 0 0 15px 0 !important;
    text-align: center !important;
    color: #ffffff !important;
}

.blog-link {
    color: white !important;
    text-decoration: underline !important;
    display: block !important;
    text-align: left !important;
    margin: 0 0 15px 0 !important;
    font-size: 0.95rem !important;
}

.divider-text {
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    color: rgba(255, 255, 255, 0.7) !important;
    text-align: left !important;
    margin: 0 !important;
}

/* Right Chat Panel */
.right-panel {
    flex: 1;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    background: var(--background);

}

/* Chat Interface */
.chat-container {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    background: var(--background);
    padding: 10px !important;  
}

.chat-message {
    max-width: 80%;
    margin-bottom: 15px;
    padding: 12px 16px;
    border-radius: 18px;
    line-height: 1.5;
}

.chat-container .user {
    background: var(--surface);
    margin-left: auto;
    border: none;
}

.chat-container .bot {
    margin-right: auto;
    border: none;
    background: var(--bot-bg) !important;
}

.bot *, .user *{
    color: rgba(255, 255, 255, 1) !important;
}

/* Input Area */
.input-container {
    padding: 15px;
}

.chat-input {
    width: 100%;
    padding: 12px 20px;
    border-radius: 25px;
    border: 1px solid var(--border);
    background: var(--background);
    color: var(--text) !important;
    font-size: 1rem;
}

.chat-input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.3);
}

.chat-input::placeholder {
    color: var(--placeholder) !important;
    opacity: 1 !important; /* Ensure full visibility */
}

/* Mobile Responsiveness */
@media (max-width: 768px) {
    .gr-row {
        flex-direction: column;
    }
    
    .left-panel {
        width: 100%;
        height: auto;
        max-height: 50vh;
        min-width: unset;
    }
    
    .right-panel {
        height: 50vh;
    }
}

/* Remove circular avatars */
.gr-chatbot .avatar {
    display: none !important;
}

/* Adjust message alignment */
.gr-chatbot .user-message {
    margin-left: auto;
    border-bottom-right-radius: 4px;
}

.gr-chatbot .assistant-message {
    margin-right: auto;
    border-bottom-left-radius: 4px;
}
.gr-chatbot {
    background: var(--background) !important;
}


.gr-chatbot .assistant-message {
    color: #ffffff !important;
    margin-right: auto !important;
    border-bottom-left-radius: 4px !important;
    border: 1px solid #2d5a2d !important;
}
/* Spinner Animation */
.spinner {
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
    margin-left: 8px;
    vertical-align: middle;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

"""

with gr.Blocks(css=custom_css) as demo:
    ui_config = get_ui_config()    
    with gr.Row():
        # Left Profile Panel
        with gr.Column(scale=1, min_width=220, elem_classes="left-panel"):
            # Main vertical container
            with gr.Column(elem_classes="profile-column"):
                # Profile image (centered)
                with gr.Column(elem_classes="profile-image-container"):
                    gr.Image("me/profile.png", 
                            elem_classes="profile-image", 
                            show_label=False, 
                            show_download_button=False)
                
                # Profile text content
 
                with gr.Column(elem_classes="profile-content"):
                    gr.Markdown(f"""
                    <h1 class="profile-name">{config.PERSONAL['name']}</h1>
                    <h2 class="profile-title">{config.PERSONAL['title']}</h2>
                    <p class="profile-description">{config.PERSONAL['description']}</p>
                    """)
                    
                    download_btn = gr.Button(
                        config.PERSONAL["resume_button_text"], 
                        elem_classes="download-btn"
                    )
                    file_download = gr.File(visible=False)

                    with gr.Column(elem_classes="divider-section"):
                        gr.Markdown(f"""<h4 class="divider-title">{ui_config["titles"]["assistant_title"]}</h4>""")
                        gr.Markdown(f"""<a href="{config.PERSONAL["blog_url"]}" target="_blank" class="blog-link">{ui_config["titles"]["blog_link_text"]}</a>""")
                        gr.Markdown(f"""<p class="divider-text">{ui_config["descriptions"]["assistant_description"]}</p>""")
                        gr.Markdown(f"""<h4 class="divider-title">{ui_config["titles"]["start_chatting_title"]}</h4>""")
                        gr.Markdown(f"""<p class="divider-text">{ui_config["chat"]["start_chatting_text"]}</p>""")
        # Right Chat Panel 
        with gr.Column(scale=2, elem_classes="right-panel"):
            chatbot = gr.Chatbot(
                elem_classes="chat-container",
                label=None,
                show_label=False,
                bubble_full_width=False,
                sanitize_html=False,
                avatar_images=None  
            )
            
            with gr.Row(elem_classes="input-container"):
                msg = gr.Textbox(
                    placeholder=config.UI["chat"]["input_placeholder"],
                    elem_classes="chat-input",
                    show_label=False,
                    container=False
                )
            
            state = gr.State([])
            
            # Load initial message with typing effect
            def load_initial_message():
                initial_text = config.UI["chat"]["initial_message"]
                for i in range(1, len(initial_text)+1):
                    yield [(None, initial_text[:i])]
                    time.sleep(0.02)
                yield [(None, initial_text)]
            
            # Modified to preserve initial message
            def respond(message, history):
                history = history or []
                
                # Keep original user message
                history.append((message, ""))
                yield history, history
                
                # Show thinking indicator
                history[-1] = (message, config.UI["chat"]["thinking_message"])
                yield history, history
                
                # Get and display response
                response = assistant.chat(message)
                clean_response = clean_message(response)
                
                full_response = ""
                for char in clean_response:
                    full_response += char
                    history[-1] = (message, full_response)
                    yield history, history
                    time.sleep(config.UI["chat"]["typing_delay"])
            
            demo.load(
                load_initial_message,
                inputs=None,
                outputs=[chatbot]
            ).then(
                lambda: [(None, config.UI["chat"]["initial_message"])],  # Keep initial message
                outputs=[state]
            )
            
            msg.submit(
                respond,
                inputs=[msg, state],
                outputs=[chatbot, state]
            ).then(
                lambda: "",
                None,
                msg
            )
if __name__ == "__main__":
    demo.launch()
