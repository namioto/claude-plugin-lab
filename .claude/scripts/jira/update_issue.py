# /// script
# dependencies = ["requests"]
# ///
"""Jira 티켓 상태/담당자 업데이트"""

import argparse
import json
import os
import sys

import requests

sys.stdout.reconfigure(encoding="utf-8")


def get_transitions(base_url, issue_key, auth):
    """가능한 전환 목록 조회"""
    url = f"{base_url}/rest/api/3/issue/{issue_key}/transitions"
    resp = requests.get(url, auth=auth, headers={"Accept": "application/json"})
    if not resp.ok:
        print(f"Error fetching transitions {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)
    return resp.json().get("transitions", [])


def transition_issue(base_url, issue_key, target_status, auth):
    """상태 전환 수행 (이름 기반 매칭)"""
    transitions = get_transitions(base_url, issue_key, auth)

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

    url = f"{base_url}/rest/api/3/issue/{issue_key}/transitions"
    payload = {"transition": {"id": matched["id"]}}
    resp = requests.post(
        url,
        json=payload,
        auth=auth,
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )

    if not resp.ok:
        print(f"Error {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)

    return matched["name"]


def update_assignee(base_url, issue_key, assignee_id, auth):
    """담당자 변경"""
    url = f"{base_url}/rest/api/3/issue/{issue_key}"
    payload = {"fields": {"assignee": {"accountId": assignee_id}}}
    resp = requests.put(
        url,
        json=payload,
        auth=auth,
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )
    if not resp.ok:
        print(f"Error {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Update Jira issue status or assignee")
    parser.add_argument("--issue", required=True, help="Issue key (e.g. DP-123)")
    parser.add_argument("--status", help="Target status name (e.g. 'In Progress', 'Done')")
    parser.add_argument("--assignee-id", help="Assignee account ID")
    args = parser.parse_args()

    if not args.status and not args.assignee_id:
        print("Error: at least one of --status or --assignee-id is required", file=sys.stderr)
        sys.exit(1)

    email = os.environ.get("JIRA_EMAIL")
    api_key = os.environ.get("JIRA_API_KEY")
    base_url = os.environ.get("ATLASSIAN_URL", "").rstrip("/")
    if not email or not api_key or not base_url:
        print("Error: JIRA_EMAIL, JIRA_API_KEY, ATLASSIAN_URL environment variables are required", file=sys.stderr)
        sys.exit(1)

    auth = (email, api_key)
    result = {"issue": args.issue, "updated": []}

    if args.status:
        new_status = transition_issue(base_url, args.issue, args.status, auth)
        result["updated"].append({"field": "status", "value": new_status})

    if args.assignee_id:
        update_assignee(base_url, args.issue, args.assignee_id, auth)
        result["updated"].append({"field": "assignee", "value": args.assignee_id})

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
