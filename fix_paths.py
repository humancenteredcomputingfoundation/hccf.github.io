import os
import warnings
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# Set this to your exact GitHub repository name
REPO_NAME = "hccf.github.io"  # e.g., "hccf-site" or "website"

PROJECT_DIR = "./"

def fix_paths_in_html(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    modified = False

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

            # Case A: Path starts with leading slash (e.g., /wp-content/...)
            if val.startswith("/") and not val.startswith("//"):
                if not val.startswith(f"/{REPO_NAME}/"):
                    clean_path = val.lstrip("/")
                    tag[attr] = f"/{REPO_NAME}/{clean_path}"
                    modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Fixed paths in: {file_path}")

def run():
    print("Running path conversion...")
    for root, _, files in os.walk(PROJECT_DIR):
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                fix_paths_in_html(full_path)
    print("Path conversion complete.")

if __name__ == "__main__":
    run()