# /// script
# dependencies = ["requests"]
# ///
"""Jira 단일 티켓 상세 조회"""

import argparse
import json
import os
import sys

import requests

sys.stdout.reconfigure(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Get Jira issue detail")
    parser.add_argument("--issue", required=True, help="Issue key (e.g. DP-123)")
    args = parser.parse_args()

    email = os.environ.get("JIRA_EMAIL")
    api_key = os.environ.get("JIRA_API_KEY")
    base_url = os.environ.get("ATLASSIAN_URL", "").rstrip("/")
    if not email or not api_key or not base_url:
        print("Error: JIRA_EMAIL, JIRA_API_KEY, ATLASSIAN_URL environment variables are required", file=sys.stderr)
        sys.exit(1)

    url = f"{base_url}/rest/api/3/issue/{args.issue}"

    resp = requests.get(
        url,
        auth=(email, api_key),
        headers={"Accept": "application/json"},
    )

    if not resp.ok:
        print(f"Error {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(resp.json(), ensure_ascii=False))


if __name__ == "__main__":
    main()
