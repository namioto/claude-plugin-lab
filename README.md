# claude-plugin-lab

> Experimental Claude Code plugin marketplace by namioto

Claude Code의 플러그인 시스템을 실험하고 커스텀 확장을 공유하는 실험적 마켓플레이스입니다.

## 설치

```
/plugin marketplace add namioto/claude-plugin-lab
```

## 플러그인 목록

| 이름 | 타입 | 설명 |
|------|------|------|
| [hello-world](./plugins/hello-world/) | agent | 최소 에이전트 구조 시연 |
| [commit-helper](./plugins/commit-helper/) | command | 커밋 메시지 자동 생성 |

## 플러그인 설치

마켓플레이스 추가 후 `/plugin` UI에서 선택하거나 직접 설치:

```
/plugin install hello-world@claude-plugin-lab
/plugin install commit-helper@claude-plugin-lab
```

## 사용법

### hello-world 에이전트
`/agents` 목록에서 **hello-world** 선택

### commit-helper 커맨드
```
/commit-helper
```

## 구조

```
claude-plugin-lab/
├── .claude-plugin/
│   └── marketplace.json     # 마켓플레이스 카탈로그
├── plugins/
│   ├── hello-world/         # 에이전트 예시
│   └── commit-helper/       # 커맨드 예시
└── .github/
    └── workflows/
        └── validate.yml     # JSON 유효성 검증 CI
```

## 기여

새 플러그인 추가를 환영합니다. [CONTRIBUTING.md](./CONTRIBUTING.md)를 참고하세요.

## 라이선스

MIT
