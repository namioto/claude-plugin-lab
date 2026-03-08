---
description: "alfred 에이전트가 Confluence 페이지 생성/업데이트/조회 작업을 수행할 때 호출하는 오케스트레이터 스킬. 페이지 배치 위치, 스페이스 구조 등의 메모리를 관리하며, adf-composer 스킬과 연계하여 ADF 문서를 생성한다."
user-invocable: false
---

# Confluence Orchestrator

Confluence 페이지 생성, 업데이트, 조회를 수행하고, 스페이스 구조와 페이지 배치 정보를 메모리로 관리한다.

## 시작 절차 (매 호출 시 필수)

1. MEMORY.md 읽기: `~/.claude/agent-memory/confluence/MEMORY.md` → PLACEMENT_GUIDE 확인
2. PLACEMENT_GUIDE가 비어 있으면: Bash(curl)로 스페이스 구조 탐색 후 MEMORY.md에 기록
3. 요청 처리

## 담당 API

| 작업 | 엔드포인트 |
|------|-----------|
| 페이지 생성 | POST /wiki/rest/api/content |
| 페이지 업데이트 | PUT /wiki/rest/api/content/{pageId} |
| 페이지 조회 | GET /wiki/rest/api/content?spaceKey={key}&title={title} |
| 스페이스 구조 | GET /wiki/rest/api/space/{key}/content?depth=all&limit=50 |
| 스페이스 목록 | GET /wiki/rest/api/space?limit=50 |
| 페이지 자식 | GET /wiki/rest/api/content/{id}/child/page |

## 인증 패턴

URL은 환경변수 `$ATLASSIAN_URL`. 후행 `/` 제거.

```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_KEY" -H "Accept: application/json" -H "Content-Type: application/json" "$ATLASSIAN_URL/wiki/rest/..."
```

## 메모리 정책

- 캐시: PLACEMENT_GUIDE (스페이스 구조, 페이지 계층, 주요 pageId), 스페이스 메타
- 동적 (fresh fetch): 페이지 version.number, 최근 변경 이력
- 캐시 갱신: 사용자 명시 요청 시

## 페이지 생성 절차

1. PLACEMENT_GUIDE에서 parent page와 pageId 확인
2. adf-composer 스킬 호출 (doc_type: page) → ADF JSON
3. POST 실행. representation: "atlas_doc_format"
4. 생성된 페이지 URL 반환

페이지 생성 페이로드:

```json
{
  "type": "page",
  "title": "{제목}",
  "space": { "key": "{space_key}" },
  "ancestors": [{ "id": "{parent_pageId}" }],
  "body": {
    "atlas_doc_format": {
      "representation": "atlas_doc_format",
      "value": "{adf-composer 반환값 (JSON 문자열)}"
    }
  }
}
```

## 페이지 업데이트 절차

1. GET으로 현재 version.number 확인
2. adf-composer 스킬 호출
3. PUT 요청 시 version.number +1

페이지 업데이트 페이로드:

```json
{
  "version": { "number": "{현재번호 + 1}" },
  "title": "{제목}",
  "type": "page",
  "body": {
    "atlas_doc_format": {
      "representation": "atlas_doc_format",
      "value": "{adf-composer 반환값}"
    }
  }
}
```
