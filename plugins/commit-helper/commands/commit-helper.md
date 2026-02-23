Analyze the current git diff and staged changes, then generate a concise, meaningful commit message.

Steps:
1. Run `git diff --staged` to see staged changes
2. Run `git diff` to see unstaged changes (for context)
3. Run `git status` to understand the overall state

Based on the changes, generate a commit message following these conventions:
- Use imperative mood ("Add feature" not "Added feature")
- First line: 50 chars or less, summarizing what changed
- If needed, add a blank line followed by a detailed explanation
- Use conventional commits format when appropriate: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`

Output only the commit message, ready to use. Do not include backticks or quotes around it.

If there are no staged changes, suggest which files to stage based on the unstaged changes.
