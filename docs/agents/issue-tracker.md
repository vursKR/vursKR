# Issue tracker: GitHub

Issues, specs, and wayfinder maps for this repo live as GitHub issues on `vursKR/vursKR`.

The `gh` CLI is not available in Claude Code remote sessions. Use the GitHub MCP tools (`mcp__github__*`) for every operation below. When `gh` is available (local sessions), the `gh` commands in the skill docs work as written.

## Conventions

- **Create an issue**: `issue_write` with `method: create`.
- **Read an issue**: `issue_read` with `method: get`, then `get_comments` and `get_labels` as needed.
- **List issues**: `list_issues` with `state` and `labels` filters.
- **Comment on an issue**: `add_issue_comment`.
- **Apply / remove labels**: `issue_write` with `method: update` and the full `labels` list.
- **Close**: comment first, then `issue_write` with `method: update`, `state: closed`.

## Pull requests as a triage surface

**PRs as a request surface: no.** _(Set to `yes` if this repo treats external PRs as feature requests; `/triage` reads this flag.)_

## When a skill says "publish to the issue tracker"

Create a GitHub issue.

## When a skill says "fetch the relevant ticket"

`issue_read` with `method: get` plus `get_comments`.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single issue with **child** issues as tickets.

- **Map**: a single issue labelled `wayfinder:map`, holding the Destination / Notes / Decisions-so-far / Not yet specified / Out of scope body.
- **Child ticket**: a GitHub sub-issue of the map. Create it with `issue_write` and `parent_issue_number: <map>`. Labels: `wayfinder:<type>` (`research` / `prototype` / `grilling` / `task`). Once claimed, the ticket is assigned to the driving dev.
- **Blocking**: GitHub native issue dependencies are not reachable through the MCP tools, so this repo uses the body convention: a `Blocked by: #<n>, #<n>` line at the top of the child body. A ticket is unblocked when every issue on that line is closed.
- **Frontier query**: `issue_read` with `method: get_sub_issues` on the map, keep open children, drop any with an open issue in its `Blocked by` line or with an assignee. First in map order wins.
- **Claim**: `issue_write` with `method: update` and `assignees: ["<login>"]`, the session's first write.
- **Resolve**: post the answer with `add_issue_comment`, close with `issue_write`, then append a context pointer (gist + link) to the map's Decisions-so-far.
- **Research findings**: written to `docs/research/<name>.md` on the working branch and linked from the ticket's resolution comment.
