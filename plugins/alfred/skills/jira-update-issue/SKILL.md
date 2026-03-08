---
description: "alfred 에이전트가 Jira 작업 시 Jira 티켓의 상태(status) 전환, 담당자(assignee) 변경, 댓글(comment) 추가를 수행할 때 사용하는 스킬. 'In Progress로 변경', '완료 처리', '담당자 변경', '댓글 추가' 등의 요청 시 호출된다. 사용자가 직접 호출하지 않으며, alfred 에이전트가 jira 스킬을 통해 호출한다."
user-invocable: false
---

# Jira Update Issue

Jira 티켓의 상태 전환, 담당자 변경, 댓글 추가를 수행한다.

## 입력 형식

호출 시 다음 정보를 포함해야 한다 (status, assignee_id, comment 중 하나 이상 필수):

```
[CONFIG]
issue: {이슈 키, 예: DP-123}
status: {선택사항: 목표 상태명, 예: "In Progress", "Done", "To Do"}
assignee_id: {선택사항: 담당자 accountId}
comment: {선택사항: 댓글 텍스트}
```

## 실행 방법

Bash 도구로 아래 명령을 실행한다:

```bash
# 상태만 변경
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/jira/update_issue.py \
  --issue "{issue_key}" \
  --status "{target_status}"

# 담당자만 변경
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/jira/update_issue.py \
  --issue "{issue_key}" \
  --assignee-id "{account_id}"

# 상태 + 담당자 동시 변경
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/jira/update_issue.py \
  --issue "{issue_key}" \
  --status "{target_status}" \
  --assignee-id "{account_id}"

# 상태 변경 + 댓글 추가 (예: 완료 처리)
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/jira/update_issue.py \
  --issue "{issue_key}" \
  --status "{target_status}" \
  --comment "{comment_text}"
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
    { "field": "assignee", "value": "account-id-xyz" },
    { "field": "comment", "value": "10501" }
  ]
}
```

## 오류 처리

- 목표 상태로의 전환이 현재 워크플로에서 허용되지 않을 수 있다
  - 예: "Backlog → Done" 직접 전환 불가 → 에러 메시지에 가능한 상태 목록 포함
- 잘못된 `assignee_id`는 400 오류를 반환한다
- 오류 발생 시 stderr 메시지를 그대로 전달한다

## 전환 가능 상태 조회

`--list-transitions` 옵션으로 현재 이슈에서 전환 가능한 상태 목록만 조회할 수 있다:

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/jira/update_issue.py \
  --issue "{issue_key}" \
  --list-transitions
```

응답:
```json
{
  "issue": "DP-123",
  "available_transitions": ["진행 중", "완료"]
}
```

상태 전환 성공 시에도 `available_transitions` 필드가 포함되어, 전환 후 상태에서 다시 전환 가능한 목록을 반환한다. jira 오케스트레이터 스킬이 이 정보를 MEMORY.md에 캐시한다.
