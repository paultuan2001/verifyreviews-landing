import os
import glob
import re

NEW_AFFITOR_LINK = "https://affitor.com/join/advertiser?aff=XZmfEXV"

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original = content

    # Replace href="https://affitor.com/join/advertiser?aff=XZmfEXV" with NEW_AFFITOR_LINK
    content = re.sub(r'href=["\']https?://(?:www\.)?affitor\.com[^"\']*["\']', f'href="{NEW_AFFITOR_LINK}"', content)

    # Replace python script dict entries "cta_link": "https://affitor.com/join/advertiser?aff=XZmfEXV"
    content = re.sub(r'"cta_link":\s*["\']https?://(?:www\.)?affitor\.com[^"\']*["\']', f'"cta_link": "{NEW_AFFITOR_LINK}"', content)

    # Replace any plain "Link: https://affitor.com..." in CSV/MD/TXT notes
    content = re.sub(r'https?://(?:www\.)?affitor\.com/marketplace/referral-program[^\s,]*', NEW_AFFITOR_LINK, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")

def main():
    root_dir = "/Users/claudetest/Documents/Hệ thống kiếm tiền online/Affiliate Global"
    
    # Collect all HTML, PY, CSV, JSON, MD files
    extensions = ['*.html', '*.py', '*.csv', '*.md', '*.txt']
    files_to_check = []
    
    for root, dirs, files in os.walk(root_dir):
        # Skip .git directory
        if '.git' in root:
            continue
        for file in files:
            if any(file.endswith(ext.replace('*', '')) for ext in extensions):
                files_to_check.append(os.path.join(root, file))

    print(f"Scanning {len(files_to_check)} files for Affitor links...")
    for file_path in files_to_check:
        update_file(file_path)

if __name__ == "__main__":
    main()
