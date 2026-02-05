@echo off
echo ========================================
echo Axilium - Push to GitHub
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo After installation, restart your terminal and run this script again.
    pause
    exit /b 1
)

echo Git is installed. Continuing...
echo.

REM Navigate to project directory
cd /d "%~dp0"

REM Initialize git if not already initialized
if not exist .git (
    echo Initializing git repository...
    git init
    echo.
)

REM Check if remote already exists
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo Adding GitHub remote...
    git remote add origin https://github.com/EpicTitan100/axilium.git
) else (
    echo Remote already exists. Updating...
    git remote set-url origin https://github.com/EpicTitan100/axilium.git
)

echo.
echo Adding all files...
git add .

echo.
echo Committing changes...
git commit -m "Initial commit: Axilium habit tracker"

echo.
echo Pushing to GitHub...
echo Note: You may be prompted for GitHub credentials.
echo.
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ERROR: Push failed!
    echo.
    echo Possible reasons:
    echo 1. You need to authenticate with GitHub
    echo 2. The repository doesn't exist yet (create it at https://github.com/EpicTitan100/axilium)
    echo 3. You don't have write access to the repository
    echo.
    echo For authentication, you can use:
    echo - GitHub Personal Access Token (recommended)
    echo - GitHub CLI (gh auth login)
    echo.
) else (
    echo.
    echo ========================================
    echo Success! Code pushed to GitHub!
    echo ========================================
    echo Repository: https://github.com/EpicTitan100/axilium
    echo.
)

pause
