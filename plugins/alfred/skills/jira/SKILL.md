---
description: "alfred 에이전트가 Jira 검색, 티켓 생성, 상태 변경 등 메모리 기반 워크플로우가 필요한 Jira 작업을 수행할 때 호출하는 오케스트레이터 스킬. JQL 검색, 이슈 생성, 이슈 업데이트, 에픽/스프린트 조회 등 복합적인 Jira 작업을 MEMORY.md 기반으로 조율한다."
user-invocable: false
---

# Jira Orchestrator

Jira Software의 메모리 기반 워크플로우를 조율하는 오케스트레이터 스킬. JQL 검색, 티켓 생성, 상태 변경 등 복합적인 Jira 작업을 MEMORY.md와 연계하여 수행한다.

## 시작 절차 (매 호출 시 필수)

1. **MEMORY.md 읽기**: Read 도구로 `~/.claude/agent-memory/jira/MEMORY.md`를 읽는다.
2. **요청 처리**: 프롬프트의 내용을 수행한다.

## API 작업 → 스킬 매핑

모든 Jira API 호출은 스킬을 우선 사용한다. 스킬로 처리할 수 없는 경우 Bash를 활용한다.

| 작업 | 사용 스킬 | 주요 입력 |
|------|---------|---------|
| JQL 티켓 검색 | `jira-search` | jql, fields, max_results |
| 티켓 생성 | `jira-create-issue` | project, summary, type, description_markdown, epic_key, sprint_id |
| 상태/담당자/댓글 변경 | `jira-update-issue` | issue, status, assignee_id, comment |
| 에픽 목록 조회 | `jira-get-epics` | project |
| 보드/스프린트 조회 | `jira-get-sprints` | project |
| 프로젝트 메타데이터 조회 | `jira-get-project-meta` | project, refresh, include_global |

## JQL 워크플로우

목록 조회 요청(검색, 할 일, 완료 항목 등)은 반드시 아래 절차를 따른다.

### 1단계: 저장된 JQL 확인

MEMORY.md의 `저장된 JQL` 섹션에서 요청과 유사한 항목을 찾는다.

- **저장된 JQL이 있으면**: 사용자에게 저장된 JQL을 제시하고 이대로 탐색할지 확인한다.
  > 예) "이전에 저장해 두신 JQL이 있습니다: `{jql}` — 이대로 탐색해 드릴까요, 아니면 수정이 필요하십니까?"
- **저장된 JQL이 없으면**: 요청을 분석하여 JQL 초안을 제안한다 (2단계로 이동).

### 2단계: JQL 제안 및 확인 (저장된 JQL 없는 경우)

요청 내용을 분석하여 적합한 JQL 초안을 사용자에게 제시한다.

> 예) "오늘 할 일 조회를 위해 아래 JQL을 제안합니다:
> ```
> assignee = currentUser() AND statusCategory != Done ORDER BY priority DESC
> ```
> 이대로 탐색해 드릴까요, 아니면 수정하실 부분이 있으십니까?"

사용자가 수정을 요청하면 JQL을 수정하고 재확인한다. 확인이 완료될 때까지 탐색을 실행하지 않는다.

### 3단계: 탐색 실행

확인된 JQL로 `jira-search` 스킬을 호출한다.

### 4단계: JQL 저장 제안 (신규 JQL인 경우)

MEMORY.md에 없던 새로운 JQL로 탐색한 경우, 탐색 결과와 함께 저장 여부를 사용자에게 제안한다.

> 예) "이 JQL을 '오늘 할 일'로 저장해 두면 다음번에 바로 사용할 수 있습니다. 저장해 드릴까요?"

사용자가 동의하면 MEMORY.md의 `저장된 JQL` 섹션에 기록한다.

### JQL 수정 요청 처리

사용자가 기존 저장된 JQL의 수정을 요청하면, 수정된 JQL로 MEMORY.md를 덮어쓴다.

## 메타데이터 필요 시점 정책

프로젝트 메타데이터(이슈 유형, 상태, 우선순위, 담당 가능 사용자, 커스텀 필드)는 `jira-get-project-meta` 스킬이 로컬 JSON 캐시로 자동 관리한다. 캐시가 유효하면(7일 이내) API 호출 없이 캐시를 반환하므로, 부담 없이 호출할 수 있다.

### 읽기 작업 (메타데이터 불필요)

- `jira-search`: 메타데이터 확인 없이 즉시 수행

### 쓰기 작업 (메타데이터 자동 확인)

- **`jira-create-issue`**: 이슈 유형 확인이 필요하다.
  - `jira-get-project-meta` 스킬을 호출하여 프로젝트의 유효한 이슈 유형과 담당 가능 사용자를 확인한다 (캐시 자동 관리).
  - 에픽/스프린트 정보가 필요하면 `jira-get-epics`, `jira-get-sprints`를 사용자 동의 후 호출한다.
- **`jira-update-issue`**: 상태 전환은 스크립트가 내부적으로 처리한다. 담당자 변경 시 `jira-get-project-meta`에서 accountId를 참조할 수 있다.

## 메모리 정책

### 저장된 JQL

사용자가 확인한 JQL을 `저장된 JQL` 섹션에 기록한다. 형식:

```
## 저장된 JQL
<!-- 사용자가 확인·저장한 JQL 목록 -->

### 오늘 할 일
```
assignee = currentUser() AND statusCategory != Done ORDER BY priority DESC
```

### 이번 주 완료한 일
```
assignee = currentUser() AND statusCategory = Done AND updated >= startOfWeek()
```
```

각 항목에는 JQL 이름(사용자가 붙인 이름 또는 요청 내용 기반)과 JQL 쿼리를 기록한다.

### 프로젝트 메타데이터 (JSON 캐시 — 자동 관리)

이슈 유형, 상태 목록, 우선순위, 담당 가능 사용자, 커스텀 필드는 `jira-get-project-meta` 스킬이 로컬 JSON 파일(`scripts/jira/.cache/project_meta.json`)로 자동 관리한다. MEMORY.md에 기록하지 않는다.

- **조회**: `jira-get-project-meta` 스킬 호출 (캐시 유효 시 API 호출 없음)
- **강제 갱신**: `refresh: true` 옵션으로 호출하거나, 사용자가 "메타데이터 갱신" 요청 시
- **커스텀 필드 조회**: `jira-get-project-meta --include-global`로 조회

### 에픽/스프린트 (MEMORY.md 캐시 — 수동 관리)

- 에픽 목록: `jira-get-epics` 스킬로 탐색 (사용자 동의 후)
- 보드 ID / 활성 스프린트 ID: `jira-get-sprints` 스킬로 탐색 (사용자 동의 후)
- **캐시 강제 갱신**: 사용자가 "에픽 다시 탐색", "스프린트 갱신" 등 명시 요청 시 재호출하여 덮어쓴다.

### 상태 전환 맵 (MEMORY.md 캐시 — 점진적 보강)

Jira 프로젝트마다 워크플로가 다르므로, 상태 전환 가능 목록을 MEMORY.md에 프로젝트별로 캐시한다.

**조회 방법**: `jira-update-issue` 스킬의 `--list-transitions` 옵션으로 특정 이슈의 현재 상태에서 전환 가능한 목록을 조회한다.

**캐시 형식**:
```
## 상태 전환 맵

### DP (프로젝트 키)
#### 해야 할 일
- 진행 중
- 완료

#### 진행 중
- 해야 할 일
- 완료

#### 완료
- 해야 할 일
```

**운용 정책**:
- **초기 수집**: 프로젝트에서 처음 상태 전환을 시도할 때, `--list-transitions`로 조회하여 MEMORY.md에 기록
- **점진적 보강**: 상태 전환 성공 시 응답에 포함된 `available_transitions`(전환 후 상태의 전환 가능 목록)을 MEMORY.md에 추가 기록
- **활용**: 상태 변경 요청 시 MEMORY.md의 전환 맵을 먼저 확인하여 올바른 상태명을 사용
- **갱신**: 사용자가 "전환 맵 갱신" 요청 시, 또는 캐시된 전환이 실패할 경우 해당 항목 삭제 후 재조회

### 캐시하지 않는 동적 데이터 (매 요청 시 fresh fetch)

- 티켓 목록, 티켓 상세 내용 및 최근 댓글
- 담당자, 상태 등 실시간 변경 가능 데이터
