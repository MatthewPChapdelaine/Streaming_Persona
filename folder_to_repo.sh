#!/bin/bash

# folder_to_repo.sh
# This script initializes a git repository from a folder and pushes it to GitHub
#
# Usage: ./folder_to_repo.sh <folder_path> [repo_name] [visibility]
#   folder_path: Path to the folder to convert to a git repo
#   repo_name: (Optional) Name for the GitHub repository (defaults to folder name)
#   visibility: (Optional) Repository visibility: public or private (defaults to public)

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    print_error "GitHub CLI (gh) is not installed. Please install it first:"
    print_error "  https://cli.github.com/manual/installation"
    exit 1
fi

# Check if gh is authenticated
if ! gh auth status &> /dev/null; then
    print_error "GitHub CLI is not authenticated. Please run: gh auth login"
    exit 1
fi

# Check if folder path is provided
if [ -z "$1" ]; then
    print_error "Usage: $0 <folder_path> [repo_name] [visibility]"
    print_error "Example: $0 ./my-project my-awesome-repo public"
    exit 1
fi

FOLDER_PATH="$1"
REPO_NAME="${2:-$(basename "$FOLDER_PATH")}"
VISIBILITY="${3:-public}"

# Validate folder exists
if [ ! -d "$FOLDER_PATH" ]; then
    print_error "Folder not found: $FOLDER_PATH"
    exit 1
fi

# Validate visibility option
if [ "$VISIBILITY" != "public" ] && [ "$VISIBILITY" != "private" ]; then
    print_error "Visibility must be 'public' or 'private'"
    exit 1
fi

print_info "Converting folder to git repository: $FOLDER_PATH"
print_info "Repository name: $REPO_NAME"
print_info "Visibility: $VISIBILITY"

# Change to the folder
cd "$FOLDER_PATH"

# Check if it's already a git repository
if [ -d ".git" ]; then
    print_warning "This folder is already a git repository"
    print_info "Checking for remote..."
    
    if git remote get-url origin &> /dev/null; then
        REMOTE_URL=$(git remote get-url origin)
        print_info "Remote already exists: $REMOTE_URL"
        print_info "Attempting to push existing changes..."
        
        # Stage all changes
        git add -A
        
        # Check if there are changes to commit
        # First check if HEAD exists (repository has commits)
        if ! git rev-parse HEAD &> /dev/null; then
            # No commits yet, just commit everything
            git commit -m "Add files from drag-and-drop"
            print_info "Changes committed"
        elif ! git diff-index --quiet HEAD --; then
            # Has commits, check for changes
            git commit -m "Add files from drag-and-drop"
            print_info "Changes committed"
        else
            print_info "No changes to commit"
        fi
        
        # Push to remote
        git push -u origin main || git push -u origin master || {
            print_error "Failed to push to remote. Please check your branch name and permissions."
            exit 1
        }
        
        print_info "Successfully pushed to existing remote!"
        exit 0
    fi
else
    # Initialize git repository
    print_info "Initializing git repository..."
    git init
    
    # Set default branch to main
    git branch -M main
    
    # Create .gitignore if it doesn't exist
    if [ ! -f ".gitignore" ]; then
        print_info "Creating default .gitignore..."
        cat > .gitignore << 'EOF'
# Common files to ignore
.DS_Store
Thumbs.db
*.log
*.tmp
node_modules/
.env
.venv/
venv/
__pycache__/
*.pyc
.idea/
.vscode/
*.swp
*.swo
*~
EOF
    fi
    
    # Stage all files
    print_info "Staging all files..."
    git add -A
    
    # Create initial commit
    print_info "Creating initial commit..."
    git commit -m "Initial commit from drag-and-drop"
fi

# Create GitHub repository
print_info "Creating GitHub repository: $REPO_NAME..."
if gh repo create "$REPO_NAME" --$VISIBILITY --source=. --remote=origin --push; then
    print_info "✓ Repository created and pushed successfully!"
    
    # Get the repository URL
    REPO_URL=$(git remote get-url origin)
    print_info "Repository URL: $REPO_URL"
    
    # Open the repository in browser (optional)
    read -p "Would you like to open the repository in your browser? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        gh repo view --web
    fi
else
    print_error "Failed to create GitHub repository"
    print_error "The repository might already exist. Try with a different name."
    exit 1
fi

print_info "✓ All done! Your folder is now a git repository on GitHub."
