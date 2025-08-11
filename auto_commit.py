import os
import random
import time
from datetime import datetime
import subprocess

# Config
MIN_COMMITS = 2
MAX_COMMITS = 5
MIN_DELAY = 300     # 5 minutes in seconds
MAX_DELAY = 1800    # 30 minutes in seconds
LOG_FILE = "activity.log"

def git(*args):
    """Run a git command."""
    return subprocess.run(["git"] + list(args), check=True)

def make_commit(commit_num):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - Commit #{commit_num}\n")
    git("add", LOG_FILE)
    git("commit", "-m", f"Automated commit #{commit_num} at {timestamp}")
    git("push", "origin", "main")  # Change 'main' if your branch is different
    print(f"[+] Commit #{commit_num} pushed at {timestamp}")

if __name__ == "__main__":
    commits_today = random.randint(MIN_COMMITS, MAX_COMMITS)
    print(f"Making {commits_today} commits today...")

    for i in range(1, commits_today + 1):
        make_commit(i)
        if i != commits_today:
            delay = random.randint(MIN_DELAY, MAX_DELAY)
            print(f"Sleeping {delay // 60} minutes before next commit...")
            time.sleep(delay)

