# GitHub Setup Instructions

## ✅ Completed
- Git repository initialized
- Files committed locally
- .gitignore created to protect sensitive files

## Next Steps: Push to GitHub

### Option 1: Create New Repository on GitHub

1. Go to https://github.com/new
2. Create a new repository (e.g., `ai-agents-day5`)
3. **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Copy the repository URL (e.g., `https://github.com/yourusername/ai-agents-day5.git`)

### Option 2: Use Existing Repository

If you already have a GitHub repository, use its URL.

### Push to GitHub

Run these commands (replace with your repository URL):

```powershell
cd "C:\AI Agents\Day5"

# Add remote (replace with your GitHub repository URL)
git remote add origin https://github.com/yourusername/your-repo-name.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### If You Need to Authenticate

- **Personal Access Token**: GitHub requires a Personal Access Token instead of password
- Create one at: https://github.com/settings/tokens
- Use the token as your password when prompted

## Files Protected by .gitignore

The following files are **NOT** committed (protected):
- `.env` files (contains secrets)
- `*.json` service account keys
- `.venv/` virtual environment
- `__pycache__/` Python cache
- Temporary files

## What Was Committed

✅ `.gitignore` - Protects sensitive files
✅ `sample_agent/agent.py` - Your agent code
✅ `sample_agent/retrieveAgent.py` - Script to query deployed agent
✅ `sample_agent/requirements.txt` - Dependencies
✅ `sample_agent/*.md` - Documentation files
✅ `sample_agent/.gitignore` - Additional protection

