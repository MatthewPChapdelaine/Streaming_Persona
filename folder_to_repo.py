#!/usr/bin/env python3
"""
folder_to_repo.py
A Python script to initialize a git repository from a folder and push it to GitHub

Usage: python3 folder_to_repo.py <folder_path> [repo_name] [visibility]
    folder_path: Path to the folder to convert to a git repo
    repo_name: (Optional) Name for the GitHub repository (defaults to folder name)
    visibility: (Optional) Repository visibility: public or private (defaults to public)
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'  # No Color


def print_info(message):
    """Print info message in green"""
    print(f"{Colors.GREEN}[INFO]{Colors.NC} {message}")


def print_error(message):
    """Print error message in red"""
    print(f"{Colors.RED}[ERROR]{Colors.NC} {message}", file=sys.stderr)


def print_warning(message):
    """Print warning message in yellow"""
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {message}")


def run_command(cmd, capture_output=False, check=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=capture_output,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        if check:
            raise
        return e


def check_gh_installed():
    """Check if GitHub CLI is installed"""
    result = run_command("command -v gh", capture_output=True, check=False)
    return result.returncode == 0


def check_gh_authenticated():
    """Check if GitHub CLI is authenticated"""
    result = run_command("gh auth status", capture_output=True, check=False)
    return result.returncode == 0


def is_git_repo(path):
    """Check if the path is already a git repository"""
    return (Path(path) / ".git").is_dir()


def has_git_remote(remote_name="origin"):
    """Check if git repository has a remote configured"""
    result = run_command(
        f"git remote get-url {remote_name}",
        capture_output=True,
        check=False
    )
    return result.returncode == 0


def create_default_gitignore():
    """Create a default .gitignore file"""
    gitignore_content = """# Common files to ignore
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
"""
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)


def folder_to_repo(folder_path, repo_name=None, visibility="public"):
    """Convert a folder to a git repository and push to GitHub"""
    
    # Validate inputs
    folder_path = Path(folder_path).resolve()
    if not folder_path.is_dir():
        print_error(f"Folder not found: {folder_path}")
        return False
    
    if repo_name is None:
        repo_name = folder_path.name
    
    if visibility not in ["public", "private"]:
        print_error("Visibility must be 'public' or 'private'")
        return False
    
    # Check prerequisites
    if not check_gh_installed():
        print_error("GitHub CLI (gh) is not installed. Please install it first:")
        print_error("  https://cli.github.com/manual/installation")
        return False
    
    if not check_gh_authenticated():
        print_error("GitHub CLI is not authenticated. Please run: gh auth login")
        return False
    
    print_info(f"Converting folder to git repository: {folder_path}")
    print_info(f"Repository name: {repo_name}")
    print_info(f"Visibility: {visibility}")
    
    # Change to the folder
    os.chdir(folder_path)
    
    # Check if it's already a git repository
    if is_git_repo("."):
        print_warning("This folder is already a git repository")
        print_info("Checking for remote...")
        
        if has_git_remote():
            remote_url = run_command(
                "git remote get-url origin",
                capture_output=True
            ).stdout.strip()
            print_info(f"Remote already exists: {remote_url}")
            print_info("Attempting to push existing changes...")
            
            # Stage all changes
            run_command("git add -A")
            
            # Check if there are changes to commit
            # First check if HEAD exists (repository has commits)
            head_check = run_command(
                "git rev-parse HEAD",
                capture_output=True,
                check=False
            )
            
            if head_check.returncode != 0:
                # No commits yet, just commit everything
                run_command('git commit -m "Add files from drag-and-drop"')
                print_info("Changes committed")
            else:
                # Has commits, check for changes
                result = run_command(
                    "git diff-index --quiet HEAD --",
                    check=False
                )
                if result.returncode != 0:
                    run_command('git commit -m "Add files from drag-and-drop"')
                    print_info("Changes committed")
                else:
                    print_info("No changes to commit")
            
            # Try to push to remote
            push_result = run_command(
                "git push -u origin main",
                check=False
            )
            if push_result.returncode != 0:
                push_result = run_command(
                    "git push -u origin master",
                    check=False
                )
            
            if push_result.returncode != 0:
                print_error("Failed to push to remote. Please check your branch name and permissions.")
                return False
            
            print_info("Successfully pushed to existing remote!")
            return True
    else:
        # Initialize git repository
        print_info("Initializing git repository...")
        run_command("git init")
        
        # Create .gitignore if it doesn't exist
        if not Path(".gitignore").exists():
            print_info("Creating default .gitignore...")
            create_default_gitignore()
        
        # Stage all files
        print_info("Staging all files...")
        run_command("git add -A")
        
        # Create initial commit
        print_info("Creating initial commit...")
        run_command('git commit -m "Initial commit from drag-and-drop"')
        
        # Set default branch to main (after initial commit)
        run_command("git branch -M main")
    
    # At this point, we have a git repository without a remote
    # This happens in two cases:
    # 1. Folder was not a git repo (we just initialized it above)
    # 2. Folder was a git repo but had no 'origin' remote
    # Create GitHub repository and set it as the origin remote
    print_info(f"Creating GitHub repository: {repo_name}...")
    result = run_command(
        f"gh repo create {repo_name} --{visibility} --source=. --remote=origin --push",
        check=False
    )
    
    if result.returncode == 0:
        print_info("✓ Repository created and pushed successfully!")
        
        # Get the repository URL
        repo_url = run_command(
            "git remote get-url origin",
            capture_output=True
        ).stdout.strip()
        print_info(f"Repository URL: {repo_url}")
        
        # Ask to open in browser
        try:
            response = input("Would you like to open the repository in your browser? (y/n) ")
            if response.lower() in ['y', 'yes']:
                run_command("gh repo view --web")
        except (KeyboardInterrupt, EOFError):
            print()  # New line after interrupt
        
        print_info("✓ All done! Your folder is now a git repository on GitHub.")
        return True
    else:
        print_error("Failed to create GitHub repository")
        print_error("The repository might already exist. Try with a different name.")
        return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Convert a folder to a git repository and push to GitHub",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 folder_to_repo.py ./my-project
  python3 folder_to_repo.py ./my-project my-awesome-repo
  python3 folder_to_repo.py ./my-project my-awesome-repo private
        """
    )
    
    parser.add_argument(
        "folder_path",
        help="Path to the folder to convert to a git repo"
    )
    parser.add_argument(
        "repo_name",
        nargs="?",
        default=None,
        help="Name for the GitHub repository (defaults to folder name)"
    )
    parser.add_argument(
        "visibility",
        nargs="?",
        default="public",
        choices=["public", "private"],
        help="Repository visibility: public or private (default: public)"
    )
    
    args = parser.parse_args()
    
    success = folder_to_repo(args.folder_path, args.repo_name, args.visibility)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
