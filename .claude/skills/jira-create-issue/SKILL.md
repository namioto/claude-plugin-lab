---
description: "alfred-jira 에이전트가 새로운 Jira 티켓을 생성할 때 사용하는 스킬. ADF 형식의 description 포함 티켓 생성, 에픽 연결, 스프린트 할당이 필요한 상황에서 호출된다. 사용자가 직접 호출하지 않으며, alfred-jira 에이전트가 위임하여 호출한다."
user-invocable: false
context: fork
---

# Jira Create Issue

ADF JSON description을 포함한 새 Jira 티켓을 생성한다.

## 입력 형식

호출 시 다음 정보를 포함해야 한다:

```
[CONFIG]
project: {프로젝트 키, 예: DP}
summary: {티켓 제목}
type: {이슈 타입: Story | Task | Bug | Sub-task 등}
description_markdown: {선택사항: 마크다운 형식 본문}
epic_key: {선택사항: 에픽 키, 예: DP-10}
sprint_id: {선택사항: 스프린트 ID}
```

## 실행 절차

### 1단계: ADF 생성 (description이 있는 경우)

`description_markdown`이 제공된 경우, 먼저 `adf-composer` 스킬을 호출하여 ADF JSON을 생성한다:

```
[TARGET]
service: jira
doc_type: issue_description

[CONTENT]
{description_markdown 내용}
```

반환된 ADF JSON을 임시 파일에 저장한다:

```bash
# Windows
$env:TEMP\jira-desc-{timestamp}.json

# macOS/Linux
/tmp/jira-desc-{timestamp}.json
```

### 2단계: 티켓 생성 스크립트 실행

Bash 도구로 아래 명령을 실행한다:

```bash
# description 없는 경우
uv run .claude/scripts/jira/create_issue.py \
  --url "{url}" \
  --project "{project_key}" \
  --summary "{summary}" \
  --type "{issue_type}" \
  [--epic-key "{epic_key}"] \
  [--sprint-id {sprint_id}]

# description 있는 경우
uv run .claude/scripts/jira/create_issue.py \
  --url "{url}" \
  --project "{project_key}" \
  --summary "{summary}" \
  --type "{issue_type}" \
  --description-file "{temp_file_path}" \
  [--epic-key "{epic_key}"] \
  [--sprint-id {sprint_id}]
```

### 3단계: 임시 파일 정리

description 파일이 생성된 경우 실행 후 삭제한다:

```bash
# Windows
Remove-Item -Path "$env:TEMP\jira-desc-*.json" -Force

# macOS/Linux
rm -f /tmp/jira-desc-*.json
```

## 출력 형식

성공 시 생성된 티켓 정보 JSON을 stdout으로 반환한다:

```json
{
  "id": "10234",
  "key": "DP-125",
  "self": "https://company.atlassian.net/rest/api/3/issue/10234"
}
```

## 결과 보고 형식

alfred-jira는 생성 완료 후 다음 형식으로 보고한다:

```
생성 완료: DP-125 - {제목}
URL: {atlassian_url}/browse/DP-125
```

## 오류 처리

- 존재하지 않는 이슈 타입 지정 시 400 오류가 반환된다
- 에픽 키가 잘못된 경우에도 400 오류가 반환된다
- 오류 발생 시 임시 파일을 먼저 정리한 뒤 stderr 메시지를 alfred-jira에 전달한다
