---
description: "alfred 에이전트가 Jira 작업 시 프로젝트의 메타데이터(이슈 유형, 상태 목록, 우선순위, 담당 가능 사용자, 커스텀 필드)를 조회하고 로컬 캐시에 저장할 때 사용하는 스킬. 티켓 생성·수정 전 프로젝트 정보 확인, '이슈 유형 뭐 있어?', '담당자 목록', '메타데이터 갱신' 등의 요청 시 호출된다. 사용자가 직접 호출하지 않으며, alfred 에이전트가 jira 스킬을 통해 호출한다."
user-invocable: false
---

# Jira Get Project Meta

프로젝트 메타데이터를 조회하고 로컬 JSON 캐시에 저장한다. 캐시가 유효하면(7일 이내) API 호출 없이 캐시를 반환한다.

## 캐시 대상

### 프로젝트별 데이터
- **이슈 유형**: Story, Task, Bug, Sub-task 등 (프로젝트 워크플로우에 따라 다름)
- **상태 목록**: 이슈 유형별 사용 가능한 상태 (해야 할 일, 진행 중, 완료 등)
- **담당 가능 사용자**: displayName + accountId + email

### 글로벌 데이터 (`--include-global` 옵션)
- **우선순위**: Highest, High, Medium, Low, Lowest 등
- **커스텀 필드**: 필드 ID + 이름 (custom 필드만)

## 입력 형식

```
[CONFIG]
project: {프로젝트 키, 예: DP}
refresh: {선택, true면 캐시 무시하고 재조회}
include_global: {선택, true면 우선순위/커스텀 필드도 조회}
```

## 실행 방법

Bash 도구로 아래 명령을 실행한다:

```bash
# 프로젝트 메타만 조회 (캐시 우선)
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/jira/get_project_meta.py \
  --project "{project_key}"

# 글로벌 메타 포함
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/jira/get_project_meta.py \
  --project "{project_key}" \
  --include-global

# 캐시 무시하고 강제 재조회
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/jira/get_project_meta.py \
  --project "{project_key}" \
  --refresh \
  --include-global
```

- `JIRA_EMAIL`, `JIRA_API_KEY`, `ATLASSIAN_URL` 환경변수가 설정되어 있어야 한다

## 출력 형식

```json
{
  "project": {
    "issue_types": [
      {"id": "10001", "name": "Story", "subtask": false, "statuses": [
        {"id": "1", "name": "해야 할 일", "category": "new"},
        {"id": "3", "name": "진행 중", "category": "indeterminate"},
        {"id": "5", "name": "완료", "category": "done"}
      ]}
    ],
    "assignable_users": [
      {"accountId": "abc123", "displayName": "Park", "emailAddress": "park@example.com"}
    ],
    "_source": "cache"
  },
  "priorities": [{"id": "1", "name": "Highest"}, ...],
  "custom_fields": [{"id": "customfield_10014", "name": "Epic Link", "custom": true}, ...]
}
```

- `_source` 필드: `"cache"` 또는 `"api"` — 데이터 출처 표시

## 캐시 위치

`${CLAUDE_PLUGIN_ROOT}/scripts/jira/.cache/project_meta.json` (자동 생성, gitignore 대상)

## 오류 처리

- Jira API 호출 실패 시 stderr에 에러 메시지 출력 후 종료
- 캐시 파일 손상 시 자동으로 재생성
