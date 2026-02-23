# /// script
# dependencies = ["requests"]
# ///
"""Jira 커스텀 필드 목록 조회 및 이름 검색"""

import argparse
import json
import os
import sys

import requests

sys.stdout.reconfigure(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Get Jira custom fields")
    parser.add_argument("--search", help="Filter fields by name (case-insensitive substring match)")
    args = parser.parse_args()

    email = os.environ.get("JIRA_EMAIL")
    api_key = os.environ.get("JIRA_API_KEY")
    base_url = os.environ.get("ATLASSIAN_URL", "").rstrip("/")
    if not email or not api_key or not base_url:
        print("Error: JIRA_EMAIL, JIRA_API_KEY, ATLASSIAN_URL environment variables are required", file=sys.stderr)
        sys.exit(1)

    resp = requests.get(
        f"{base_url}/rest/api/3/field",
        auth=(email, api_key),
        headers={"Accept": "application/json"},
    )

    if not resp.ok:
        print(f"Error {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)

    fields = resp.json()

    if args.search:
        keyword = args.search.lower()
        fields = [f for f in fields if keyword in f.get("name", "").lower()]

    result = [{"id": f["id"], "name": f["name"], "custom": f.get("custom", False)} for f in fields]
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
