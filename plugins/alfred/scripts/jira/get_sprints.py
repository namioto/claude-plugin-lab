# /// script
# dependencies = ["requests"]
# ///
"""Jira 보드/스프린트 목록 조회"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import JiraClient, JiraError

sys.stdout.reconfigure(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Get Jira board and sprint info")
    parser.add_argument("--project", required=True, help="Project key (e.g. DP)")
    args = parser.parse_args()

    client = JiraClient()

    # Step 1: 보드 목록 조회
    try:
        boards_data = client.get(
            "/rest/agile/1.0/board",
            params={"projectKeyOrId": args.project},
        )
    except JiraError as e:
        print(f"Error {e.status_code}: {e.text}", file=sys.stderr)
        sys.exit(1)

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
        for state in ("active", "future"):
            try:
                sprints_data = client.get(
                    f"/rest/agile/1.0/board/{board_id}/sprint",
                    params={"state": state},
                )
                for sprint in sprints_data.get("values", []):
                    result["sprints"].append({
                        "id": sprint["id"],
                        "name": sprint["name"],
                        "state": sprint["state"],
                        "boardId": board_id,
                        "startDate": sprint.get("startDate"),
                        "endDate": sprint.get("endDate"),
                    })
            except JiraError:
                pass  # 스프린트가 없는 보드는 무시

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
