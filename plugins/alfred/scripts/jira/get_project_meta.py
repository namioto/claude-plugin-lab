# /// script
# dependencies = ["requests"]
# ///
"""Jira 프로젝트 메타데이터 조회 및 캐시"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import JiraClient, JiraError
from lib.cache import MetaCache

sys.stdout.reconfigure(encoding="utf-8")


def fetch_project_meta(client: JiraClient, project_key: str) -> dict:
    """프로젝트별 메타데이터 조회: 이슈 유형 + 상태, 담당 가능 사용자"""
    # 이슈 유형 + 상태 (프로젝트별)
    statuses_data = client.get(f"/rest/api/3/project/{project_key}/statuses")
    issue_types = []
    for it in statuses_data:
        issue_types.append({
            "id": it.get("id"),
            "name": it.get("name"),
            "subtask": it.get("subtask", False),
            "statuses": [
                {
                    "id": s.get("id"),
                    "name": s.get("name"),
                    "category": s.get("statusCategory", {}).get("key"),
                }
                for s in it.get("statuses", [])
            ],
        })

    # 담당 가능 사용자 (프로젝트별)
    users_data = client.get(
        "/rest/api/3/user/assignable/search",
        params={"project": project_key, "maxResults": 1000},
    )
    assignable_users = [
        {
            "accountId": u.get("accountId"),
            "displayName": u.get("displayName"),
            "emailAddress": u.get("emailAddress"),
        }
        for u in users_data
        if u.get("accountType") == "atlassian"
    ]

    return {"issue_types": issue_types, "assignable_users": assignable_users}


def fetch_global_meta(client: JiraClient) -> dict:
    """글로벌 메타데이터 조회: 우선순위, 커스텀 필드"""
    result = {}

    # 우선순위 (글로벌)
    priorities_data = client.get("/rest/api/3/priority")
    result["priorities"] = [
        {"id": p.get("id"), "name": p.get("name")}
        for p in priorities_data
    ]

    # 커스텀 필드 (글로벌)
    fields_data = client.get("/rest/api/3/field")
    result["custom_fields"] = [
        {"id": f["id"], "name": f["name"], "custom": f.get("custom", False)}
        for f in fields_data
        if f.get("custom", False)
    ]

    return result


def main():
    parser = argparse.ArgumentParser(description="Fetch and cache Jira project metadata")
    parser.add_argument("--project", required=True, help="Project key (e.g. DP)")
    parser.add_argument("--refresh", action="store_true", help="Force re-fetch ignoring cache")
    parser.add_argument("--include-global", action="store_true", help="Also fetch priorities and custom fields")
    args = parser.parse_args()

    cache = MetaCache()
    client = None
    result = {}

    # 프로젝트 메타
    try:
        cached_project = None if args.refresh else cache.get_project(args.project)
        if cached_project:
            result["project"] = {**cached_project, "_source": "cache"}
        else:
            client = client or JiraClient()
            project_data = fetch_project_meta(client, args.project)
            cache.set_project(args.project, project_data)
            result["project"] = {**project_data, "_source": "api"}
    except JiraError as e:
        print(f"Error fetching project meta: {e.status_code}: {e.text}", file=sys.stderr)
        sys.exit(1)

    # 글로벌 메타
    if args.include_global:
        try:
            cached_priorities = None if args.refresh else cache.get_global("priorities")
            cached_fields = None if args.refresh else cache.get_global("custom_fields")

            if cached_priorities and cached_fields:
                result["priorities"] = cached_priorities
                result["custom_fields"] = cached_fields
                result["_global_source"] = "cache"
            else:
                client = client or JiraClient()
                global_data = fetch_global_meta(client)
                cache.set_global("priorities", global_data["priorities"])
                cache.set_global("custom_fields", global_data["custom_fields"])
                result["priorities"] = global_data["priorities"]
                result["custom_fields"] = global_data["custom_fields"]
                result["_global_source"] = "api"
        except JiraError as e:
            print(f"Error fetching global meta: {e.status_code}: {e.text}", file=sys.stderr)
            sys.exit(1)

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
