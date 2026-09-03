import os
import warnings
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# Replace with your actual GitHub repository name (e.g., "website" or "hccf-site")
REPO_NAME = "hccf.github.io"
PROJECT_DIR = "./"

def inject_base_tag(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    head = soup.find("head")

    if head:
        # Check if base tag already exists
        existing_base = head.find("base")
        base_url = f"/{REPO_NAME}/"

        if existing_base:
            existing_base["href"] = base_url
        else:
            base_tag = soup.new_tag("base", href=base_url)
            head.insert(0, base_tag)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Injected <base> tag into: {file_path}")

def run():
    for root, _, files in os.walk(PROJECT_DIR):
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                inject_base_tag(full_path)

if __name__ == "__main__":
    run()