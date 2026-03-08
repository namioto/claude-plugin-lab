# /// script
# dependencies = ["requests"]
# ///
"""Jira 프로젝트 에픽 목록 조회"""

import argparse
import json
import os
import sys

import requests

sys.stdout.reconfigure(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Get Jira project epics")
    parser.add_argument("--project", required=True, help="Project key (e.g. DP)")
    args = parser.parse_args()

    email = os.environ.get("JIRA_EMAIL")
    api_key = os.environ.get("JIRA_API_KEY")
    base_url = os.environ.get("ATLASSIAN_URL", "").rstrip("/")
    if not email or not api_key or not base_url:
        print("Error: JIRA_EMAIL, JIRA_API_KEY, ATLASSIAN_URL environment variables are required", file=sys.stderr)
        sys.exit(1)

    url = f"{base_url}/rest/api/3/search/jql"

    jql = f"project = {args.project} AND issuetype = Epic ORDER BY created DESC"
    params = {
        "jql": jql,
        "fields": "summary,status,customfield_10014",
        "maxResults": 100,
    }

    resp = requests.get(
        url,
        params=params,
        auth=(email, api_key),
        headers={"Accept": "application/json"},
    )

    if not resp.ok:
        print(f"Error {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(resp.json(), ensure_ascii=False))


if __name__ == "__main__":
    main()
