---
description: "alfred-jira 에이전트가 JQL 쿼리로 Jira 티켓을 검색할 때 사용하는 스킬. 담당자 필터, 스프린트 필터, 프로젝트 필터 등 JQL 기반 검색이 필요한 모든 상황에서 호출된다. 사용자가 직접 호출하지 않으며, alfred-jira 에이전트가 검색 요청 시 위임하여 호출한다."
user-invocable: false
context: fork
---

# Jira Search

JQL 쿼리를 실행하여 Jira 티켓 목록을 반환한다.

## 입력 형식

호출 시 다음 정보를 포함해야 한다:

```
[CONFIG]
jql: {JQL 쿼리 문자열}
fields: {선택사항: 반환할 필드 목록, 콤마 구분}
max_results: {선택사항: 최대 결과 수, 기본값 50}
```

## 실행 방법

Bash 도구로 아래 명령을 실행한다:

```bash
uv run .claude/scripts/jira/search.py \
  --jql "{jql}" \
  [--fields "{fields}"] \
  [--max-results {max_results}]
```

- `JIRA_EMAIL`, `JIRA_API_KEY`, `ATLASSIAN_URL` 환경변수가 설정되어 있어야 한다
- `uv`가 설치되어 있지 않으면 `pip install requests` 후 `python .claude/scripts/jira/search.py`로 실행한다

## 출력 형식

성공 시 Jira REST API의 search 응답 JSON을 stdout으로 반환한다:

```json
{
  "total": 5,
  "issues": [
    {
      "key": "DP-123",
      "fields": {
        "summary": "...",
        "status": { "name": "In Progress" },
        "assignee": { "displayName": "..." },
        "priority": { "name": "High" }
      }
    }
  ]
}
```

## 오류 처리

- 스크립트가 `sys.exit(1)`로 종료되면 stderr의 메시지를 alfred-jira에 그대로 전달한다
- 인증 오류(401), 권한 오류(403), JQL 문법 오류(400) 메시지를 구분하여 보고한다

## 자주 사용하는 JQL 패턴

| 목적 | JQL 예시 |
|------|---------|
| 내 활성 스프린트 티켓 | `assignee = currentUser() AND sprint in openSprints()` |
| 프로젝트 전체 In Progress | `project = DP AND status = "In Progress"` |
| 오늘 업데이트된 티켓 | `project = DP AND updated >= startOfDay()` |
| 미완료 티켓 | `project = DP AND status != Done ORDER BY priority DESC` |
