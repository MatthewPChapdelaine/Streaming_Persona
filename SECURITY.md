# Security Considerations

## Overview

The folder-to-repo scripts help you quickly push local folders to GitHub. However, it's important to understand the security implications and best practices.

## ⚠️ Important Security Warnings

### 1. Review Before You Push

**ALWAYS** review the contents of a folder before running these scripts:

```bash
# Review folder contents first
ls -la ./my-folder
cat ./my-folder/.env  # Check for secrets!
```

**Common files to look for:**
- `.env` files with API keys or passwords
- Configuration files with credentials
- Private keys (`.pem`, `.key`, `.p12`)
- Database connection strings
- OAuth tokens
- SSH keys

### 2. Automatic .gitignore

The scripts create a default `.gitignore` that excludes:
- `.env` files
- Common credential patterns
- System files

**However**, this is NOT foolproof. Always manually verify.

### 3. Public vs Private

```bash
# Public repository - anyone can see
./folder_to_repo.sh ./my-folder my-repo public

# Private repository - only you and collaborators
./folder_to_repo.sh ./my-folder my-repo private
```

**Remember**: 
- Public repos are visible to the entire internet
- Even deleted commits can be recovered from forks
- Once published publicly, consider all secrets compromised

### 4. Existing Git Repositories

If the folder is already a git repo, the script:
- Preserves existing remotes
- Commits all changes
- Pushes to the existing remote

**Risk**: You might accidentally push to the wrong remote!

**Recommendation**: Check remotes first:
```bash
cd ./my-folder
git remote -v
```

## Best Practices

### Before Running the Script

1. **Scan for secrets**:
   ```bash
   # Check for common secret patterns
   grep -r "password" ./my-folder
   grep -r "api_key" ./my-folder
   grep -r "secret" ./my-folder
   ```

2. **Review .env files**:
   ```bash
   find ./my-folder -name ".env*" -o -name "*credentials*"
   ```

3. **Check for large files**:
   ```bash
   find ./my-folder -type f -size +50M
   ```

### After Running the Script

1. **Review the first commit**:
   ```bash
   cd ./my-folder
   git log -1 -p
   ```

2. **Check what was pushed**:
   ```bash
   gh repo view --web
   # Manually review files on GitHub
   ```

3. **Enable secret scanning** (for private repos with GitHub Advanced Security):
   - Go to repository Settings → Security
   - Enable "Secret scanning"

### For Sensitive Projects

1. **Use private repositories**:
   ```bash
   ./folder_to_repo.sh ./confidential my-repo private
   ```

2. **Add comprehensive .gitignore BEFORE running**:
   ```bash
   cd ./my-folder
   # Create detailed .gitignore
   echo "secrets/" >> .gitignore
   echo "*.key" >> .gitignore
   echo "credentials.json" >> .gitignore
   # Then run the script
   cd ..
   ./folder_to_repo.sh ./my-folder
   ```

3. **Use environment-specific configs**:
   ```bash
   # Instead of committing secrets
   # Use template files
   cp .env .env.template
   # Edit .env.template to remove secrets
   # Add .env to .gitignore
   ```

## What Gets Excluded by Default

The auto-generated `.gitignore` excludes:

```
# System files
.DS_Store
Thumbs.db

# Logs
*.log
*.tmp

# Environment variables
.env

# Dependencies
node_modules/
venv/
.venv/
__pycache__/

# IDE files
.idea/
.vscode/
*.swp
*.swo
```

## What Does NOT Get Excluded

These are **NOT** automatically excluded and may contain secrets:

- `config.json` or `config.yaml`
- `.aws/credentials`
- `.ssh/id_rsa`
- `database.yml`
- `.npmrc` (may contain auth tokens)
- `.pypirc`
- Custom configuration files

**Action Required**: Add these to `.gitignore` manually if present!

## If You Accidentally Commit Secrets

### Immediate Actions

1. **Revoke the secret immediately**:
   - Change passwords
   - Rotate API keys
   - Revoke OAuth tokens

2. **For private repos**, consider if the secret was compromised:
   - Who has access to the repo?
   - Was it briefly public?

3. **Remove the secret from git history** (advanced):
   ```bash
   # Use git filter-repo (recommended)
   pip install git-filter-repo
   git filter-repo --invert-paths --path secrets.txt
   
   # Or use BFG Repo-Cleaner
   # https://rtyley.github.io/bfg-repo-cleaner/
   ```

4. **Force push** (if you're the only user):
   ```bash
   git push --force-with-lease
   ```

**Warning**: Force pushing can cause issues for collaborators!

### Long-term Prevention

1. **Use secret managers**:
   - GitHub Secrets for Actions
   - AWS Secrets Manager
   - HashiCorp Vault
   - Azure Key Vault

2. **Use pre-commit hooks**:
   ```bash
   pip install pre-commit detect-secrets
   # Setup hooks to scan for secrets before commit
   ```

3. **Enable GitHub's secret scanning**

## Repository Visibility Changes

You can change visibility after creation:

```bash
# Make private
gh repo edit owner/repo --visibility private

# Make public (be careful!)
gh repo edit owner/repo --visibility public
```

**Note**: Making a repository public cannot undo previous privacy!

## GitHub CLI Authentication

The scripts require GitHub CLI authentication:

```bash
gh auth login
```

**Security notes**:
- Uses OAuth tokens, not passwords
- Tokens are stored securely by `gh`
- Can be revoked at any time
- Scoped permissions

**To logout**:
```bash
gh auth logout
```

## Codespaces Specific

When using in GitHub Codespaces:

1. **Automatic authentication**: Codespaces may auto-authenticate `gh`
2. **Shared environments**: Don't use in shared/public codespaces
3. **Temporary environments**: Codespaces are ephemeral but commits are permanent

## Audit Trail

All git operations create an audit trail:

- Commits show author and timestamp
- GitHub logs all pushes
- Repository activity is logged

**This is good for security but means:**
- You can't "undo" a public push completely
- Commits are permanent records

## Compliance Considerations

For regulated industries:

1. **Data residency**: Check where GitHub stores data
2. **Access controls**: Use private repos with strict access
3. **Audit logs**: Enable GitHub Advanced Security
4. **Encryption**: GitHub encrypts data at rest and in transit

## Additional Resources

- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [.gitignore templates](https://github.com/github/gitignore)
- [git-filter-repo](https://github.com/newren/git-filter-repo)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

## Checklist Before Using These Scripts

- [ ] I have reviewed all files in the folder
- [ ] I have checked for `.env` files and secrets
- [ ] I have verified no credentials are present
- [ ] I have checked for large binary files
- [ ] I have chosen appropriate visibility (public/private)
- [ ] I understand that public repos are visible to everyone
- [ ] I have a backup of important data
- [ ] I am using the correct GitHub account

## Summary

✅ **DO**:
- Review folder contents before pushing
- Use private repos for sensitive data
- Add comprehensive .gitignore files
- Revoke secrets if accidentally committed
- Use secret managers for credentials

❌ **DON'T**:
- Push without reviewing contents
- Assume .gitignore catches everything
- Commit API keys, passwords, or tokens
- Make repos public without careful review
- Store production secrets in git

---

**When in doubt, use `private` visibility and review carefully!**
