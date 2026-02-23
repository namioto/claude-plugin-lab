---
description: "alfred-jira 에이전트가 Jira 커스텀 필드 ID를 조회할 때 사용하는 스킬. 사용자가 특정 커스텀 필드('배경 설명', '원인 분석' 등)의 값을 읽거나 쓰도록 요청했을 때, 해당 필드의 ID를 이름으로 검색하여 반환한다. 사용자가 직접 호출하지 않으며, alfred-jira 에이전트가 위임하여 호출한다."
user-invocable: false
context: fork
---

# Jira Get Fields

필드 이름으로 Jira 커스텀 필드 ID를 검색하여 반환한다.

## 입력 형식

```
[CONFIG]
search: {검색할 필드 이름 (선택. 생략 시 전체 반환)}
```

## 실행 방법

Bash 도구로 아래 명령을 실행한다:

```bash
# 이름으로 검색
uv run .claude/scripts/jira/get_fields.py --search "배경 설명"

# 전체 목록 반환
uv run .claude/scripts/jira/get_fields.py
```

- `JIRA_EMAIL`, `JIRA_API_KEY`, `ATLASSIAN_URL` 환경변수가 설정되어 있어야 한다

## 출력 형식

성공 시 매칭된 필드 목록을 JSON 배열로 반환한다:

```json
[
  {"id": "customfield_10050", "name": "배경 설명", "custom": true}
]
```

- `id`: `jira-get-issue`, `jira-search`의 `fields` 파라미터 또는 `jira-create-issue`의 커스텀 필드 값으로 사용
- `custom`: `true`면 커스텀 필드, `false`면 기본 제공 필드

## 오류 처리

- 검색 결과가 없으면 빈 배열 `[]`을 반환한다
- 오류 발생 시 stderr 메시지를 alfred-jira에 그대로 전달한다
