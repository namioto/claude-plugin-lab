# hello-world

Claude Code 플러그인 구조를 시연하는 최소한의 에이전트 예시입니다.

## 설치

```
/plugin marketplace add namioto/claude-plugin-lab
/plugin install hello-world@claude-plugin-lab
```

## 사용법

`/agents` 목록에서 **hello-world** 에이전트를 선택하거나, 대화 중에 에이전트를 직접 호출하세요.

이 에이전트는 다음을 안내합니다:
- Claude Code 플러그인 시스템 개요
- 에이전트, 커맨드, 훅, MCP 서버의 차이점
- 직접 플러그인을 만드는 방법

## 구조

```
hello-world/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   └── hello-world.md   # 에이전트 시스템 프롬프트
└── README.md
```
