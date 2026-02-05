# Setting Up GitHub Repository

## Step 1: Install Git

If Git is not installed on your system:

1. Download Git from: https://git-scm.com/download/win
2. Run the installer with default settings
3. **Important**: Restart your terminal/command prompt after installation

## Step 2: Create GitHub Repository

1. Go to https://github.com/EpicTitan100/axilium
2. If the repository doesn't exist, create it:
   - Click "New repository" on GitHub
   - Name it `axilium`
   - Choose Public or Private
   - **Do NOT** initialize with README, .gitignore, or license
   - Click "Create repository"

## Step 3: Push Your Code

### Option A: Use the Batch Script (Windows)

1. Double-click `push_to_github.bat`
2. Follow the prompts

### Option B: Manual Commands

Open a terminal in the project folder (`C:\Users\james\axilium`) and run:

```bash
# Initialize git (if not already done)
git init

# Add remote repository
git remote add origin https://github.com/EpicTitan100/axilium.git

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Axilium habit tracker"

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Authentication

When pushing, you'll need to authenticate with GitHub. Options:

### Option 1: Personal Access Token (Recommended)

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate a new token with `repo` permissions
3. Copy the token
4. When prompted for password, paste the token instead

### Option 2: GitHub CLI

```bash
# Install GitHub CLI from https://cli.github.com/
gh auth login
```

### Option 3: SSH Key (Advanced)

1. Generate SSH key: `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. Add SSH key to GitHub: Settings → SSH and GPG keys
3. Change remote URL: `git remote set-url origin git@github.com:EpicTitan100/axilium.git`

## Troubleshooting

### "Repository not found" error
- Make sure the repository exists at https://github.com/EpicTitan100/axilium
- Verify you have write access to the repository

### Authentication failed
- Use a Personal Access Token instead of password
- Make sure the token has `repo` scope

### "Remote origin already exists"
- Update the remote: `git remote set-url origin https://github.com/EpicTitan100/axilium.git`

## After Pushing

Once pushed, your code will be available at:
**https://github.com/EpicTitan100/axilium**

You can view it, share it, and continue making changes!
