---
description: "alfred 에이전트가 Jira Product Discovery(JPD) 아이디어 생성/조회/업데이트, 이니셔티브 관리 작업을 수행할 때 호출하는 오케스트레이터 스킬. JPD 프로젝트 메타, 이니셔티브 목록, 커스텀 필드 스키마 등의 메모리를 관리한다."
user-invocable: false
---

# JPD 오케스트레이터

Jira Product Discovery(JPD) 아이디어 생성·조회·업데이트 및 이니셔티브 관리를 수행한다.

## JPD 특징

- JPD 아이디어는 Jira 이슈로 저장 (issuetype: Idea)
- 이니셔티브는 별도 issuetype (Initiative)
- 아이디어-이니셔티브 연결은 커스텀 필드
- JPD 전용 API 없음, `/rest/api/3/issue`를 issuetype으로 구분
- JPD 프로젝트는 `typeKey=product_discovery`로 식별

## 시작 절차

1. MEMORY.md 읽기: `~/.claude/agent-memory/jpd/MEMORY.md`
   - JPD 프로젝트 메타 비어 있으면 → API 탐색
   - 이니셔티브 목록 비어 있으면 → JQL 탐색
   - 커스텀 필드 스키마 비어 있으면 → createmeta API 탐색
2. 요청 처리

## 담당 API

| 작업 | 엔드포인트 |
|------|----------|
| 아이디어 생성 | POST /rest/api/3/issue (issuetype: Idea) |
| 아이디어 조회 | GET /rest/api/3/search?jql=project={key} AND issuetype=Idea |
| 이니셔티브 조회 | GET /rest/api/3/search?jql=project={key} AND issuetype=Initiative |
| 아이디어 업데이트 | PUT /rest/api/3/issue/{issueIdOrKey} |
| JPD 프로젝트 탐색 | GET /rest/api/3/project/search?typeKey=product_discovery |
| 커스텀 필드 스키마 | GET /rest/api/3/issue/createmeta?projectKeys={key}&expand=projects.issuetypes.fields |

## 인증 패턴

URL: `$ATLASSIAN_URL` (후행 `/` 제거)

```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_KEY" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  "$ATLASSIAN_URL/rest/api/3/..."
```

## 메모리 정책

- **캐시**: JPD 프로젝트 키·ID, 이니셔티브 목록, 커스텀 필드 스키마
- **동적**: 현재 아이디어 목록/상태, 아이디어 상세
- **캐시 갱신**: 사용자 명시 요청 시

## 아이디어 생성 절차

1. 이니셔티브 목록에서 연결할 이니셔티브 확인. 불명확하면 사용자에게 확인
2. `adf-composer` 스킬 호출 (doc_type: issue_description) → ADF JSON
3. ADF를 description 필드에 삽입
4. POST 실행. 이니셔티브 연결 커스텀 필드도 포함
5. 생성된 아이디어 key와 URL 반환

아이디어 생성 페이로드:

```json
{
  "fields": {
    "project": { "key": "{jpd_project_key}" },
    "summary": "{아이디어 제목}",
    "issuetype": { "name": "Idea" },
    "description": "{adf-composer 반환값}",
    "{이니셔티브 연결 커스텀 필드}": { "key": "{initiative_key}" }
  }
}
```
