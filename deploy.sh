#!/bin/bash
# Auto-deploy script for VerifyReviews (Affiliate Global)

echo "=================================================="
echo "🚀 AUTO-DEPLOYING VERIFYREVIEWS TO GITHUB PAGES..."
echo "=================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "⚠️ Git repository not initialized yet."
    echo "Please link your GitHub repo first by running:"
    echo "  git init"
    echo "  git remote add origin YOUR_GITHUB_REPO_URL"
    echo "  git branch -M main"
    exit 1
fi

# Add all changed and new files
git add .

# Commit with timestamp
git commit -m "Auto update website content: $(date '+%Y-%m-%d %H:%M:%S')"

# Push to main branch
git push origin main

echo "=================================================="
echo "✅ SUCCESS! Deployed to GitHub & verifyreviews.net!"
echo "=================================================="
