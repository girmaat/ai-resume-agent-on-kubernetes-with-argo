import gradio as gr
from app.assistant.minimal_assistant import ResumeAssistant

assistant = ResumeAssistant()

def respond(message, history):
    history = history or []
    history.append((f"🧑 {message}", "<span class='spinner'></span>"))
    response = assistant.chat(message)
    history[-1] = (f"🧑 {message}", f"🤖 {response}")
    return history, history

custom_css = """
:root {    
    --primary: #0ea5e9;
    --primary-dark: #0284c7;  
    --background: #0f172a;
    --surface: #1e293b;
    --text: #ffffff;
    --border: #334155;
    --divider: #334155;
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
    margin-bottom: 20px !important;
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
}

.chat-message {
    max-width: 80%;
    margin-bottom: 15px;
    padding: 12px 16px;
    border-radius: 18px;
    line-height: 1.5;
}

.user-message {
    background: var(--primary);
    color: white;
    margin-left: auto;
    border-bottom-right-radius: 4px;
}

.bot-message {
    background: rgba(255, 255, 255, 0.1);
    margin-right: auto;
    border-bottom-left-radius: 4px;
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
    color: white;
    font-size: 1rem;
}

.chat-input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.3);
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
"""

with gr.Blocks(css=custom_css) as demo:
    with gr.Row():
        # Left Profile Panel
        with gr.Column(scale=2, min_width=220, elem_classes="left-panel"):
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
                    gr.Markdown("""
                    <h1 class="profile-name">Girma Debella</h1>
                    <h2 class="profile-title">AI Engineer</h2>
                    <p class="profile-description">I specialize in building intelligent systems using LLM.</p>
                    """)
                    
                    # Download button
                    gr.Button("Download Resume", elem_classes="download-btn")
                    
                    # Divider section
                    with gr.Column(elem_classes="divider-section"):
                        gr.Markdown("""<h4 class="divider-title">I Built This AI to Talk About My Resume</h4>""")
                        gr.Markdown("""<a href="https://yourblog.com" target="_blank" class="blog-link">Link to my blog here - left aligned</a>""")
                        gr.Markdown("""<p class="divider-text">This demo showcases a full-stack AI assistant I built from scratch to chat about my own resume. Powered by OpenAI’s GPT models and deployed with Kubernetes, ArgoCD, and GitOps, it answers questions about my experience and triggers tool-based actions like logging interest or unknown queries. It reflects my skills in prompt engineering, tool calling, PDF parsing, and secure, observable DevOps — demonstrating that I don’t just use AI, I engineer systems around it.</p>""")
                        gr.Markdown("""<h4 class="divider-title">Start Chatting with My Resume</h4>""")
                        gr.Markdown("""<p class="divider-text">Start typing to ask me anything about my work, projects, or experience — the assistant will respond in real time.</p>""")

        # Right Chat Panel
        with gr.Column(scale=3, elem_classes="right-panel"):
            chatbot = gr.Chatbot(
                elem_classes="chat-container",
                label=None,
                show_label=False,
                bubble_full_width=False,
                sanitize_html=False,
                avatar_images=("🧑", "🤖")
            )
            
            with gr.Row(elem_classes="input-container"):
                msg = gr.Textbox(
                    placeholder="Chat with my resume — just type here a question about my work or experience...",
                    elem_classes="chat-input",
                    show_label=False,
                    container=False
                )
            
            state = gr.State([])
            msg.submit(respond, [msg, state], [chatbot, state]).then(lambda: "", None, msg)

if __name__ == "__main__":
    demo.launch()
