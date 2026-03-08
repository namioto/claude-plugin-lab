# /// script
# dependencies = ["requests"]
# ///
"""Jira 티켓 생성 (ADF JSON 지원)"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import JiraClient, JiraError

sys.stdout.reconfigure(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Create Jira issue")
    parser.add_argument("--project", required=True, help="Project key (e.g. DP)")
    parser.add_argument("--summary", required=True, help="Issue summary/title")
    parser.add_argument("--type", required=True, dest="issue_type", help="Issue type (e.g. Story, Task, Bug)")
    parser.add_argument("--description-file", help="Path to ADF JSON file for description")
    parser.add_argument("--epic-key", help="Epic issue key to link (e.g. DP-10)")
    parser.add_argument("--sprint-id", type=int, help="Sprint ID to assign")
    args = parser.parse_args()

    client = JiraClient()

    fields = {
        "project": {"key": args.project},
        "summary": args.summary,
        "issuetype": {"name": args.issue_type},
    }

    # ADF description
    if args.description_file:
        try:
            with open(args.description_file, "r", encoding="utf-8") as f:
                fields["description"] = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"Error reading description file: {e}", file=sys.stderr)
            sys.exit(1)

    # 에픽 연결 (customfield_10014 = Epic Link)
    if args.epic_key:
        fields["customfield_10014"] = args.epic_key

    # 스프린트 할당 (customfield_10020 = Sprint)
    if args.sprint_id:
        fields["customfield_10020"] = {"id": args.sprint_id}

    try:
        data = client.post("/rest/api/3/issue", {"fields": fields})
    except JiraError as e:
        print(f"Error {e.status_code}: {e.text}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    main()
