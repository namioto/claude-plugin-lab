---
description: "alfred-jira 에이전트가 특정 프로젝트의 에픽 목록을 조회할 때 사용하는 스킬. 티켓 생성 전 에픽 연결이 필요하거나, MEMORY.md 에픽 캐시를 채워야 할 때 호출된다. 사용자가 직접 호출하지 않으며, alfred-jira 에이전트가 위임하여 호출한다."
user-invocable: false
context: fork
---

# Jira Get Epics

프로젝트의 에픽(issuetype = Epic) 목록을 반환한다.

## 입력 형식

호출 시 다음 정보를 포함해야 한다:

```
[CONFIG]
project: {프로젝트 키, 예: DP}
```

## 실행 방법

Bash 도구로 아래 명령을 실행한다:

```bash
uv run .claude/scripts/jira/get_epics.py \
  --project "{project_key}"
```

- `JIRA_EMAIL`, `JIRA_API_KEY`, `ATLASSIAN_URL` 환경변수가 설정되어 있어야 한다
- 내부적으로 `project = {key} AND issuetype = Epic ORDER BY created DESC` JQL을 사용한다

## 출력 형식

성공 시 에픽 검색 결과 JSON을 stdout으로 반환한다:

```json
{
  "total": 3,
  "issues": [
    {
      "key": "DP-10",
      "fields": {
        "summary": "사용자 인증 개선",
        "status": { "name": "In Progress" }
      }
    }
  ]
}
```

## MEMORY.md 캐시 갱신 연계

반환된 에픽 목록을 alfred-jira MEMORY.md의 에픽 섹션에 다음 형식으로 기록한다:

```markdown
## 에픽 목록 ({project_key})

| Key | 제목 | 상태 |
|-----|------|------|
| DP-10 | 사용자 인증 개선 | In Progress |
| DP-20 | 성능 최적화 | To Do |
```

## 오류 처리

- 프로젝트가 존재하지 않으면 400/404 오류가 반환된다
- 오류 발생 시 stderr 메시지를 alfred-jira에 그대로 전달한다
