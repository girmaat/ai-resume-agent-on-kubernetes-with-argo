
import gradio as gr
from app.assistant.minimal_assistant import ResumeAssistant
from app.github import RepoAnalyzer
from app.github.chat_manager import RepoChatManager
from app.github import GithubLoader, RepoAnalyzer
import os
from dotenv import load_dotenv
from typing import List, Dict
import matplotlib.pyplot as plt
import io
import base64

load_dotenv()
chat_manager = RepoChatManager()
assistant = ResumeAssistant()
github_loader = GithubLoader()
analyzer = RepoAnalyzer()
# Custom Tag Component
def create_tag(tag_text: str, visible: bool = True) -> gr.HTML:
    """Creates a styled tag component using HTML"""
    color_map = {
        "AWS": "#FF9900",
        "AI": "#10B981",
        "DevOps": "#3B82F6",
        "Python": "#3776AB",
        "JavaScript": "#F7DF1E"
    }
    color = color_map.get(tag_text, "#6B7280")
    
    return gr.HTML(
        visible=visible,
        value=f"""
        <span class="skill-tag" style="background: {color}22; border-color: {color}; color: {color}">
            {tag_text}
        </span>
        """
    )

def handle_repo_chat(repo_header: str, message: str, chat_history: list):
    """Handle chat messages with repo context"""
    if not chat_history:
        chat_history = []
    
    # Add user message
    chat_history.append({"role": "user", "content": message})
    yield repo_header, chat_history
    
    try:
        # Get repo URL from header if available
        repo_url = None
        if repo_header and "(" in repo_header:
            repo_url = repo_header.split("(")[-1].rstrip(")")
        
        response = chat_manager.generate_response(repo_url or "resume", message)
        
        bot_response = response.get("text", "No response text")
        if "follow_ups" in response:
            bot_response += "\n\n**Suggested follow-ups:**\n" + "\n".join(f"▸ {q}" for q in response['follow_ups'])
        
        chat_history.append({"role": "assistant", "content": bot_response})
    except Exception as e:
        chat_history.append({"role": "assistant", "content": f"⚠️ Error: {str(e)}"})
    
    yield repo_header, chat_history

active_tab = gr.State(value=0)  # 0=Resume Chat, 1=Repo Analysis, 2=Repo Chat

def handle_repo_click(repo_url: str, action: str) -> list:
    """Handle button clicks for repo actions - returns exactly 9 outputs"""
    # Create default updates for all 9 outputs
    default_updates = [
        gr.update(value=""),                # repo_summary
        gr.update(value=""),                # skills_plot
        gr.update(value=""),                # skills_tags
        gr.update(visible=False),           # aws_tag
        gr.update(visible=False),           # ai_tag
        gr.update(visible=False),           # devops_tag
        gr.update(value=""),                # current_repo_header
        gr.update(value=[]),                # repo_chatbot
        gr.update(selected=0)               # tabs (default to Resume Chat)
    ]
    
    if action == "summary":
        try:
            analysis = analyzer.analyze(repo_url)  # Use the pre-initialized analyzer
            return [
                gr.update(value=analysis["summary"]),
                gr.update(value=f'<img src="{create_skills_plot(analysis["skills"])}" style="max-width: 100%;">'),
                gr.update(value=create_tech_tags(analysis["skills"])),
                gr.update(visible=bool(analysis["skills"].get("aws_resources"))),
                gr.update(visible=bool(analysis["skills"].get("ai_components"))),
                gr.update(visible=bool(analysis["skills"].get("devops"))),
                gr.update(value=f"### Analyzing: {repo_url.split('/')[-1]}"),
                default_updates[7],  # Keep chat as is
                gr.update(selected=1)  # Switch to Repo Analysis tab
            ]
        except Exception as e:
            print(f"Error analyzing repo: {str(e)}")
            return [
                gr.update(value=f"Error analyzing repository: {str(e)}"),
                default_updates[1],
                default_updates[2],
                default_updates[3],
                default_updates[4],
                default_updates[5],
                gr.update(value=f"### Error analyzing: {repo_url}"),
                default_updates[7],
                gr.update(selected=1)  # Still switch to Repo Analysis
            ]
    
    else:  # "chat" action
        if repo_url == "resume":
            return [
                default_updates[0],
                default_updates[1],
                default_updates[2],
                default_updates[3],
                default_updates[4],
                default_updates[5],
                gr.update(value="### Chatting with: My Resume"),
                gr.update(value=[{"role": "system", "content": "Chatting with my resume"}]),
                gr.update(selected=0)  # Switch to Resume Chat tab
            ]
        else:
            return [
                default_updates[0],
                default_updates[1],
                default_updates[2],
                default_updates[3],
                default_updates[4],
                default_updates[5],
                gr.update(value=f"### Chatting with: {repo_url.split('/')[-1]}"),
                gr.update(value=[{"role": "system", "content": f"Chatting about {repo_url}"}]),
                gr.update(selected=2)  # Switch to Repo Chat tab
            ]

def load_public_repos():
    """Load public repos with better error handling"""
    repo_urls = [url.strip() for url in os.getenv("GITHUB_REPOS", "").split(",") if url.strip()]
    
    repos = []
    for repo_url in repo_urls:
        try:
            repo_path = repo_url.split("github.com/")[-1].strip("/")
            repo = github_loader.g.get_repo(repo_path)
            
            repos.append({
                "url": f"https://github.com/{repo_path}",
                "name": repo.name,
                "description": repo.description or "No description",
                "topics": repo.get_topics(),
                "private": repo.private
            })
        except Exception as e:
            print(f"Error loading repo {repo_url}: {str(e)}")
            continue
    
    return [r for r in repos if not r['private']]
    
def create_repo_card(repo):
    """Generate project card UI"""
    topics = " ".join([f"`{t}`" for t in repo["topics"][:3]])
    return f"""
    <div class="repo-card">
        <h4>{repo['name']}</h4>
        <p>{repo['description']}</p>
        <div class="topics">{topics}</div>
    </div>
    """

def respond(message, history):
    history = history or []
    
    # Add user message with icon (using the new format)
    history.append({
        "role": "user", 
        "content": f"🧑 {message}"
    })
    
    # Add temporary assistant message with spinner
    history.append({
        "role": "assistant",
        "content": "<span class='spinner'></span>"
    })
    
    try:
        response = assistant.chat(message)
        # Update with bot response and icon
        history[-1] = {
            "role": "assistant",
            "content": f"🤖 {response}"
        }
    except Exception as e:
        # Update with error message
        history[-1] = {
            "role": "assistant",
            "content": f"⚠️ Error: {str(e)}"
        }
    
    return history

def create_skills_plot(skills: Dict[str, List[str]]) -> str:
    """Generate skill distribution bar chart"""
    fig, ax = plt.subplots(figsize=(8, 4))
    categories = []
    counts = []
    
    for category, items in skills.items():
        if items:
            categories.append(category.replace("_", " ").title())
            counts.append(len(items))
    
    bars = ax.barh(categories, counts, color=['#3B82F6', '#10B981', '#FF9900'])
    ax.bar_label(bars, padding=3)
    ax.set_xlim(0, max(counts) + 1 if counts else 5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig)
    return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"

def create_tech_tags(skills: Dict[str, List[str]]) -> str:
    """Generate colored skill tags HTML"""
    color_map = {
        'languages': '#3B82F6',
        'frameworks': '#8B5CF6', 
        'devops': '#EF4444',
        'ai_components': '#10B981',
        'aws_resources': '#FF9900'
    }
    
    html = []
    for category, items in skills.items():
        if items:
            html.append(f'<div style="margin-bottom: 8px;"><strong>{category.title()}:</strong>')
            for item in items:
                html.append(
                    f'<span class="skill-tag" style="background: {color_map.get(category, "#6B7280")}22; '
                    f'border-color: {color_map.get(category, "#6B7280")}">'
                    f'{item}</span>'
                )
            html.append('</div>')
    return "".join(html)

          
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
    background: var(--background);
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
    background: var(--panel-bg);
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
    background: var(--panel-bg);

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
    background: rgba(255, 255, 255, 0.05);
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
}.repo-card {
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 15px;
    background: var(--surface);
}

.repo-card h4 {
    margin: 0 0 8px 0;
    color: var(--primary);
}

.repo-card p {
    margin: 0 0 10px 0;
    font-size: 0.9em;
    color: var(--text);
    opacity: 0.8;
}

.topics {
    margin-bottom: 12px;
}

.topics code {
    background: var(--primary-dark);
    color: white;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.8em;
    margin-right: 5px;
}

.buttons {
    display: flex;
    gap: 8px;
}

.summary-btn, .chat-btn {
    flex: 1;
    padding: 6px 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.85em;
}

.summary-btn {
    background: var(--primary);
    color: white;
}

.chat-btn {
    background: var(--surface);
    border: 1px solid var(--primary);
    color: var(--primary);
}

/* Equal column widths */
.gr-row > .gr-column {
    flex: 1;
    min-width: 300px;
}

.repo-tech-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 12px 0;
}

.skill-tag {
    display: inline-block;
    padding: 4px 12px;
    margin: 2px;
    border-radius: 16px;
    border: 1px solid;
    color: white;
    font-size: 0.9em;
}

/* Plot container */
.plot-container {
    background: white;
    padding: 12px;
    border-radius: 8px;
    margin: 12px 0;
    border: 1px solid var(--border);
}

/* Responsive tags */
@media (max-width: 768px) {
    .skill-tag {
        font-size: 0.7em;
        padding: 2px 8px;
    }
}

/* Chat specific styles */
.repo-chat-container {
    height: 60vh;
    overflow-y: auto;
    padding-right: 8px;
}

.repo-chat-input {
    margin-top: 15px;
}

/* Message bubbles */
.repo-user-message {
    background: var(--primary);
    color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 10px 16px;
    max-width: 80%;
    margin-left: auto;
}

.repo-bot-message {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 18px 18px 18px 4px;
    padding: 10px 16px;
    max-width: 80%;
    margin-right: auto;
}

/* Add to custom_css */
.followup-container {
    margin-top: 15px;
    padding: 12px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    border-left: 3px solid var(--primary);
}

.followup-title {
    font-size: 0.9em;
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: 8px;
}

.followup-item {
    padding: 6px 10px;
    margin: 4px 0;
    background: rgba(59, 130, 246, 0.1);
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s;
}

.followup-item:hover {
    background: rgba(59, 130, 246, 0.2);
    transform: translateX(2px);
}

.followups {
    margin-top: 1.2em;
    padding: 0.8em;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 8px;
    border-left: 3px solid var(--primary);
}

.followups h4 {
    margin: 0 0 0.5em 0;
    font-size: 0.9em;
    color: rgba(255, 255, 255, 0.7);
}

.followup-question {
    display: block;
    padding: 0.4em 0.8em;
    margin: 0.3em 0;
    background: rgba(59, 130, 246, 0.1);
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s;
}

.followup-question:hover {
    background: rgba(59, 130, 246, 0.2);
    transform: translateX(3px);
}

.repo-header {
    margin: 0 0 15px 0;
    padding: 10px 0;
    border-bottom: 1px solid var(--border);
    color: var(--primary);
    font-size: 1.1em;
}

"""


with gr.Blocks(css=custom_css) as demo:
    with gr.Row():
        # Left Profile Panel
        with gr.Column(scale=3, min_width=220, elem_classes="left-panel"):
            with gr.Column(elem_classes="profile-column"):
                with gr.Column(elem_classes="profile-image-container"):
                    gr.Image("me/profile.png", 
                            elem_classes="profile-image", 
                            show_label=False, 
                            show_download_button=False)
                
                with gr.Column(elem_classes="profile-content"):
                    gr.Markdown("""
                    <h1 class="profile-name">Girma Debella</h1>
                    <h2 class="profile-title">AI Engineer</h2>
                    <p class="profile-description">I specialize in building intelligent systems using LLM.</p>
                    """)
                    
                    gr.Button("Download Resume", elem_classes="download-btn")
                    
                    with gr.Column(elem_classes="divider-section"):
                        gr.Markdown("""<h4 class="divider-title">I Built This AI to Talk About My Resume</h4>""")
                        gr.Markdown("""<a href="https://yourblog.com" target="_blank" class="blog-link">Link to my blog here - left aligned</a>""")
                        gr.Markdown("""<p class="divider-text">This demo showcases a full-stack AI assistant I built from scratch to chat about my own resume. Powered by OpenAI's GPT models and deployed with Kubernetes, ArgoCD, and GitOps, it answers questions about my experience and triggers tool-based actions like logging interest or unknown queries. It reflects my skills in prompt engineering, tool calling, PDF parsing, and secure, observable DevOps — demonstrating that I don't just use AI, I engineer systems around it.</p>""")
                        gr.Markdown("""<h4 class="divider-title">Start Chatting with My Resume</h4>""")
                        gr.Markdown("""<p class="divider-text">Start typing to ask me anything about my work, projects, or experience — the assistant will respond in real time.</p>""")       
        
        # Middle Column - Project List
        with gr.Column(scale=2):
            gr.Markdown("### My Projects")
            public_repos = load_public_repos()
            
            # Resume chat card
            with gr.Group(elem_classes="repo-card"):
                gr.Markdown("""
                **Chat With My Resume**
                <p>Ask about my experience and skills</p>
                """)
                with gr.Row():
                    resume_summary_btn = gr.Button("AI Summary", elem_classes="summary-btn")
                    resume_chat_btn = gr.Button("Chat", elem_classes="chat-btn")
            
            # Repository cards
            repo_components = []
            for repo in public_repos:
                with gr.Group(elem_classes="repo-card"):
                    gr.Markdown(create_repo_card(repo))
                    with gr.Row():
                        summary_btn = gr.Button("AI Summary", elem_classes="summary-btn")
                        chat_btn = gr.Button("Chat", elem_classes="chat-btn")
                        repo_components.append((repo["url"], summary_btn, chat_btn))
        
        # Right Column - Content
        with gr.Column(scale=4, elem_classes="right-panel"):
            tabs = gr.Tabs()
            with tabs:
                # Resume Chat Tab
                with gr.Tab("Resume Chat", id="resume_chat"):
                    resume_header = gr.Markdown(
                        "### Chat with My Resume",
                        elem_classes="repo-header"
                    )
                    chatbot = gr.Chatbot(
                        elem_classes="chat-container",
                        type="messages",  
                        avatar_images=("🧑", "🤖")
                    )
                    msg = gr.Textbox(placeholder="Ask about my resume...", elem_classes="chat-input")
                    msg.submit(
                        respond,
                        [msg, chatbot],
                        [chatbot, msg]
                    )
                    
                # Repo Analysis Tab
                with gr.Tab("Repo Analysis", id="repo"):
                    repo_summary = gr.Markdown()
                    gr.Markdown("### Skill Distribution")
                    skills_plot = gr.HTML()
                    gr.Markdown("### Technology Breakdown")
                    skills_tags = gr.HTML()
                    with gr.Row():
                        aws_tag = create_tag("AWS", False)
                        ai_tag = create_tag("AI", False)
                        devops_tag = create_tag("DevOps", False)
                
                # Repo Chat Tab
                with gr.Tab("Repo Chat", id="repo_chat"):
                    current_repo_header = gr.Markdown(
                        "### Select a repository to chat with",
                        elem_classes="repo-header"
                    )
                    repo_chatbot = gr.Chatbot(
                        elem_classes="chat-container",
                        type="messages"
                    )
                    repo_msg = gr.Textbox(placeholder="Ask about this repository...")
                    repo_msg.submit(
                        handle_repo_chat,
                        [current_repo_header, repo_msg, repo_chatbot],
                        [current_repo_header, repo_chatbot]
                    )
        # Bind resume buttons
        resume_summary_btn.click(
            lambda: handle_repo_click("resume", "summary"),
            outputs=[
                repo_summary, skills_plot, skills_tags,
                aws_tag, ai_tag, devops_tag,
                current_repo_header, repo_chatbot,
                tabs
            ]
        )

        resume_chat_btn.click(
            lambda: handle_repo_click("resume", "chat"),
            outputs=[
                repo_summary, skills_plot, skills_tags,
                aws_tag, ai_tag, devops_tag,
                current_repo_header, repo_chatbot,
                tabs
            ]
        )

        # For repo cards
        for repo_url, summary_btn, chat_btn in repo_components:
            summary_btn.click(
                lambda url=repo_url: handle_repo_click(url, "summary"),
                outputs=[
                    repo_summary, skills_plot, skills_tags,
                    aws_tag, ai_tag, devops_tag,
                    current_repo_header, repo_chatbot,
                    tabs
                ]
            )
            chat_btn.click(
                lambda url=repo_url: handle_repo_click(url, "chat"),
                outputs=[
                    repo_summary, skills_plot, skills_tags,
                    aws_tag, ai_tag, devops_tag,
                    current_repo_header, repo_chatbot,
                    tabs
                ]
            )

if __name__ == "__main__":
    demo.launch()
