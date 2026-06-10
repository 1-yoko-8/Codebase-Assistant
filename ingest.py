from git import Repo
import shutil
import os


def clone_repo(repo_url):
    repo_path = "repos/project"

    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    Repo.clone_from(repo_url, repo_path)       # mainly to prevent git issues (if repos/project is not new (not empty)) - also limits the app to one active repo

    print("Repository cloned successfully!")


if __name__ == "__main__":
    repo_url = input("Enter GitHub repository URL: ")
    clone_repo(repo_url)

# Testing
# clone_repo("https://github.com/1-yoko-8/electiontrackwebsitebackend.git")