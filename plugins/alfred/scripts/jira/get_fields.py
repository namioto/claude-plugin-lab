# /// script
# dependencies = ["requests"]
# ///
"""Jira 커스텀 필드 목록 조회 및 이름 검색"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import JiraClient, JiraError

sys.stdout.reconfigure(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Get Jira custom fields")
    parser.add_argument("--search", help="Filter fields by name (case-insensitive substring match)")
    args = parser.parse_args()

    client = JiraClient()

    try:
        fields = client.get("/rest/api/3/field")
    except JiraError as e:
        print(f"Error {e.status_code}: {e.text}", file=sys.stderr)
        sys.exit(1)

    if args.search:
        keyword = args.search.lower()
        fields = [f for f in fields if keyword in f.get("name", "").lower()]

    result = [{"id": f["id"], "name": f["name"], "custom": f.get("custom", False)} for f in fields]
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
