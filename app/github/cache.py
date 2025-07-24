import sqlite3
import json
import os
from typing import Optional, Dict, Any
from pathlib import Path
from datetime import datetime, timedelta


class RepoCache:
    def __init__(self):
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = int(os.getenv("GITHUB_CACHE_TTL", "3600"))  # Default 1 hour
        
    def get(self, repo_url: str) -> Optional[Dict[str, Any]]:
        """Get cached data with TTL validation"""
        cached_data = self._get_from_source(repo_url)
        if cached_data and not self._is_expired(cached_data):
            return cached_data["data"]
        return None

    def store(self, repo_url: str, data: Dict[str, Any]):
        """Store data with timestamp"""
        cache_item = {
            "data": data,
            "cached_at": datetime.utcnow().isoformat()
        }
        if self._db_exists():
            self._store_db(repo_url, cache_item)
        else:
            self._store_local(repo_url, cache_item)

    def _get_from_source(self, repo_url: str) -> Optional[Dict[str, Any]]:
        """Unified cache retrieval"""
        if self._db_exists():
            return self._query_db(repo_url)
        return self._load_local(repo_url)

    def _is_expired(self, cache_item: Dict[str, Any]) -> bool:
        """Check if cached item has expired"""
        if not cache_item or "cached_at" not in cache_item:
            return True
            
        cached_time = datetime.fromisoformat(cache_item["cached_at"])
        return (datetime.utcnow() - cached_time) > timedelta(seconds=self.ttl)

    def _db_exists(self) -> bool:
        return os.path.exists("repos.db")

    def _query_db(self, repo_url: str) -> Optional[Dict[str, Any]]:
        try:
            conn = sqlite3.connect("repos.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT data FROM repos 
                WHERE url = ?
            """, (repo_url,))
            result = cursor.fetchone()
            conn.close()
            return json.loads(result[0]) if result else None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def _store_db(self, repo_url: str, data: Dict[str, Any]):
        try:
            conn = sqlite3.connect("repos.db")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS repos (
                    url TEXT PRIMARY KEY,
                    data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute(
                "INSERT OR REPLACE INTO repos (url, data) VALUES (?, ?)",
                (repo_url, json.dumps(data))
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Failed to store in database: {e}")
            self._store_local(repo_url, data)  # Fallback

    def _load_local(self, repo_url: str) -> Optional[Dict[str, Any]]:
        cache_file = self.cache_dir / f"{self._sanitize_url(repo_url)}.json"
        try:
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Local cache error: {e}")
        return None
        
    def _store_local(self, repo_url: str, data: Dict[str, Any]):
        cache_file = self.cache_dir / f"{self._sanitize_url(repo_url)}.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f)
        except IOError as e:
            print(f"Failed to store locally: {e}")

    def _sanitize_url(self, repo_url: str) -> str:
        """Make repo URL filesystem-safe"""
        return repo_url.replace('/', '_').replace(':', '-')
