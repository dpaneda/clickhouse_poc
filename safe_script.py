#! /usr/bin/env python

import os
import sys
import base64
import subprocess

print("Everything gonna go fine")

def create_and_push_tag(tag_name, message=None):
    # Nothing special is needed to write on the repository, since git is
    # already configured with a write-all credentials from the checkout
    try:
        subprocess.run(['git', 'tag', tag_name], check=True)
        subprocess.run(['git', 'push', 'origin', tag_name], check=True)

        print(f"Tag '{tag_name}' created")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create tag: {e}")


def create_github_issue(title, body=None, labels=None):
    """Create issue using GitHub API with token authentication"""
    repo = os.getenv('GITHUB_REPOSITORY')

    # Extract the auth_header from the persisted stored credentials
    auth = os.popen('git config http.https://github.com/.extraheader').read()
    # Split it and get the auth header which is b64 encoded
    auth_header_b64 = auth.split()[-1]
    # To extract the token, we need to decode the header and split the token
    # access-token:GITHUB_TOKEN
    token = base64.b64decode(auth_header_b64).decode().split(':')[-1]

    # Just use the token for any actions, for example an issue creation
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    payload = {
        "title": title,
        "body": body or "",
        "labels": labels or []
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

create_and_push_tag('test_tag')
issue_response = create_github_issue(
    title="Example issue",
    body="Hello there",
)
