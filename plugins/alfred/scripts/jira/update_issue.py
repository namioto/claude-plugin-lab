# /// script
# dependencies = ["requests"]
# ///
"""Jira 티켓 상태/담당자 업데이트"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import JiraClient, JiraError

sys.stdout.reconfigure(encoding="utf-8")


def get_transitions(client: JiraClient, issue_key: str) -> list:
    """가능한 전환 목록 조회"""
    data = client.get(f"/rest/api/3/issue/{issue_key}/transitions")
    return data.get("transitions", [])


def transition_issue(client: JiraClient, issue_key: str, target_status: str) -> str:
    """상태 전환 수행 (이름 기반 매칭)"""
    transitions = get_transitions(client, issue_key)

    # 대소문자 무시하여 이름 매칭
    target_lower = target_status.lower()
    matched = next(
        (t for t in transitions if t["name"].lower() == target_lower),
        None,
    )

    if not matched:
        available = [t["name"] for t in transitions]
        print(
            f"Error: status '{target_status}' not found. Available: {available}",
            file=sys.stderr,
        )
        sys.exit(1)

    client.post(
        f"/rest/api/3/issue/{issue_key}/transitions",
        {"transition": {"id": matched["id"]}},
    )

    return matched["name"]


def resolve_assignee_id(client: JiraClient, assignee_id: str) -> str:
    """'current' 키워드를 실제 accountId로 변환"""
    if assignee_id.lower() != "current":
        return assignee_id
    data = client.get("/rest/api/3/myself")
    return data["accountId"]


def update_assignee(client: JiraClient, issue_key: str, assignee_id: str) -> str:
    """담당자 변경"""
    assignee_id = resolve_assignee_id(client, assignee_id)
    client.put(
        f"/rest/api/3/issue/{issue_key}",
        {"fields": {"assignee": {"accountId": assignee_id}}},
    )
    return assignee_id


def add_comment(client: JiraClient, issue_key: str, comment_text: str) -> str:
    """댓글 추가 (ADF 형식)"""
    payload = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": comment_text}],
                }
            ],
        }
    }
    data = client.post(f"/rest/api/3/issue/{issue_key}/comment", payload)
    return data.get("id") if data else None


def update_priority(client: JiraClient, issue_key: str, priority_name: str) -> str:
    """우선순위 변경"""
    client.put(
        f"/rest/api/3/issue/{issue_key}",
        {"fields": {"priority": {"name": priority_name}}},
    )
    return priority_name


def main():
    parser = argparse.ArgumentParser(description="Update Jira issue status or assignee")
    parser.add_argument("--issue", required=True, help="Issue key (e.g. DP-123)")
    parser.add_argument("--status", help="Target status name (e.g. 'In Progress', 'Done')")
    parser.add_argument("--assignee-id", help="Assignee account ID")
    parser.add_argument("--priority", help="Priority name (e.g. 'High', 'Medium', 'Low')")
    parser.add_argument("--comment", help="Comment text to add")
    parser.add_argument("--list-transitions", action="store_true", help="List available transitions and exit")
    args = parser.parse_args()

    if not args.list_transitions and not args.status and not args.assignee_id and not args.priority and not args.comment:
        print("Error: at least one of --status, --assignee-id, --priority, --comment, or --list-transitions is required", file=sys.stderr)
        sys.exit(1)

    client = JiraClient()

    try:
        if args.list_transitions:
            transitions = get_transitions(client, args.issue)
            result = {
                "issue": args.issue,
                "available_transitions": [t["name"] for t in transitions],
            }
            print(json.dumps(result, ensure_ascii=False))
            return

        result = {"issue": args.issue, "updated": []}

        if args.status:
            new_status = transition_issue(client, args.issue, args.status)
            result["updated"].append({"field": "status", "value": new_status})
            # 전환 후 새로운 상태에서의 가능한 전환 목록도 반환
            post_transitions = get_transitions(client, args.issue)
            result["available_transitions"] = [t["name"] for t in post_transitions]

        if args.assignee_id:
            resolved_id = update_assignee(client, args.issue, args.assignee_id)
            result["updated"].append({"field": "assignee", "value": resolved_id})

        if args.priority:
            new_priority = update_priority(client, args.issue, args.priority)
            result["updated"].append({"field": "priority", "value": new_priority})

        if args.comment:
            comment_id = add_comment(client, args.issue, args.comment)
            result["updated"].append({"field": "comment", "value": comment_id})

        print(json.dumps(result, ensure_ascii=False))

    except JiraError as e:
        print(f"Error {e.status_code}: {e.text}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
