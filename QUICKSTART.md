# Quick Start Guide: Drag-and-Drop Folder to GitHub

## What This Tool Does

When you drag and drop a folder into your codespace, this tool will:
1. Initialize it as a git repository
2. Create a new repository on GitHub
3. Push all your files to GitHub

All in one command!

## Setup (One-Time)

### 1. Install GitHub CLI

**Already installed in most codespaces!** If not:

- **macOS**: `brew install gh`
- **Linux/Codespace**: Usually pre-installed
- **Windows**: Download from [cli.github.com](https://cli.github.com/)

### 2. Authenticate with GitHub

```bash
gh auth login
```

Follow the prompts to authenticate.

## Usage

### Super Quick Method

After dragging a folder into your codespace:

```bash
./folder_to_repo.sh ./your-folder-name
```

Done! Your folder is now on GitHub.

### With Custom Settings

```bash
# Custom repository name
./folder_to_repo.sh ./folder-name my-cool-repo

# Private repository
./folder_to_repo.sh ./folder-name my-cool-repo private
```

## Common Scenarios

### Scenario 1: New Project Folder

You have a new project folder with code you want to backup:

```bash
./folder_to_repo.sh ~/Downloads/my-new-app
```

### Scenario 2: Existing Work That Needs GitHub

You've been working on something locally and now want it on GitHub:

```bash
python3 folder_to_repo.py ~/projects/my-work my-work-backup
```

### Scenario 3: Private/Confidential Code

```bash
./folder_to_repo.sh ~/confidential company-internal private
```

## Parameters Explained

```bash
./folder_to_repo.sh <folder> [repo-name] [visibility]
```

1. **folder** (required): Path to your folder
2. **repo-name** (optional): Name on GitHub (defaults to folder name)
3. **visibility** (optional): `public` or `private` (defaults to public)

## Choosing Bash vs Python

Both scripts do the same thing:

- **Use Bash** (`folder_to_repo.sh`) if:
  - You prefer shell scripts
  - You're on Linux/macOS
  
- **Use Python** (`folder_to_repo.py`) if:
  - You prefer Python
  - You want better error messages
  - You're on Windows (works better)

## What Gets Committed

Everything in your folder EXCEPT:
- `.DS_Store` and system files
- `node_modules/`
- Python virtual environments
- `.env` files
- Log files
- IDE settings

(See the auto-generated `.gitignore` file)

## Troubleshooting

### "gh: command not found"

Install GitHub CLI:
```bash
# Check if available
gh --version

# Install if needed
brew install gh  # macOS
```

### "not authenticated"

Run:
```bash
gh auth login
```

### "repository already exists"

Choose a different name:
```bash
./folder_to_repo.sh ./my-folder different-name
```

Or delete the existing repo on GitHub first.

## Tips

💡 **Tip 1**: The folder name becomes the repo name by default
💡 **Tip 2**: You can run this on folders that are already git repos
💡 **Tip 3**: The script won't overwrite existing remotes
💡 **Tip 4**: All your files are committed in one batch

## Need Help?

1. Check the main [README.md](README.md) for detailed documentation
2. Run the script without arguments to see usage
3. Check GitHub CLI status: `gh auth status`

## Example Workflow

```bash
# 1. You drag "my-app" folder into codespace
# 2. Open terminal
# 3. Run:
./folder_to_repo.sh ./my-app

# 4. Script asks if you want to open in browser
# 5. Your code is now on GitHub!
```

That's it! Happy coding! 🚀
