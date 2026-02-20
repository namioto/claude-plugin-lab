# Contributing to claude-plugin-lab

플러그인 기여 방법 안내입니다.

## 플러그인 구조

새 플러그인은 `plugins/<plugin-name>/` 디렉토리에 추가합니다.

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json          # 필수: 플러그인 메타데이터
├── agents/                  # 선택: 커스텀 에이전트 (.md)
├── commands/                # 선택: 슬래시 커맨드 (.md)
├── skills/                  # 선택: 에이전트 스킬
│   └── <skill-name>/
│       └── SKILL.md
├── hooks/
│   └── hooks.json           # 선택: 이벤트 훅
├── .mcp.json                # 선택: MCP 서버 설정
└── README.md                # 권장: 사용 방법 설명
```

## plugin.json 필수 필드

```json
{
  "name": "my-plugin",
  "description": "플러그인 설명",
  "version": "0.1.0",
  "author": { "name": "your-github-username" }
}
```

## 기여 절차

1. 이 저장소를 Fork
2. `plugins/<plugin-name>/` 디렉토리 생성
3. 위 구조에 맞게 파일 작성
4. `.claude-plugin/marketplace.json`의 `plugins` 배열에 항목 추가
5. PR 제출

## PR 체크리스트

- [ ] `plugin.json` 에 `name`, `description`, `version`, `author` 포함
- [ ] `marketplace.json` 에 플러그인 항목 추가
- [ ] `README.md` 에 설치 방법과 사용법 설명
- [ ] 모든 JSON 파일 문법 검증 완료

## 네이밍 규칙

- 플러그인 이름: `kebab-case` (소문자, 하이픈)
- 커맨드 파일: `<command-name>.md`
- 에이전트 파일: `<agent-name>.md`
- 스킬 디렉토리: `<skill-name>/SKILL.md` (SKILL.md는 대문자 필수)

## 버전 규칙

[Semantic Versioning](https://semver.org/) 사용:
- `0.x.x` — 실험적/개발 중
- `1.0.0` — 안정 버전
