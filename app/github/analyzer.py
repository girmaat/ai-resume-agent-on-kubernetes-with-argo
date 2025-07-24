from llama_index.core import VectorStoreIndex
from pathlib import Path
import os
import requests
from datetime import datetime, timedelta
from collections import Counter
from .cache import RepoCache  # Import RepoCache

class RepoAnalyzer:
    def __init__(self):
        try:
            from llama_index.readers.github import GithubRepositoryReader
        except ImportError:
            from llama_index.core import download_loader
            GithubRepositoryReader = download_loader("GithubRepositoryReader")
        
        # Initialize GitHub client properly
        from github import Github
        github_client = Github(os.getenv("GITHUB_TOKEN"))
        
        self.loader = GithubRepositoryReader(
            github_client=github_client,
            owner="dummy",
            repo="dummy",
            verbose=True
        )
        self.cache = RepoCache()  # Now properly defined

    def analyze(self, repo_url: str) -> dict:
        """Main method to analyze a repo, using cache if available"""
        if cached := self.cache.get(repo_url):
            return cached

        # Extract owner and repo from the URL
        # Example: "https://github.com/owner/repo"
        parts = repo_url.split("/")
        if len(parts) < 2:
            return {"error": "Invalid repo URL"}
        owner = parts[-2]
        repo = parts[-1]

        try:
            # Fresh analysis
            documents = self.loader.load_data(branch="main", commit_sha=None, repo_url=repo_url)
            index = VectorStoreIndex.from_documents(documents)
            
            result = {
                "summary": self._generate_summary(index),
                "skills": self._extract_skills(documents),
                "commits": self._analyze_commits(repo_url)
            }
            
            self.cache.store(repo_url, result)
            return result
        except Exception as e:
            print(f"Error analyzing repo {repo_url}: {str(e)}")
            return {
                "summary": f"Error analyzing repository: {str(e)}",
                "skills": {},
                "commits": {}
            }

    def _generate_summary(self, index):
        query_engine = index.as_query_engine()
        return query_engine.query(
            "Generate a 3-paragraph technical summary of this repository"
        ).response

    def _extract_skills(self, documents) -> dict:
        """Updated to include AWS detection"""
        filenames = [d.metadata.get("file_name", "").lower() for d in documents]
        content = " ".join(d.text for d in documents)
        
        return {
            "languages": self._map_extensions(documents),
            "devops": self._detect_devops(filenames, content),
            "ai_components": self._detect_ai_tech(filenames, content),
            "aws_resources": self._detect_aws_resources(filenames, content),
            "frameworks": self._detect_frameworks(filenames)
        }

    def _detect_devops(self, filenames: list, content: str) -> list:
        """Explicit DevOps tool detection"""
        devops_indicators = {
            # File-based detection
            'dockerfile': 'Docker',
            'kubernetes': 'Kubernetes',
            'argo': 'ArgoCD',
            'helm': 'Helm',
            'terraform': 'Terraform',
            'github-actions': 'GitHub Actions',
            
            # Content patterns
            'apiVersion: apps/v1': 'Kubernetes',
            'image: ': 'Docker',
            'helm install': 'Helm'
        }
        
        detected = set()
        for filename in filenames:
            for term, tool in devops_indicators.items():
                if term in filename:
                    detected.add(tool)
        
        # Additional content scanning
        for term, tool in devops_indicators.items():
            if term in content.lower():
                detected.add(tool)
                
        return sorted(detected)

    def _detect_ai_tech(self, filenames: list, content: str) -> list:
        """Explicit AI/ML technology detection"""
        ai_indicators = {
            # Framework files
            'requirements.txt': self._scan_ai_dependencies,
            'pytorch': 'PyTorch',
            'tensorflow': 'TensorFlow',
            'transformers': 'HuggingFace',
            
            # Content patterns
            'from langchain': 'LangChain',
            'openai': 'OpenAI',
            'llama-index': 'LlamaIndex',
            'model.fit(': 'Scikit-learn/TensorFlow',
            'AutoModelFor': 'HuggingFace'
        }
        
        detected = set()
        for filename in filenames:
            if 'requirements.txt' in filename:
                detected.update(self._scan_ai_dependencies(content))
                
            for term, tool in ai_indicators.items():
                if callable(tool):
                    continue
                if term in filename:
                    detected.add(tool)
        
        # Deep content scan
        for term, tool in ai_indicators.items():
            if callable(tool):
                continue
            if term in content.lower():
                detected.add(tool)
                
        return sorted(detected)

    def _detect_aws_resources(self, filenames: list, content: str) -> list:
        """Flags AWS services using file patterns and content signatures"""
        aws_indicators = {
            # Infrastructure-as-Code files
            'serverless.yml': 'AWS Lambda',
            'template.yaml': 'AWS CloudFormation',
            'cdk.json': 'AWS CDK',
            
            # SDK/CLI patterns
            'boto3': 'AWS SDK (Python)',
            'aws-sdk': 'AWS SDK',
            'aws configure': 'AWS CLI',
            
            # Service-specific identifiers
            's3://': 'Amazon S3',
            'arn:aws:lambda': 'AWS Lambda',
            'arn:aws:s3': 'Amazon S3',
            'arn:aws:ec2': 'Amazon EC2',
            'dynamodb.Table': 'Amazon DynamoDB',
            'sns.publish': 'Amazon SNS',
            'sqs.send_message': 'Amazon SQS',
            'rds.amazonaws.com': 'Amazon RDS',
            'secretsmanager': 'AWS Secrets Manager'
        }
        
        detected = set()
        
        # 1. Filename detection
        for filename in filenames:
            for term, service in aws_indicators.items():
                if term in filename:
                    detected.add(service)
        
        # 2. Deep content scanning
        content_lower = content.lower()
        for term, service in aws_indicators.items():
            if term in content_lower:
                detected.add(service)
        
        # 3. Terraform-specific detection
        if any(f.endswith('.tf') for f in filenames):
            tf_services = {
                'aws_instance': 'Amazon EC2',
                'aws_lambda_function': 'AWS Lambda',
                'aws_s3_bucket': 'Amazon S3',
                'aws_rds_cluster': 'Amazon RDS'
            }
            for term, service in tf_services.items():
                if term in content_lower:
                    detected.add(service)
        
        return sorted(detected)

    def _scan_ai_dependencies(self, content: str) -> list:
        """Parse requirements.txt for AI libraries"""
        ai_packages = {
            'torch': 'PyTorch',
            'tensorflow': 'TensorFlow',
            'transformers': 'HuggingFace',
            'openai': 'OpenAI',
            'langchain': 'LangChain',
            'llama-index': 'LlamaIndex',
            'sentence-transformers': 'Sentence Transformers'
        }
        
        found = set()
        for line in content.split('\n'):
            line = line.split('#')[0].strip().lower()
            for pkg, name in ai_packages.items():
                if pkg in line:
                    found.add(name)
        return sorted(found)

    def _map_extensions(self, documents) -> list:
        """Map file extensions to languages"""
        extension_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.go': 'Go',
            '.rs': 'Rust',
            '.md': 'Markdown',
            '.yml': 'YAML',
            '.yaml': 'YAML'
        }
        extensions = set()
        for doc in documents:
            file_name = doc.metadata.get("file_name", "")
            ext = Path(file_name).suffix
            if ext:
                extensions.add(ext)
        return sorted({
            extension_map[ext] for ext in extensions 
            if ext in extension_map
        })

    def _detect_frameworks(self, filenames: list) -> list:
        """Detect frameworks from filenames"""
        framework_hints = {
            'requirements.txt': 'Python',
            'package.json': 'Node.js',
            'go.mod': 'Go',
            'Cargo.toml': 'Rust',
            'dockerfile': 'Docker',
            'config.ru': 'Ruby on Rails'
        }
        
        detected = set()
        for filename in filenames:
            for hint, framework in framework_hints.items():
                if hint in filename:
                    detected.add(framework)
        return sorted(detected)

    def _analyze_commits(self, repo_url: str) -> dict:
        """Basic commit message analysis"""
        repo_path = repo_url.split("github.com/")[-1]
        commits_url = f"https://api.github.com/repos/{repo_path}/commits"
        
        try:
            response = requests.get(
                commits_url,
                headers={"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"},
                params={"per_page": 100}  # Analyze last 100 commits
            )
            commits = response.json()
            
            return {
                "recent_activity": self._get_activity_stats(commits),
                "common_patterns": self._get_commit_patterns(commits)
            }
        except Exception as e:
            print(f"Commit analysis failed: {str(e)}")
            return {}

    def _get_activity_stats(self, commits) -> dict:
        """Calculate commit frequency stats"""
        if not commits:
            return {}
            
        last_week = datetime.now() - timedelta(days=7)
        recent = [c for c in commits 
                 if datetime.strptime(c['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ') > last_week]
        
        return {
            "last_commit": commits[0]['commit']['author']['date'],
            "commits_last_week": len(recent),
            "avg_commits_per_week": len(commits) // 4  # Approximate for 1 month
        }

    def _get_commit_patterns(self, commits) -> list:
        """Identify common commit message prefixes"""
        prefixes = Counter()
        for commit in commits:
            msg = commit['commit']['message'].lower()
            if ':' in msg:
                prefix = msg.split(':')[0].strip()
                prefixes[prefix] += 1
        return prefixes.most_common(3)
