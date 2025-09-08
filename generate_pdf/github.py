from github import Github
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")

UPDATE_COMMIT_MESSAGE = "Update CV LaTeX file"
DELETE_COMMIT_MESSAGE = "Delete old CV LaTeX file"
FILE_PATH_IN_REPO = "main.tex"

class github_repo:
    def __init__(self):
        self.g = Github(GITHUB_TOKEN)
        self.repo = self.g.get_repo(REPO_NAME)
        self.url = self.repo.html_url

    def upload_file(self, local_path: str):
        with open(local_path, "r", encoding="utf-8") as f:
            content = f.read()

        try:
            file = self.repo.get_contents(FILE_PATH_IN_REPO)
            self.repo.update_file(file.path, UPDATE_COMMIT_MESSAGE, content, file.sha)
            print(f"✅ File updated in repo: {FILE_PATH_IN_REPO}")
        except Exception as e:
            if "404" in str(e):
                # File doesn't exist, create it
                self.repo.create_file(FILE_PATH_IN_REPO, UPDATE_COMMIT_MESSAGE, content)
                print(f"✅ File created in repo: {FILE_PATH_IN_REPO}")
            else:
                print(f"❌ Failed to upload file: {e}")
                raise e
            
    def delete_file(self):
        try:
            file = self.repo.get_contents(FILE_PATH_IN_REPO)
            self.repo.delete_file(file.path, DELETE_COMMIT_MESSAGE, file.sha)
            print(f"✅ File deleted from repo: {FILE_PATH_IN_REPO}")
        except Exception as e:
            print(f"❌ Failed to delete file: {e}")