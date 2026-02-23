# ADF 노드 JSON 참조

SKILL.md의 변환 규칙 및 유효성 규칙을 보완하는 상세 JSON 예시 모음.
특정 노드 구조가 필요할 때 이 파일을 참조한다.

---

## 블록 노드

**paragraph:**
```json
{"type": "paragraph", "content": [{"type": "text", "text": "내용"}]}
```

**heading:**
```json
{"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "제목"}]}
```
`attrs.level`: 1 ~ 6

**bulletList:**
```json
{
  "type": "bulletList",
  "content": [{
    "type": "listItem",
    "content": [{"type": "paragraph", "content": [{"type": "text", "text": "항목"}]}]
  }]
}
```

**orderedList:**
```json
{
  "type": "orderedList",
  "attrs": {"order": 1},
  "content": [{
    "type": "listItem",
    "content": [{"type": "paragraph", "content": [{"type": "text", "text": "항목"}]}]
  }]
}
```
`attrs.order`: 목록 시작 번호 (기본값 1, 선택)

**codeBlock:**
```json
{"type": "codeBlock", "attrs": {"language": "javascript"}, "content": [{"type": "text", "text": "코드"}]}
```
지원 언어: `javascript`, `typescript`, `python`, `java`, `go`, `rust`, `bash`, `sql`, `json`, `yaml` 등 Prism 지원 언어. 미지원 언어는 `"text"` 사용.

**blockquote:**
```json
{
  "type": "blockquote",
  "content": [{"type": "paragraph", "content": [{"type": "text", "text": "인용문"}]}]
}
```

**rule:**
```json
{"type": "rule"}
```

**panel:**
```json
{
  "type": "panel",
  "attrs": {"panelType": "info"},
  "content": [{"type": "paragraph", "content": [{"type": "text", "text": "내용"}]}]
}
```
`attrs.panelType`: `"info"` | `"note"` | `"warning"` | `"error"` | `"success"`

**table:**
```json
{
  "type": "table",
  "content": [
    {
      "type": "tableRow",
      "content": [
        {"type": "tableHeader", "attrs": {"colspan": 1, "rowspan": 1}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "헤더"}]}]},
        {"type": "tableHeader", "attrs": {"colspan": 1, "rowspan": 1}, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "헤더2"}]}]}
      ]
    },
    {
      "type": "tableRow",
      "content": [
        {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "값"}]}]},
        {"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "값2"}]}]}
      ]
    }
  ]
}
```
`tableHeader` / `tableCell` 선택 attrs: `colspan` (number), `rowspan` (number)

**taskList / taskItem:**
```json
{
  "type": "taskList",
  "attrs": {"localId": "task-list-1"},
  "content": [
    {
      "type": "taskItem",
      "attrs": {"localId": "task-1", "state": "TODO"},
      "content": [{"type": "paragraph", "content": [{"type": "text", "text": "해야 할 일"}]}]
    },
    {
      "type": "taskItem",
      "attrs": {"localId": "task-2", "state": "DONE"},
      "content": [{"type": "paragraph", "content": [{"type": "text", "text": "완료된 일"}]}]
    }
  ]
}
```
`taskItem.attrs.state`: `"TODO"` | `"DONE"`. `localId`는 페이지 내 고유 문자열.

**decisionList / decisionItem:**
```json
{
  "type": "decisionList",
  "attrs": {"localId": "decision-list-1"},
  "content": [
    {
      "type": "decisionItem",
      "attrs": {"localId": "decision-1", "state": "DECIDED"},
      "content": [{"type": "paragraph", "content": [{"type": "text", "text": "결정 사항 내용"}]}]
    }
  ]
}
```

**expand (접기/펼치기 — Jira·Confluence·JSM 공통):**
```json
{
  "type": "expand",
  "attrs": {"title": "펼치기 제목"},
  "content": [
    {"type": "paragraph", "content": [{"type": "text", "text": "숨겨진 내용"}]}
  ]
}
```

**nestedExpand (tableCell / tableHeader 내부 전용):**
```json
{
  "type": "nestedExpand",
  "attrs": {"title": "중첩 펼치기"},
  "content": [{"type": "paragraph", "content": [{"type": "text", "text": "내용"}]}]
}
```

**mediaSingle + media (이미지 — 단일):**
```json
{
  "type": "mediaSingle",
  "attrs": {"layout": "center"},
  "content": [
    {
      "type": "media",
      "attrs": {
        "id": "media-file-id",
        "type": "file",
        "collection": "contentId-context",
        "width": 800,
        "height": 600
      }
    }
  ]
}
```
`mediaSingle.attrs.layout`: `"center"` | `"wide"` | `"full-width"` | `"wrap-left"` | `"wrap-right"` | `"align-start"` | `"align-end"`
외부 이미지 URL: `"type": "external"`, `"url": "https://..."` 사용

**mediaGroup (첨부파일 묶음 — 복수):**
```json
{
  "type": "mediaGroup",
  "content": [
    {
      "type": "media",
      "attrs": {
        "id": "media-file-id-1",
        "type": "file",
        "collection": "contentId-context",
        "width": 200,
        "height": 150
      }
    },
    {
      "type": "media",
      "attrs": {
        "id": "media-file-id-2",
        "type": "file",
        "collection": "contentId-context"
      }
    }
  ]
}
```

**blockCard (스마트 링크 — 블록):**
```json
{
  "type": "blockCard",
  "attrs": {"url": "https://..."}
}
```

---

## 인라인 노드

**mention:**
```json
{"type": "mention", "attrs": {"id": "account-id", "text": "@username", "userType": "DEFAULT"}}
```
`attrs.userType`: `"DEFAULT"` (일반 사용자) | `"ATLASSIAN"` | `"APP"` (봇/앱) — 선택

**emoji:**
```json
{"type": "emoji", "attrs": {"shortName": ":grinning:", "text": "😀"}}
```

**hardBreak (강제 줄바꿈):**
```json
{"type": "hardBreak"}
```

**date (인라인 날짜):**
```json
{"type": "date", "attrs": {"timestamp": "1582152559"}}
```
`attrs.timestamp`: Unix 타임스탬프 (초 단위 문자열). 사용자 로케일로 자동 표시됨.

**status (상태 로젠지):**
```json
{"type": "status", "attrs": {"text": "IN PROGRESS", "color": "blue", "localId": "uuid-here"}}
```
`attrs.color`: `"neutral"` | `"purple"` | `"blue"` | `"red"` | `"yellow"` | `"green"`

**inlineCard (스마트 링크 — 인라인):**
```json
{"type": "inlineCard", "attrs": {"url": "https://..."}}
```

---

## 마크(Mark) 참조

**strong (굵게):**
```json
{"type": "text", "text": "굵은 텍스트", "marks": [{"type": "strong"}]}
```

**em (기울임):**
```json
{"type": "text", "text": "기울임 텍스트", "marks": [{"type": "em"}]}
```

**strike (취소선):**
```json
{"type": "text", "text": "취소선", "marks": [{"type": "strike"}]}
```

**code (인라인 코드):**
```json
{"type": "text", "text": "const x = 1", "marks": [{"type": "code"}]}
```
`code` mark는 `textColor`와 동시 적용 불가.

**underline (밑줄):**
```json
{"type": "text", "text": "밑줄", "marks": [{"type": "underline"}]}
```

**link (하이퍼링크):**
```json
{"type": "text", "text": "링크텍스트", "marks": [{"type": "link", "attrs": {"href": "https://...", "title": "툴팁 제목"}}]}
```
`attrs.title`: 마우스오버 시 툴팁 텍스트 — 선택

**textColor (글자색):**
```json
{"type": "text", "text": "빨간 텍스트", "marks": [{"type": "textColor", "attrs": {"color": "#FF0000"}}]}
```

**backgroundColor (배경색):**
```json
{"type": "text", "text": "형광 배경", "marks": [{"type": "backgroundColor", "attrs": {"color": "#FFFF00"}}]}
```

**subsup (위첨자/아래첨자):**
```json
{"type": "text", "text": "2", "marks": [{"type": "subsup", "attrs": {"type": "sup"}}]}
```
`attrs.type`: `"sup"` (위첨자) | `"sub"` (아래첨자)

**복합 marks (bold + link):**
```json
{"type": "text", "text": "굵은 링크", "marks": [{"type": "strong"}, {"type": "link", "attrs": {"href": "https://..."}}]}
```
