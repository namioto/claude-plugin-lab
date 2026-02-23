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

## 에이전트 프론트매터 (agents/*.md)

`name`과 `description`은 필수입니다.

```yaml
---
name: my-agent
description: Claude가 이 에이전트를 언제 호출해야 하는지 설명. 구체적일수록 좋음.
model: haiku        # sonnet | opus | haiku | inherit (기본값: inherit)
color: cyan         # UI에서 에이전트를 구분하는 배경색
tools: Read, Bash   # 허용할 도구 목록 (생략 시 전체 상속)
disallowedTools: Write, Edit  # 금지할 도구 목록
permissionMode: default       # default | acceptEdits | dontAsk | bypassPermissions | plan
maxTurns: 10        # 최대 에이전트 턴 수
memory: user        # user | project | local (지속 메모리 범위)
background: false   # true로 설정 시 항상 백그라운드 실행
isolation: worktree # worktree로 설정 시 독립 git worktree에서 실행
---
```

## 커맨드/스킬 프론트매터 (commands/*.md, skills/*/SKILL.md)

```yaml
---
name: my-command              # 생략 시 파일명/디렉토리명 사용
description: 이 스킬의 용도. Claude가 자동 실행 여부를 판단하는 기준.
disable-model-invocation: true  # true: 사용자만 수동 호출 가능 (커밋·배포 등 부작용 있는 워크플로우에 필수)
user-invocable: false           # false: / 메뉴에서 숨김 (Claude 전용 백그라운드 지식)
allowed-tools: Bash             # 이 스킬 실행 중 허용할 도구
argument-hint: "[issue-number]" # 자동완성에 표시되는 인자 힌트
model: sonnet                   # 이 스킬 실행 시 사용할 모델
context: fork                   # fork: 독립된 서브에이전트 컨텍스트에서 실행
agent: Explore                  # context: fork 시 사용할 에이전트 타입
---
```

> **핵심 규칙**: `/commit`, `/deploy` 등 부작용이 있는 워크플로우는 반드시 `disable-model-invocation: true`를 설정하세요. 설정하지 않으면 Claude가 상황을 판단해 자동 실행할 수 있습니다.

## 기여 절차

1. 이 저장소를 Fork
2. `plugins/<plugin-name>/` 디렉토리 생성
3. 위 구조에 맞게 파일 작성
4. `.claude-plugin/marketplace.json`의 `plugins` 배열에 항목 추가
5. PR 제출

## PR 체크리스트

- [ ] `plugin.json` 에 `name`, `description`, `version`, `author` 포함
- [ ] 에이전트 파일에 `name`, `description` 프론트매터 포함
- [ ] 커맨드/스킬 파일에 `description` 프론트매터 포함
- [ ] 부작용 있는 커맨드에 `disable-model-invocation: true` 설정
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
