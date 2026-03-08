# /// script
# dependencies = ["requests"]
# ///
"""Jira 단일 티켓 상세 조회"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import JiraClient, JiraError

sys.stdout.reconfigure(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Get Jira issue detail")
    parser.add_argument("--issue", required=True, help="Issue key (e.g. DP-123)")
    args = parser.parse_args()

    client = JiraClient()

    try:
        data = client.get(f"/rest/api/3/issue/{args.issue}")
    except JiraError as e:
        print(f"Error {e.status_code}: {e.text}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    main()
