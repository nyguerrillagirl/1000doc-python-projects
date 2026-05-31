import os
import subprocess

# List of repo directories (absolute paths recommended)
REPOS = [
    r"C:\1000-days-of-code",    # original repo
    r"C:\1000-days-of-code-repos\1000doc-brainycode-website",
    r"C:\1000-days-of-code-repos\1000doc-coursera",
    r"C:\1000-days-of-code-repos\1000doc-docs",
    r"C:\1000-days-of-code-repos\1000doc-html-css-javascript-projects",
    r"C:\1000-days-of-code-repos\1000doc-intellij-projects",
    r"C:\1000-days-of-code-repos\1000doc-python-projects",
    r"C:\1000-days-of-code-repos\1000doc-react-projects",
    r"C:\1000-days-of-code-repos\1000doc-windows-programming",
    r"C:\1000-days-of-code-repos\1000doc-dos-games",
]

CYAN = "\033[96m"
RESET = "\033[0m"


def run(cmd, cwd):
    """Run a shell command inside a specific directory and return output."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=True)
    return result.stdout.strip()


def update_repo(path):
    print(f"\n{CYAN}=== Checking repo: {path} ==={RESET}")

    # Check for changes
    status = run("git status --porcelain", path)

    if not status:
        print("No changes. Skipping.")
        return

    print("Changes detected:")
    print(run("git status", path))

    msg = input("Commit message (leave empty to skip): ").strip()
    if not msg:
        print("Skipping commit for this repo.")
        return

    # Commit and push
    print(f"...Updating the repo: {path}")
    run("git add .", path)
    #run(f'git commit -m "{msg}"', path)
    subprocess.run(["git", "commit", "-m", msg], cwd=path)
    print(run("git push", path))

    print("Updated successfully.")


def main():
    for repo in REPOS:
        if os.path.isdir(repo):
            update_repo(repo)
        else:
            print(f"Directory not found: {repo}")


if __name__ == "__main__":
    main()
