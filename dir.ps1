# Set root directory path (update this to match your actual path)
$root = "C:\Personal Folder\AI Studies\AI Projects\LLM-KM\ai-resume-agent-on-kubernetes-with-argo"

Set-Location -Path $root

# Define all folders to create (recursive structure)
$folders = @(
    "services/assistant-service/app",
    "services/assistant-service/tests",
    "services/resume-parser-service/app",
    "services/resume-parser-service/resumes",
    "services/notification-service/app",
    "services/logging-service/app",
    "services/tools-service/app",
    "services/api-gateway/app",

    "ui/gradio-ui/static",
    "ui/react-ui",

    "database",
    "shared/schemas",
    "shared/config",

    "monitoring/prometheus",
    "monitoring/grafana/dashboards",
    "monitoring/grafana/datasources",
    "monitoring/loki",

    "k8s",
    "helm/assistant-service",
    "helm/notification-service",

    "argocd/applications",
    "argocd/projects",

    "argo-workflows"
)

# Create folders
foreach ($folder in $folders) {
    $fullPath = Join-Path $root $folder
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
    }
}

# Create top-level files
$files = @(
    ".env.example",
    "README.md",
    "requirements.txt",
    "docker-compose.yaml"
)

foreach ($file in $files) {
    $filePath = Join-Path $root $file
    if (-not (Test-Path $filePath)) {
        New-Item -ItemType File -Path $filePath | Out-Null
    }
}

# Create .gitignore with common rules
$gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
*.egg
*.egg-info/
dist/
build/
.venv/
.env

# OS
.DS_Store

# VSCode
.vscode/

# Logs
*.log

# Others
*.sqlite
"@
$gitignorePath = Join-Path $root ".gitignore"
$gitignoreContent | Set-Content -Path $gitignorePath

# Initialize Git
if (-not (Test-Path (Join-Path $root ".git"))) {
    git init
}

# Add remote repo if not added already
$remoteExists = git remote get-url origin 2>$null
if (-not $remoteExists) {
    git remote add origin https://github.com/girmaat/ai-resume-agent-on-kubernetes-with-argo.git
}

# Git add, commit
git add .
git commit -m "Scaffold full project directory structure"
