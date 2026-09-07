# vursKR

공모전 자동화 시스템: 참여 가능한 공모전 리서치, 응모작 작성, 자동 응모, 피드백 적립.

## Agent skills

### Issue tracker

Issues live in this repo's GitHub Issues (`vursKR/vursKR`), driven through the GitHub MCP tools. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

### Contest skills

`contest-recon` (공고 해부, 발주처 기존사업 스캔, 배점 역산) and `contest-redteam` (제출 전 적대적 검증) are the user's synced personal skills. Every writing-stage session consults both.
