# commit-helper

git diff를 분석해 의미 있는 커밋 메시지를 자동으로 생성하는 슬래시 커맨드입니다.

## 설치

```
/plugin marketplace add namioto/claude-plugin-lab
/plugin install commit-helper@claude-plugin-lab
```

## 사용법

```
/commit-helper
```

staged 변경사항이 있으면 즉시 커밋 메시지를 생성합니다.
staged 변경사항이 없으면 어떤 파일을 stage할지 제안합니다.

## 특징

- Conventional Commits 형식 지원 (`feat:`, `fix:`, `docs:` 등)
- 50자 이내 요약 + 필요시 상세 설명
- 명령형 어조 사용

## 구조

```
commit-helper/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── commit-helper.md   # 커맨드 프롬프트
└── README.md
```
