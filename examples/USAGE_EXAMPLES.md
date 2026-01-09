# Usage Examples

## Example 1: Simple Public Repository

You downloaded a folder of code samples and want to put it on GitHub:

```bash
# Navigate to your workspace
cd ~/workspace

# Drag and drop folder "code-samples" into codespace
# Then run:
./folder_to_repo.sh ./code-samples
```

**Result**: Creates a public repository named "code-samples" with all files.

---

## Example 2: Custom Repository Name

You have a folder named "my-stuff" but want a better repository name:

```bash
./folder_to_repo.sh ./my-stuff awesome-project
```

**Result**: Creates a public repository named "awesome-project".

---

## Example 3: Private Repository

You have confidential code that should be private:

```bash
python3 folder_to_repo.py ./confidential-code private-project private
```

**Result**: Creates a private repository named "private-project".

---

## Example 4: Updating Existing Repository

You already ran the script once, made changes, and want to push updates:

```bash
# Make some changes to files in the folder
echo "new content" >> ./my-project/newfile.txt

# Run the script again
./folder_to_repo.sh ./my-project
```

**Result**: Detects existing repository, commits new changes, and pushes to GitHub.

---

## Example 5: Work in Progress Project

You've been working on a project locally and want to back it up:

```bash
cd ~/projects/work-in-progress
# Folder already has code but no git

# Run from parent directory
cd ..
./folder_to_repo.sh ./work-in-progress wip-backup private
```

**Result**: Initializes git, creates private repo "wip-backup", pushes all files.

---

## Example 6: Quick Backup

You have a folder with important files and want a quick backup:

```bash
./folder_to_repo.sh ~/Documents/important-files important-backup private
```

**Result**: Private repository with all your important files backed up.

---

## Example 7: Python Project

A Python project with dependencies:

```bash
# Your folder structure:
# my-python-app/
# ├── main.py
# ├── requirements.txt
# └── tests/

./folder_to_repo.sh ./my-python-app my-python-app public
```

**Result**: Public repository with auto-generated `.gitignore` excluding `__pycache__`, `.venv`, etc.

---

## Example 8: Web Project

A web project with node_modules:

```bash
# Your folder structure:
# my-web-app/
# ├── index.html
# ├── package.json
# └── node_modules/

python3 folder_to_repo.py ./my-web-app my-web-app
```

**Result**: Public repository with `.gitignore` excluding `node_modules/`.

---

## Example 9: Multiple Folders at Once

Process multiple folders:

```bash
# Create a simple script
for folder in ./project1 ./project2 ./project3; do
  ./folder_to_repo.sh "$folder"
  sleep 2  # Brief pause between operations
done
```

**Result**: Three separate repositories, each named after their folder.

---

## Example 10: From Downloads

You downloaded a project archive and extracted it:

```bash
cd ~/Downloads
unzip project.zip
./folder_to_repo.sh ./project my-fork-of-project
```

**Result**: Your own repository based on the downloaded project.

---

## Advanced Examples

### With Custom Commit Message

The scripts use default commit messages. To customize:

```bash
# After the script runs, you can amend the commit
./folder_to_repo.sh ./my-project
cd ./my-project
git commit --amend -m "Your custom commit message"
git push -f
```

### Selective File Addition

If you want to exclude certain files before creating the repo:

```bash
cd ./my-project

# Create/edit .gitignore first
echo "secrets.txt" >> .gitignore
echo "*.backup" >> .gitignore

# Then run the script
cd ..
./folder_to_repo.sh ./my-project
```

### Organization Repository

To create a repository under an organization:

```bash
# The gh CLI will prompt you to choose personal or organization
# Or specify it in the repo name:
./folder_to_repo.sh ./my-project my-org/my-project
```

---

## Troubleshooting Examples

### Example: Repository Name Conflict

```bash
$ ./folder_to_repo.sh ./my-project
[ERROR] Failed to create GitHub repository
[ERROR] The repository might already exist. Try with a different name.

# Solution: Use a different name
$ ./folder_to_repo.sh ./my-project my-project-v2
```

### Example: Permission Issues

```bash
$ ./folder_to_repo.sh ./locked-folder
[ERROR] Folder not found: ./locked-folder

# Solution: Check permissions and path
$ ls -la ./locked-folder
$ chmod +r ./locked-folder
```

### Example: Large Files Warning

If you have large files (>100MB), git will warn you:

```bash
# Before running the script, use git-lfs
cd ./my-project
git lfs install
git lfs track "*.psd"
git lfs track "*.zip"

# Then run the script
cd ..
./folder_to_repo.sh ./my-project
```

---

## Tips for Success

1. **Check folder contents first**: Make sure there are no sensitive files
2. **Review .gitignore**: The auto-generated one covers common cases but might need tweaks
3. **Choose visibility carefully**: Public vs private - you can change this later on GitHub
4. **Use meaningful names**: Future-you will thank you for good repository names
5. **Test with small folders first**: Get comfortable with the tool before using on important projects

---

## Common Workflows

### Daily Backup Workflow

```bash
#!/bin/bash
# save as: daily-backup.sh

DATE=$(date +%Y%m%d)
./folder_to_repo.sh ~/work/current-project "project-backup-$DATE" private
```

### Code Sharing Workflow

```bash
# Quick way to share code with colleagues
./folder_to_repo.sh ./code-to-share temp-share-$(date +%s) public
# Share the GitHub URL with your team
```

### Archive Workflow

```bash
# Archive old projects
for project in ~/old-projects/*; do
  if [ -d "$project" ]; then
    name=$(basename "$project")
    ./folder_to_repo.sh "$project" "archive-$name" private
  fi
done
```
