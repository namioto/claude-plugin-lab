# /// script
# dependencies = ["requests"]
# ///
"""Jira JQL 기반 티켓 검색"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import JiraClient, JiraError

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

    client = JiraClient()

    try:
        data = client.get(
            "/rest/api/3/search/jql",
            params={"jql": args.jql, "fields": args.fields, "maxResults": args.max_results},
        )
    except JiraError as e:
        print(f"Error {e.status_code}: {e.text}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    main()
