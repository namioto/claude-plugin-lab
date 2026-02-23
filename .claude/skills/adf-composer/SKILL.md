---
description: "Jira, Confluence, JSM, JPD 서브에이전트가 이슈 생성/수정, 페이지 작성, 댓글, 요청 본문 등 ADF 필드를 포함한 write 작업을 수행하기 전에 반드시 사용해야 하는 스킬. 마크다운 형식 입력을 유효한 ADF JSON으로 변환해 반환한다. 사용자가 직접 호출하지 않으며, 서비스 서브에이전트가 write 요청 시 위임하여 호출한다."
user-invocable: false
context: fork
---

# ADF Composer

구조화된 마크다운 명세를 받아 유효한 Atlassian Document Format(ADF) JSON을 반환한다.

## 입력 형식

다음 구조의 입력을 받아 처리한다:

```
[TARGET]
service: jira | confluence | jsm | jpd
doc_type: issue_description | page | comment | request_description

[CONTENT]
(마크다운 형식 내용)

[METADATA]
mentions: [@name: account-id]  # 선택
links: [표시텍스트: URL]        # 선택
```

## 처리 절차

1. `[TARGET]` 블록에서 `service`와 `doc_type`을 확인한다
2. 서비스 지원 범위 표를 참조해 사용 가능한 노드를 결정한다
3. `[METADATA]` 블록이 있으면 mention 매핑 테이블을 구성한다
   — METADATA에 없는 `@username`은 `id`를 빈 문자열로, `text`에 원본 문자열을 유지한다
4. `[CONTENT]` 블록의 마크다운을 아래 변환 규칙에 따라 ADF 노드로 변환한다
5. 유효성 규칙을 검증한다 (빈 content 배열, 잘못된 자식 노드, 서비스 미지원 노드 등)
6. 최상위 `doc` 구조로 감싸 순수 JSON을 출력한다

## 출력 규칙

- 순수 ADF JSON 객체만 반환한다
- 코드 펜스(` ``` `) 없음
- 설명 텍스트 없음
- JSON 객체 단독 출력

## ADF 최상위 구조

```json
{
  "version": 1,
  "type": "doc",
  "content": []
}
```

`content` 배열에 블록 노드를 순서대로 배치한다.

## 마크다운 → ADF 변환 규칙

| 마크다운 | ADF 노드 |
|---------|---------|
| `# H1` ~ `###### H6` | `heading` (level 1–6) |
| `**bold**` | `text` + `strong` mark |
| `*italic*` | `text` + `em` mark |
| `~~strikethrough~~` | `text` + `strike` mark |
| `` `inline code` `` | `text` + `code` mark |
| `__underline__` | `text` + `underline` mark |
| `- item` | `bulletList` > `listItem` > `paragraph` |
| `1. item` | `orderedList` > `listItem` > `paragraph` |
| ` ```lang\ncode\n``` ` | `codeBlock` (attrs.language) |
| `\| table \|` | `table` > `tableRow` > `tableHeader` / `tableCell` |
| `> quote` | `blockquote` > `paragraph` |
| `---` | `rule` |
| `[INFO] 텍스트` | `panel` (panelType: info) |
| `[WARNING] 텍스트` | `panel` (panelType: warning) |
| `[NOTE] 텍스트` | `panel` (panelType: note) |
| `[SUCCESS] 텍스트` | `panel` (panelType: success) |
| `[ERROR] 텍스트` | `panel` (panelType: error) |
| `@username` | `mention` (METADATA에서 account-id 조회) |
| `[text](url)` | `text` + `link` mark |
| `- [ ] item` | `taskList` > `taskItem` (미완료, `state: "TODO"`) |
| `- [x] item` | `taskList` > `taskItem` (완료, `state: "DONE"`) |
| `[EXPAND title]...[/EXPAND]` | `expand` |
| `[DATE 2024-01-15]` | `date` (attrs.timestamp: Unix 초 단위 문자열) |
| `\` (줄 끝) 또는 `<br>` | `hardBreak` |
| 빈 줄로 구분된 텍스트 | `paragraph` |

## ADF 유효성 규칙

- `doc` 직접 자식: 블록 노드만 허용 (paragraph, heading, bulletList, orderedList, codeBlock, table, blockquote, rule, panel, taskList, decisionList, expand, mediaSingle, mediaGroup, blockCard)
- `nestedExpand`는 `tableCell` / `tableHeader` 내부에만 배치 가능
- `taskItem` / `decisionItem`은 반드시 `localId` attr 포함
- `mediaSingle` 자식: `media` 노드 단 하나만 허용
- `mediaGroup` 자식: `media` 노드 하나 이상 허용
- `paragraph` 자식: 인라인 노드만 허용 (text, mention, hardBreak, emoji, date, status, inlineCard)
- `listItem`은 반드시 블록 노드(paragraph 등)를 감싸야 함
- `tableRow`는 `tableHeader` 또는 `tableCell`만 포함
- `code` mark는 `textColor` mark와 동시 적용 불가
- 빈 `content` 배열 금지

## 서비스별 노드 지원 범위

| 노드 / 마크 | Jira | Confluence | JSM | JPD |
|------------|:----:|:----------:|:---:|:---:|
| paragraph, heading, lists, codeBlock, blockquote, rule | ✅ | ✅ | ✅ | ✅ |
| table | ✅ | ✅ | ✅ | ✅ |
| panel | ✅ | ✅ | ✅ | ✅ |
| taskList / taskItem | ✅ | ✅ | ✅ | ✅ |
| decisionList / decisionItem | ✅ | ✅ | — | — |
| expand | ✅ | ✅ | ✅ | — |
| nestedExpand | — | ✅ | — | — |
| mediaSingle / mediaGroup / media | ✅ | ✅ | ✅ | — |
| blockCard / inlineCard | ✅ | ✅ | ✅ | — |
| date / status / emoji | ✅ | ✅ | ✅ | — |
| mention | ✅ | ✅ | ✅ | — |
| strong, em, strike, code, underline, link, subsup | ✅ | ✅ | ✅ | ✅ |
| textColor / backgroundColor | ✅ | ✅ | — | — |

`nestedExpand`는 `tableCell` / `tableHeader` 내부에서만 사용 가능하며, 최상위 `doc` 직접 자식으로 배치 불가.

## 노드 구조 참조

각 노드 및 마크의 상세 JSON 예시는 **`references/adf-nodes.md`** 를 참조한다.
