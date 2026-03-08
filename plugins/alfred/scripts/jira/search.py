# /// script
# dependencies = ["requests"]
# ///
"""Jira JQL 기반 티켓 검색"""

import argparse
import json
import os
import sys

import requests

sys.stdout.reconfigure(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Jira JQL search")
    parser.add_argument("--jql", required=True, help="JQL query string")
    parser.add_argument(
        "--fields",
        default="summary,status,assignee,priority,issuetype,created,updated,duedate,customfield_10014,customfield_10020",
        help="Comma-separated field list",
    )
    parser.add_argument("--max-results", type=int, default=50, help="Maximum number of results")
    args = parser.parse_args()

    email = os.environ.get("JIRA_EMAIL")
    api_key = os.environ.get("JIRA_API_KEY")
    base_url = os.environ.get("ATLASSIAN_URL", "").rstrip("/")
    if not email or not api_key or not base_url:
        print("Error: JIRA_EMAIL, JIRA_API_KEY, ATLASSIAN_URL environment variables are required", file=sys.stderr)
        sys.exit(1)

    url = f"{base_url}/rest/api/3/search/jql"

    params = {
        "jql": args.jql,
        "fields": args.fields,
        "maxResults": args.max_results,
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
