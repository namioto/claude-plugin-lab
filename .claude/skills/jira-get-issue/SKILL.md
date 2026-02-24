---
description: "alfred-jira 에이전트가 특정 Jira 티켓의 상세 정보를 조회할 때 사용하는 스킬. 티켓 키(예: DP-123)로 단일 이슈의 전체 필드를 가져올 때 호출된다. 사용자가 직접 호출하지 않으며, alfred-jira 에이전트가 위임하여 호출한다."
user-invocable: false
---

# Jira Get Issue

티켓 키로 단일 Jira 이슈의 상세 정보를 반환한다.

## 입력 형식

호출 시 다음 정보를 포함해야 한다:

```
[CONFIG]
issue: {이슈 키, 예: DP-123}
```

## 실행 방법

Bash 도구로 아래 명령을 실행한다:

```bash
uv run .claude/scripts/jira/get_issue.py \
  --issue "{issue_key}"
```

- `JIRA_EMAIL`, `JIRA_API_KEY`, `ATLASSIAN_URL` 환경변수가 설정되어 있어야 한다

## 출력 형식

성공 시 Jira REST API의 issue 응답 JSON을 stdout으로 반환한다:

```json
{
  "key": "DP-123",
  "fields": {
    "summary": "...",
    "description": { "type": "doc", "content": [...] },
    "status": { "name": "In Progress" },
    "assignee": { "displayName": "...", "accountId": "..." },
    "priority": { "name": "High" },
    "issuetype": { "name": "Story" },
    "created": "2024-01-15T09:00:00.000+0900",
    "updated": "2024-01-20T14:30:00.000+0900",
    "comment": { "comments": [...] }
  }
}
```

## 오류 처리

- 존재하지 않는 키 조회 시 404 오류가 반환된다
- 오류 발생 시 stderr 메시지를 alfred-jira에 그대로 전달한다
