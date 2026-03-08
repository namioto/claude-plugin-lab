# /// script
# dependencies = ["requests"]
# ///
"""Jira 보드/스프린트 목록 조회"""

import argparse
import json
import os
import sys

import requests

sys.stdout.reconfigure(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Get Jira board and sprint info")
    parser.add_argument("--project", required=True, help="Project key (e.g. DP)")
    args = parser.parse_args()

    email = os.environ.get("JIRA_EMAIL")
    api_key = os.environ.get("JIRA_API_KEY")
    base_url = os.environ.get("ATLASSIAN_URL", "").rstrip("/")
    if not email or not api_key or not base_url:
        print("Error: JIRA_EMAIL, JIRA_API_KEY, ATLASSIAN_URL environment variables are required", file=sys.stderr)
        sys.exit(1)

    # Step 1: 보드 목록 조회
    boards_url = f"{base_url}/rest/agile/1.0/board"
    boards_resp = requests.get(
        boards_url,
        params={"projectKeyOrId": args.project},
        auth=(email, api_key),
        headers={"Accept": "application/json"},
    )

    if not boards_resp.ok:
        print(f"Error {boards_resp.status_code}: {boards_resp.text}", file=sys.stderr)
        sys.exit(1)

    boards_data = boards_resp.json()
    boards = boards_data.get("values", [])

    if not boards:
        print(json.dumps({"boards": [], "sprints": []}, ensure_ascii=False))
        return

    result = {"boards": [], "sprints": []}

    for board in boards:
        board_id = board["id"]
        board_info = {"id": board_id, "name": board["name"], "type": board.get("type")}
        result["boards"].append(board_info)

        # Step 2: 각 보드의 스프린트 조회 (active + future)
        sprints_url = f"{base_url}/rest/agile/1.0/board/{board_id}/sprint"
        for state in ("active", "future"):
            sprints_resp = requests.get(
                sprints_url,
                params={"state": state},
                auth=(email, api_key),
                headers={"Accept": "application/json"},
            )
            if sprints_resp.ok:
                for sprint in sprints_resp.json().get("values", []):
                    result["sprints"].append(
                        {
                            "id": sprint["id"],
                            "name": sprint["name"],
                            "state": sprint["state"],
                            "boardId": board_id,
                            "startDate": sprint.get("startDate"),
                            "endDate": sprint.get("endDate"),
                        }
                    )

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
