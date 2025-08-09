import argparse
import urllib.request
import json

parser = argparse.ArgumentParser(prog="Github-Activity CLI", description="Displays recent activity of a github user")
parser.add_argument("username", type=str, help="Enter your github username")
args = parser.parse_args()

url = f"https://api.github.com/users/{args.username}/events"

with urllib.request.urlopen(url) as response: 
    body = response.read()

body_str = body.decode("utf-8")
events = json.loads(body_str)

for event in events: 

    if event["type"] == "PushEvent": 

        name = event["repo"]["name"]
        branch = event["payload"]["ref"]
        commits = len(event["payload"]["commits"])
        print(f"Pushed {commits} commits to {branch.replace('refs/heads/', '')} branch of {name}")

    elif event["type"] == "WatchEvent":
        repo_name = event["repo"]["name"]
        print(f"⭐ Starred {repo_name}")

    elif event["type"] == "ForkEvent": 
        repo_name = event["repo"]["name"]
        forkee = event["payload"]["forkee"]["full_name"]
        print(f"Forked {repo_name} -> {forkee}")
    
    elif event["type"] == "IssuesEvent": 
        action = event["payload"]["action"]
        issue_title = event["payload"]["issue"]["title"]
        issue_number = event["payload"]["issue"]["number"]
        repo_name = event["repo"]["name"]
        print(f"{action} issue #{issue_number}: '{issue_title}' in {repo_name}")

    elif event["type"] == "PullRequestEvent":
        action = event["payload"]["action"]
        pr_number = event["payload"]["pull_request"]["number"]
        pr_title = event["payload"]["pull_request"]["title"]
        repo_name = event["repo"]["name"]
        print(f"{action} PR #{pr_number}: '{pr_title}' in {repo_name}")

    elif event["type"] == "CreateEvent":
        ref_type = event["payload"]["ref_type"]
        ref = event["payload"]["ref"]
        repo_name = event["repo"]["name"]
        print(f"Created branch {ref} in {repo_name}")
    
    else:
        print(f"[?] Unhandled event type: {event['type']}")