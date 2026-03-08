# /// script
# dependencies = ["requests"]
# ///
"""Jira 프로젝트 에픽 목록 조회"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import JiraClient, JiraError

sys.stdout.reconfigure(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Get Jira project epics")
    parser.add_argument("--project", required=True, help="Project key (e.g. DP)")
    args = parser.parse_args()

    client = JiraClient()

    jql = f"project = {args.project} AND issuetype = Epic ORDER BY created DESC"
    try:
        data = client.get(
            "/rest/api/3/search/jql",
            params={"jql": jql, "fields": "summary,status,customfield_10014", "maxResults": 100},
        )
    except JiraError as e:
        print(f"Error {e.status_code}: {e.text}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    main()
