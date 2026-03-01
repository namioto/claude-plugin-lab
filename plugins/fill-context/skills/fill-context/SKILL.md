---
name: fill-context
description: >
  This skill should be used when the user asks to "맥락 채워줘", "fill context",
  "context 보충해줘", "빠진 맥락 채워", "정보 보충해줘", "뭐가 더 필요해?",
  "what info do you need?", "ask me clarifying questions", "what's missing?",
  or when the user wants to remove ambiguity from a vague request by iteratively
  probing for background, motivation, and concrete details.
---

# Fill Context

Remove ambiguity from a vague or incomplete request by iteratively probing
the user for background, motivation, problem definition, and concrete action
items. Continue asking until the user signals they are satisfied.

This is NOT about filling in form fields (assignee, priority, etc.).
This IS about understanding WHY something needs to be done, WHAT problem
it solves, and HOW it should be approached.

## When NOT to Activate

- The request already contains clear background, motivation, and concrete details
- The user explicitly says to skip questions and just execute

## Process

### 1. Identify the Core Request

Examine the user's message and extract the surface-level request.
For example: "사용자 인증 개선 Jira 티켓 만들어줘" — the surface request
is a Jira ticket, but the real work is understanding what "사용자 인증 개선"
means in depth.

### 2. Probe Depth-First

Ask questions that go deeper into the request, not wider. Follow this
priority order:

#### Round 1: Background & Problem

- **Why**: Why does this need to happen? What triggered this?
- **Problem**: What is the current pain point or failure? Who is affected?

#### Round 2: Desired Outcome

- **Goal**: What does success look like concretely?
- **Scope**: What is in scope and what is explicitly out of scope?

#### Round 3: Approach & Actions

- **Tasks**: What specific work needs to be done?
- **Dependencies**: What needs to happen first? What is blocked?
- **Risks**: What could go wrong? Any concerns?

#### Additional Rounds

Continue probing based on the user's answers. Each answer may reveal
new areas that need clarification. Keep asking until:

- The user says "됐어", "그만", "충분해", "enough", or similar
- The user's answers become short confirmations with no new information
- All critical ambiguity has been resolved

### 3. Questioning Rules

- Use `AskUserQuestion` to ask multiple related questions in one round
  (max 4 questions per round). Group questions from the same probe round together.
- Each question should build on previous answers, digging deeper
- Rephrase vague answers back to the user for confirmation:
  "~라는 말씀이신가요?" / "구체적으로 어떤 상황인지 예시를 들어주실 수 있나요?"
- Do NOT ask about operational details (assignee, priority, sprint)
  — those are decisions, not context
- Match the language the user is communicating in

### 4. Clarify Jargon and Proper Nouns

When the user mentions project names, system names, abbreviations, or
internal terms (e.g., "dp-admin", "auth-gateway"), ask whether:

- The term should be used as-is (audience already knows it)
- A brief explanation should be added so others can understand

This ensures the final output is readable by its intended audience,
not just the person who made the request.

### 5. Share Progress Between Rounds

After every 2-3 rounds of questions, present a running summary of what
has been gathered so far. Format as a concise bullet list:

```
지금까지 정리된 내용:
- **배경**: ...
- **문제**: ...
- **목표**: ...
```

Ask the user to confirm, correct, or add to the summary before continuing
with the next round. This prevents misunderstandings from accumulating
and gives the user a sense of progress.

### 6. Compile the Result

After the user signals completion, compile all gathered information into
a structured summary:

```
## Context Summary

### Background
[Why this is needed, what triggered it]

### Problem
[Current pain point, who is affected, concrete examples]

### Goal
[What success looks like, desired outcome]

### Scope
[What is in / out of scope]

### Action Items
[Specific work to be done, broken down into concrete steps]

### Risks & Dependencies
[What could go wrong, what needs to happen first]
```

Include only sections where meaningful information was gathered.

Present the summary to the user for confirmation. If the user corrects
or adds anything, update accordingly. Then proceed with the original task
using this enriched context.
