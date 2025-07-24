import os
from typing import Dict, List
from openai import OpenAI
from app.github.cache import RepoCache

class RepoChatManager:
    def __init__(self):
        self.cache = RepoCache()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.followup_prompt = """Based on the conversation, suggest 3 technical follow-up questions focusing on:
- Code structure
- Implementation details
- Architecture
Format as bullet points without numbering."""

    def get_chat_history(self, repo_url: str) -> List[Dict]:
        """Retrieve or initialize chat history"""
        if history := self.cache.get(f"chat_{repo_url}"):
            return history
        return [{
            "role": "system",
            "content": f"You are a technical expert analyzing {repo_url}. "
                      "Answer questions about the codebase, architecture, and "
                      "implementation details."
        }]
    
    def add_message(self, repo_url: str, role: str, content: str):
        """Persist chat messages"""
        history = self.get_chat_history(repo_url)
        history.append({"role": role, "content": content})
        self.cache.store(f"chat_{repo_url}", history)
    

    def generate_response(self, repo_url: str, user_query: str) -> dict:
        """Generate AI response with repo context"""
        history = self.get_chat_history(repo_url)
        history.append({"role": "user", "content": user_query})
        
        # Get main response
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=history,
            temperature=0.3
        )
        ai_response = response.choices[0].message.content
        
        # Generate follow-ups
        follow_ups = self._generate_follow_ups(history[-3:])
        
        return {
            "text": ai_response,
            "follow_ups": follow_ups
        }

    def _generate_follow_ups(self, context: list) -> list:
        """Generate technical follow-up questions"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": self.followup_prompt + "\n\nContext:\n" + 
                              "\n".join(f"{m['role']}: {m['content']}" for m in context)
                }],
                temperature=0.5,
                max_tokens=100
            )
            return [line[2:].strip() for line in response.choices[0].message.content.split('\n') if line.strip()][:3]
        except Exception:
            return [
                "How is error handling implemented?",
                "What's the data flow architecture?",
                "Are there performance benchmarks?"
            ]
    
