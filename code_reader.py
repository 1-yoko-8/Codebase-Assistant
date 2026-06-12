import os

SUPPORTED_EXTENSIONS = (
    ".py",
    ".js",
    ".ts",
    ".java",
    ".cpp",
    ".c",
    ".h",
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json"
)

def load_code_files(repo_path):

    documents = []

    for root, dirs, files in os.walk(repo_path):    # refer notes

        for file in files:
            if file.endswith(SUPPORTED_EXTENSIONS):
                file_path = os.path.join(root, file)
                try:
                    with open(
                        file_path,
                        "r",
                        encoding="utf-8",   # use utf-8 for bytes to text conversion
                        errors="ignore"     # ignores - UnicodeDecodeError: 'utf-8' codec can't decode byte
                    ) as f:

                        documents.append({
                            "path": file_path,
                            "content": f.read()
                        })

                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return documents