from github import Github, GithubException
import os
from typing import Optional, Dict
from datetime import datetime
import time
import logging
from app.github.cache import RepoCache

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GithubLoader:
    def __init__(self):
        self.g = Github(os.getenv("GITHUB_TOKEN"))
        self.cache = RepoCache()
        self.last_request_time = None
        self.rate_limit_delay = 1.0  # seconds between requests

    def _handle_rate_limit(self):
        """Ensure we don't exceed GitHub's rate limits"""
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.rate_limit_delay:
                time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()

    def get_repo(self, repo_url: str) -> Optional[Dict]:
        """Get enriched repo data with caching and rate limiting"""
        try:
            # Try cache first
            if cached := self.cache.get(repo_url):
                return cached

            self._handle_rate_limit()
            
            repo_path = repo_url.split("github.com/")[-1]
            repo = self.g.get_repo(repo_path)
            
            # Get readme with fallback
            readme_content = ""
            try:
                readme_content = repo.get_readme().decoded_content.decode('utf-8')
            except Exception as readme_error:
                logger.warning(f"Could not fetch readme for {repo_path}: {readme_error}")

            result = {
                "name": repo.name,
                "description": repo.description or "",
                "topics": repo.get_topics(),
                "readme": readme_content,
                "last_updated": repo.updated_at.isoformat() if repo.updated_at else None,
                "cached_at": datetime.utcnow().isoformat()
            }
            
            # Store in cache
            self.cache.store(repo_url, result)
            return result
            
        except GithubException as ge:
            logger.error(f"GitHub API error for {repo_url}: {str(ge)}")
            if ge.status == 403:
                logger.warning("Rate limit exceeded - consider increasing delay")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching {repo_url}: {str(e)}")
            return None
