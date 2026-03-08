---
description: "alfred 에이전트가 Jira Service Management(JSM) 서비스 요청 생성/조회, 서비스 카탈로그 탐색 작업을 수행할 때 호출하는 오케스트레이터 스킬. 서비스데스크 메타, 서비스 카탈로그 등의 메모리를 관리한다. 사용자가 '서데'라고 축약할 수 있다."
user-invocable: false
---

# JSM Orchestrator

JSM 서비스 요청 생성, 조회, 댓글 작성을 수행하고, 서비스데스크 메타와 서비스 카탈로그 정보를 메모리로 관리한다.

## 시작 절차 (매 호출 시 필수)

1. MEMORY.md 읽기: `~/.claude/agent-memory/jsm/MEMORY.md`
   - 서비스데스크 메타 비어 있으면 → API 탐색
   - 서비스 카탈로그 비어 있으면 → API 탐색
2. 요청 처리

## 담당 API

| 작업 | 엔드포인트 |
|------|-----------|
| 서비스데스크 목록 | GET /rest/servicedeskapi/servicedesk |
| 서비스 카탈로그 | GET /rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype |
| 요청 생성 | POST /rest/servicedeskapi/request |
| 요청 목록 조회 | GET /rest/servicedeskapi/request?serviceDeskId={id} |
| 요청 상세 | GET /rest/servicedeskapi/request/{issueIdOrKey} |
| 요청에 댓글 | POST /rest/servicedeskapi/request/{issueIdOrKey}/comment |

## 인증 패턴

servicedeskapi는 추가 헤더 `X-ExperimentalApi: opt-in` 필요.
URL은 환경변수 `$ATLASSIAN_URL`. 후행 `/` 제거. 프로젝트 키: `$JSM_PROJECT`.

```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_KEY" -H "Accept: application/json" -H "Content-Type: application/json" -H "X-ExperimentalApi: opt-in" "$ATLASSIAN_URL/rest/servicedeskapi/..."
```

## 메모리 정책

- 캐시: 서비스데스크 메타 ($JSM_PROJECT의 serviceDeskId, 프로젝트명), 서비스 카탈로그 (requestTypeId, 이름, 설명)
- 동적 (fresh fetch): 현재 요청 목록/상태, 요청 상세/댓글
- 캐시 갱신: 사용자 명시 요청 시

## 서비스데스크 탐색 절차

1. GET /rest/servicedeskapi/servicedesk로 전체 목록
2. $JSM_PROJECT와 일치하는 serviceDeskId 확인
3. GET requesttype으로 요청 유형 목록 조회
4. MEMORY.md에 기록

## 요청 생성 절차

1. MEMORY.md 카탈로그에서 requestTypeId 확인
2. adf-composer 스킬 호출 (doc_type: request_description) → ADF JSON
3. ADF를 description에 삽입
4. POST 실행
5. 생성된 요청 key와 URL을 사용자에게 반환

요청 생성 페이로드:

```json
{
  "serviceDeskId": "{serviceDeskId}",
  "requestTypeId": "{requestTypeId}",
  "requestFieldValues": {
    "summary": "{요약}",
    "description": "{adf-composer 반환값}"
  }
}
```
