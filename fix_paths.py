import os
import re
from bs4 import BeautifulSoup

# Directory containing your exported HTML files
PROJECT_DIR = "./"  # Change to your static site folder path if different

# Your GitHub repo name if deploying to username.github.io/repo-name/
# Set REPO_NAME = "" if using a custom domain or username.github.io root
REPO_NAME = "hccf.github.io" 

def fix_paths_in_html(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    modified = False

    # Attributes that typically hold URLs to local assets or pages
    url_attributes = {
        "a": "href",
        "link": "href",
        "script": "src",
        "img": "src",
        "source": "srcset",
    }

    for tag_name, attr in url_attributes.items():
        for tag in soup.find_all(tag_name):
            val = tag.get(attr)
            if not val:
                continue

            # Case 1: Fix leading slash absolute paths (e.g., /wp-content/...)
            if val.startswith("/") and not val.startswith("//"):
                if REPO_NAME:
                    # Strip existing leading slash and attach repo name prefix
                    clean_path = val.lstrip("/")
                    new_val = f"/{REPO_NAME}/{clean_path}"
                else:
                    # Convert to relative path
                    new_val = f".{val}"

                tag[attr] = new_val
                modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Fixed paths in: {file_path}")

def run():
    print("Starting path conversion...")
    for root, _, files in os.walk(PROJECT_DIR):
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                fix_paths_in_html(full_path)
    print("Path conversion complete.")

if __name__ == "__main__":
    run()