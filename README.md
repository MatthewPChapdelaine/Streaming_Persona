# Streaming_Persona
Streaming Persona - Mathias Mindblade

## Drag-and-Drop Folder to Git Repository

This repository includes tools to quickly convert any folder into a git repository and push it to GitHub. Perfect for when you drag and drop a folder into your codespace and want to version control it immediately.

### Features

- 🚀 Quick initialization of git repositories
- 📦 Automatic GitHub repository creation
- 🔄 Smart handling of existing repositories
- 📝 Auto-generated `.gitignore` files
- 🎨 Colorful terminal output
- ✅ Support for both public and private repositories

### Prerequisites

1. **GitHub CLI (gh)**: Install from [cli.github.com](https://cli.github.com/manual/installation)
2. **Authentication**: Run `gh auth login` to authenticate with GitHub
3. **Git**: Must be installed on your system

### Usage

#### Option 1: Bash Script

```bash
# Basic usage (creates public repository with folder name)
./folder_to_repo.sh /path/to/your/folder

# Specify custom repository name
./folder_to_repo.sh /path/to/your/folder my-awesome-repo

# Create a private repository
./folder_to_repo.sh /path/to/your/folder my-awesome-repo private
```

#### Option 2: Python Script

```bash
# Basic usage (creates public repository with folder name)
python3 folder_to_repo.py /path/to/your/folder

# Specify custom repository name
python3 folder_to_repo.py /path/to/your/folder my-awesome-repo

# Create a private repository
python3 folder_to_repo.py /path/to/your/folder my-awesome-repo private
```

### Quick Start Example

1. Drag and drop a folder into your codespace
2. Open the terminal
3. Run one of these commands:

```bash
# Using bash script
./folder_to_repo.sh ./my-new-project

# Using Python script
python3 folder_to_repo.py ./my-new-project
```

That's it! Your folder is now a git repository on GitHub.

### What the Script Does

1. **Validates** the folder exists and prerequisites are met
2. **Initializes** git repository (if not already initialized)
3. **Creates** a default `.gitignore` file (if needed)
4. **Commits** all files with an initial commit message
5. **Creates** a GitHub repository with your specified settings
6. **Pushes** all content to the remote repository
7. **Opens** the repository in your browser (optional)

### Advanced Options

#### For Existing Git Repositories

If the folder is already a git repository, the script will:
- Check for an existing remote
- Stage and commit any new changes
- Push to the existing remote

#### Custom `.gitignore`

If you already have a `.gitignore` file, the script will respect it. Otherwise, it creates one with common patterns for:
- System files (`.DS_Store`, `Thumbs.db`)
- Logs and temporary files
- Node.js (`node_modules/`)
- Python (`__pycache__/`, `.venv/`)
- IDE files (`.idea/`, `.vscode/`)

### Troubleshooting

**Error: GitHub CLI is not installed**
```bash
# Install GitHub CLI first
# macOS
brew install gh

# Linux
# See: https://github.com/cli/cli/blob/trunk/docs/install_linux.md

# Windows
# See: https://github.com/cli/cli/releases
```

**Error: GitHub CLI is not authenticated**
```bash
gh auth login
# Follow the prompts to authenticate
```

**Error: Repository already exists**
- Use a different repository name
- Or delete the existing repository from GitHub first

### Examples

```bash
# Create a public repository for a Python project
./folder_to_repo.sh ~/projects/my-python-app my-python-app public

# Create a private repository for work files
python3 folder_to_repo.py ~/work/confidential-project confidential private

# Quick public repo with default name
./folder_to_repo.sh ~/Downloads/new-project
```

### License

MIT License - Feel free to use and modify as needed.
