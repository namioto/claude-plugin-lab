---
description: "alfred-jira 에이전트가 특정 프로젝트의 보드 및 스프린트 정보를 조회할 때 사용하는 스킬. 활성 스프린트 ID 확인, MEMORY.md 보드/스프린트 캐시 갱신이 필요할 때 호출된다. 사용자가 직접 호출하지 않으며, alfred-jira 에이전트가 위임하여 호출한다."
user-invocable: false
context: fork
---

# Jira Get Sprints

프로젝트의 보드 목록과 활성/예정 스프린트 정보를 반환한다.

## 입력 형식

호출 시 다음 정보를 포함해야 한다:

```
[CONFIG]
project: {프로젝트 키, 예: DP}
```

## 실행 방법

Bash 도구로 아래 명령을 실행한다:

```bash
uv run .claude/scripts/jira/get_sprints.py \
  --project "{project_key}"
```

- `JIRA_EMAIL`, `JIRA_API_KEY`, `ATLASSIAN_URL` 환경변수가 설정되어 있어야 한다
- 내부적으로 agile REST API(`/rest/agile/1.0/board`, `/rest/agile/1.0/board/{id}/sprint`)를 사용한다

## 출력 형식

성공 시 보드 및 스프린트 정보 JSON을 stdout으로 반환한다:

```json
{
  "boards": [
    { "id": 42, "name": "DP Board", "type": "scrum" }
  ],
  "sprints": [
    {
      "id": 101,
      "name": "Sprint 10",
      "state": "active",
      "boardId": 42,
      "startDate": "2024-01-15T09:00:00.000Z",
      "endDate": "2024-01-29T09:00:00.000Z"
    },
    {
      "id": 102,
      "name": "Sprint 11",
      "state": "future",
      "boardId": 42,
      "startDate": null,
      "endDate": null
    }
  ]
}
```

## MEMORY.md 캐시 갱신 연계

반환된 데이터를 alfred-jira MEMORY.md의 보드/스프린트 섹션에 다음 형식으로 기록한다:

```markdown
## 보드/스프린트 메타 ({project_key})

보드 ID: 42 (DP Board, scrum)
활성 스프린트 ID: 101 (Sprint 10, ~2024-01-29)
```

## 오류 처리

- Scrum 보드가 없는 프로젝트(Kanban 등)는 스프린트 정보가 비어 있을 수 있다
- 오류 발생 시 stderr 메시지를 alfred-jira에 그대로 전달한다
