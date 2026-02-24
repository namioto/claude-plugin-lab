---
description: "alfred-jira 에이전트가 Jira 티켓의 상태(status)를 전환하거나 담당자(assignee)를 변경할 때 사용하는 스킬. 'In Progress로 변경', '완료 처리', '담당자 변경' 등의 요청 시 호출된다. 사용자가 직접 호출하지 않으며, alfred-jira 에이전트가 위임하여 호출한다."
user-invocable: false
---

# Jira Update Issue

Jira 티켓의 상태 전환 또는 담당자 변경을 수행한다.

## 입력 형식

호출 시 다음 정보를 포함해야 한다 (status 또는 assignee_id 중 하나 이상 필수):

```
[CONFIG]
issue: {이슈 키, 예: DP-123}
status: {선택사항: 목표 상태명, 예: "In Progress", "Done", "To Do"}
assignee_id: {선택사항: 담당자 accountId}
```

## 실행 방법

Bash 도구로 아래 명령을 실행한다:

```bash
# 상태만 변경
uv run .claude/scripts/jira/update_issue.py \
  --issue "{issue_key}" \
  --status "{target_status}"

# 담당자만 변경
uv run .claude/scripts/jira/update_issue.py \
  --issue "{issue_key}" \
  --assignee-id "{account_id}"

# 상태 + 담당자 동시 변경
uv run .claude/scripts/jira/update_issue.py \
  --issue "{issue_key}" \
  --status "{target_status}" \
  --assignee-id "{account_id}"
```

- `JIRA_EMAIL`, `JIRA_API_KEY`, `ATLASSIAN_URL` 환경변수가 설정되어 있어야 한다

## 상태 전환 내부 동작

`--status` 지정 시 스크립트가 2단계로 처리한다:

1. `GET /rest/api/3/issue/{key}/transitions` → 현재 가능한 전환 목록 조회
2. 목표 상태명과 대소문자 무시하여 매칭 → `POST /rest/api/3/issue/{key}/transitions`

가능한 전환이 없으면 `stderr`에 사용 가능한 상태 목록을 출력하고 `sys.exit(1)`로 종료한다.

## 출력 형식

성공 시 업데이트 결과 JSON을 stdout으로 반환한다:

```json
{
  "issue": "DP-123",
  "updated": [
    { "field": "status", "value": "In Progress" },
    { "field": "assignee", "value": "account-id-xyz" }
  ]
}
```

## 오류 처리

- 목표 상태로의 전환이 현재 워크플로에서 허용되지 않을 수 있다
  - 예: "Backlog → Done" 직접 전환 불가 → 에러 메시지에 가능한 상태 목록 포함
- 잘못된 `assignee_id`는 400 오류를 반환한다
- 오류 발생 시 stderr 메시지를 alfred-jira에 그대로 전달한다
