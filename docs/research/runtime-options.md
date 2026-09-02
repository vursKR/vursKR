# 공모전 리서치 정기 실행 런타임 비교

조사 기준: 2026-09-02. 출처는 code.claude.com/docs 와 github.com/anthropics/claude-code-action 공식 문서로 한정. 문서에서 확인하지 못한 항목은 "확인되지 않음"으로 표기.

## 요약

- 정기 실행 후보는 네 가지: (1) Claude Code on the web의 Routines, (2) CLI `/loop` 및 Desktop 로컬 스케줄 태스크, (3) Agent SDK로 직접 만드는 스케줄러, (4) GitHub Actions의 `schedule` 트리거.
- Gmail·Google Calendar·Slack 커넥터를 별도 OAuth 구현 없이 무인 실행에서 쓸 수 있는 경로는 Routines가 유일하다. 최소 간격 1시간, 하루 실행 횟수 상한이 있다.
- Agent SDK와 GitHub Actions는 API 키 기반이며 claude.ai 커넥터를 쓸 수 없고, Gmail 등 Anthropic 호스팅 커넥터는 로컬 OAuth 자체를 지원하지 않는다.
- Playwright 브라우저 자동화는 어느 런타임 문서에도 "사전 설치된 Chromium"이 명시되어 있지 않다. 클라우드 VM 설치 도구 목록에는 `chromedriver`만 있고 Chrome/Chromium 항목은 없다.
- 결론: 리서치 단계는 Routines(Trusted 또는 Custom 네트워크 + Slack/Gmail 커넥터), 응모 단계(브라우저 폼 제출 등)는 로컬 CLI + Chrome 확장 또는 Desktop 스케줄 태스크가 현실적이다.

## 런타임 비교 표

| 항목 | Routines (web) | CLI `/loop` / Desktop 태스크 | Agent SDK 자체 스케줄러 | GitHub Actions |
|---|---|---|---|---|
| 스케줄 | 프리셋(hourly/daily/weekdays/weekly) + `/schedule update`로 cron, 최소 1시간, 1회성 가능 [R] | `/loop` 최소 1분, 7일 후 자동 만료, 세션 열려 있어야 함 [ST]; Desktop 최소 1분, 앱 실행 중·컴퓨터 깨어 있어야 함 [DT] | 스케줄 기능 없음. 외부 cron/Docker/K8s에서 `query()` 호출 [SDK-H] | `on: schedule` cron 지원. 기본 브랜치에서만, public repo는 60일 비활성 시 중지 [GA] |
| 커넥터 | claude.ai 커넥터 전부 기본 포함, 실행 중 승인 없이 쓰기까지 허용 [R] | CLI: claude.ai 로그인 시 커넥터 자동 로드 [MCP]; Desktop: 설정 파일 + 커넥터 [DT] | `mcpServers` 옵션으로 stdio/HTTP/SSE/in-process. claude.ai 커넥터 불가, OAuth 브라우저 플로우 없음 [SDK-MCP] | `claude_args: --mcp-config`로 MCP 추가. 내장 GitHub MCP 2종. claude.ai 커넥터 확인되지 않음 [GA][ACT-FAQ] |
| 브라우저 | 확인되지 않음(설치 도구 표에 Chrome/Chromium 없음, `chromedriver`만 존재) [CE] | Chrome 확장(`--chrome`)은 로컬 Chrome 필요, API 키 인증 시 비활성 [CH]; Playwright MCP는 "이미 설치된 Chrome"을 구동 [MQ] | 자체 컨테이너에 브라우저 설치하면 가능. 문서에 명시 없음 → 확인되지 않음 | 확인되지 않음(공식 문서·repo docs에 playwright 언급 없음) [ACT-USAGE] |
| 비밀 관리 | 환경변수는 환경 사용자 모두 열람 가능. API credentials는 프록시가 주입, 세션에서 값 안 보임 [CE] | 로컬 파일/환경변수(사용자 책임) | `ANTHROPIC_API_KEY` 환경변수, 프록시로 키 주입 권장 [SDK-H] | GitHub Secrets(`ANTHROPIC_API_KEY` 또는 `CLAUDE_CODE_OAUTH_TOKEN`), OIDC 페더레이션 가능 [GA] |
| 비용 모델 | 구독 사용량 차감 + 일일 실행 횟수 상한, VM 별도 과금 없음 [R][W] | 구독 사용량 | API 토큰 과금(구독 로그인 불허) + 컨테이너 비용 [SDK-O][SDK-H] | API 토큰 또는 구독 OAuth 토큰 + GitHub Actions 분 [GA] |
| 권한 프롬프트 | 없음(완전 자율) [R] | 세션 상속 / Desktop은 태스크별 모드 [ST][DT] | `default/dontAsk/acceptEdits/bypassPermissions/plan/auto` [SDK-P] | `--allowedTools` 또는 `settings`로 명시 허용 [GA] |

출처 약어: [W] https://code.claude.com/docs/en/claude-code-on-the-web · [R] https://code.claude.com/docs/en/routines · [CE] https://code.claude.com/docs/en/cloud-environments · [ST] https://code.claude.com/docs/en/scheduled-tasks · [DT] https://code.claude.com/docs/en/desktop-scheduled-tasks · [MCP] https://code.claude.com/docs/en/mcp · [MQ] https://code.claude.com/docs/en/mcp-quickstart · [CH] https://code.claude.com/docs/en/chrome · [SDK-O] https://code.claude.com/docs/en/agent-sdk/overview · [SDK-MCP] https://code.claude.com/docs/en/agent-sdk/mcp · [SDK-P] https://code.claude.com/docs/en/agent-sdk/permissions · [SDK-H] https://code.claude.com/docs/en/agent-sdk/hosting · [SDK-Q] https://code.claude.com/docs/en/agent-sdk/quickstart · [GA] https://code.claude.com/docs/en/github-actions · [ACT-USAGE] https://github.com/anthropics/claude-code-action/blob/main/docs/usage.md · [ACT-SEC] https://github.com/anthropics/claude-code-action/blob/main/docs/security.md · [ACT-SOL] https://github.com/anthropics/claude-code-action/blob/main/docs/solutions.md · [ACT-FAQ] https://github.com/anthropics/claude-code-action/blob/main/docs/faq.md · [PM] https://code.claude.com/docs/en/permission-modes · [WQ] https://code.claude.com/docs/en/web-quickstart · [MB] https://code.claude.com/docs/en/mobile

## 런타임별 상세

### 1. Claude Code on the web + Routines

**Routines 기능** ([R])
- "A routine is a saved Claude Code configuration: a prompt, one or more repositories, and a set of connectors". 트리거는 Scheduled / API(HTTP POST + bearer token) / GitHub 이벤트 세 종류이며 조합 가능.
- 연구 프리뷰(research preview). Pro, Max, Team, Enterprise에서 사용. claude.ai/code/routines 또는 CLI `/schedule`로 생성.
- "Routines run autonomously as full Claude Code cloud sessions: there is no permission-mode picker and no approval prompts during a run."
- 매 실행마다 새 세션이 생성되고 저장소는 기본 브랜치에서 fresh clone. 결과는 세션 목록에 남는다.
- 실행 상태 녹색은 "인프라 오류 없이 종료"만 뜻하며 작업 성공을 보장하지 않으므로 트랜스크립트 확인 필요.

**최소 실행 간격** ([R])
- "The minimum interval is one hour; expressions that run more frequently are rejected." 프리셋은 hourly, daily, weekdays, weekly. 커스텀 cron은 `/schedule update`로 지정.
- "Runs may start a few minutes after the scheduled time due to stagger."
- 1회성(one-off) 실행은 일일 캡에 포함되지 않음.

**네트워크 정책** ([CE] Access levels)
- 네 단계: **None**(세션 네트워크로 외부 접근 없음) / **Trusted**(패키지 레지스트리·GitHub·클라우드 SDK 등 허용 목록만) / **Full**(모든 도메인) / **Custom**(자체 허용 목록, 기본 목록 포함 선택 가능).
- Trusted에서 허용 목록 밖 호스트는 `403`, `x-deny-reason: host_not_allowed` ([R]).
- 어떤 레벨이든 GitHub 프록시, MCP 커넥터 트래픽, API credentials에 등록한 호스트, Anthropic API는 별도 경로로 도달.
- 공모전 사이트 크롤링은 Trusted로는 불가. Custom에 도메인을 나열하거나 Full로 열어야 한다.

**세션 컨테이너 수명** ([W][CE])
- "Cloud sessions stop after a period of inactivity and the session's VM is reclaimed." 구체 시간은 문서에 없음 → 확인되지 않음. 재오픈 시 대화 이력 복원되지만 실행 중이던 백그라운드 작업은 복원되지 않음.
- VM: Ubuntu 24.04 x86_64, 약 4 vCPU / 16 GB RAM / 30 GB 디스크. 세션마다 새 VM.
- setup script 결과는 약 7일 캐시. 스크립트는 약 5분 안에 끝나야 함.
- "There is no separate compute charge for the cloud VM." 사용량은 계정 전체 rate limit과 공유 ([W]).

**커넥터** ([R][MCP][CE])
- "Under Connectors at the bottom of the form, all of your connected MCP connectors are included by default." 커넥터 트래픽은 Anthropic 서버를 경유하므로 allowlist 수정 불필요.
- 문서에 명시된 커넥터 예: Slack, Linear, Google Drive([R] 관련 링크), Microsoft 365, Gmail, Google Calendar([MCP]). **Notion**은 커넥터 목록으로 명시된 문장이 없음(다만 [MQ]에서 "Sentry, Linear, and Notion run their MCP servers behind OAuth"로 원격 MCP 서버로 언급). Google Calendar·Gmail은 "Anthropic-hosted connectors"로 claude.ai에서만 연결 가능.
- 커넥터 동작은 본인 계정 명의: "Slack messages, Linear tickets, or other connector actions use your linked accounts".
- CLI `claude mcp add`로 넣은 로컬 서버는 Routine에 안 뜬다. 필요하면 claude.ai/customize/connectors에 커넥터로 등록하거나 저장소 `.mcp.json`에 커밋.

**비밀 관리** ([CE])
- 환경변수: "Anyone who uses the environment can read the values." 비밀 저장 금지 권고.
- API credentials: "Anthropic's agent proxy adds the key to requests for the hosts you list... The key never reaches Claude". 수정 불가(삭제 후 재등록), 조직 CMEK 사용 시 저장 불가.

**알림** — Routine 완료 푸시 알림에 대한 문서 서술은 없음 → 확인되지 않음. Slack 커넥터로 결과 게시는 예시 유스케이스로 명시("posts a summary to Slack") [R]. 모바일 푸시는 Remote Control·Dispatch 기준으로만 서술 [MB].

**권한 모드** — 웹 세션은 Accept edits / Plan / Auto만 제공, Bypass 불가. `defaultMode: "bypassPermissions"`나 `"dontAsk"`는 무시됨 [PM][WQ].

### 2. Claude Code CLI `/loop` · Desktop 스케줄 태스크

- `/loop <interval> <prompt>`: 최소 1분(초 단위는 분으로 올림), 세션 범위. "Tasks only fire while Claude Code is running and idle. Closing the terminal or letting the session exit stops them firing." 반복 태스크는 생성 7일 후 자동 만료. 세션당 최대 50개. 시간대는 로컬. jitter로 최대 30분 지연 [ST].
- `--resume`/`--continue`로 만료 전 태스크 복원 가능. 세션을 백그라운드로 보내면 터미널 없이 계속 실행 [ST].
- Desktop 로컬 태스크: 최소 1분, 앱이 열려 있고 컴퓨터가 깨어 있어야 함. 놓친 실행은 최근 1회만 catch-up. 태스크별 권한 모드, 로컬 파일·MCP·커넥터 접근 가능 [DT].
- 공식 비교표: Cloud(Routines) = "Requires machine on: No", Desktop/`/loop` = "Yes" [ST][DT].
- 커넥터: claude.ai 계정으로 로그인한 CLI에는 커넥터가 자동 로드. `ANTHROPIC_API_KEY` 등 API 인증 시 로드 안 됨 [MCP].
- 브라우저: `claude --chrome`은 로컬 Chrome/Edge + 확장 필요, Pro/Max/Team/Enterprise + `/login` 필수, API 키·`setup-token` 인증에서는 꺼짐, WSL 미지원 [CH]. Playwright MCP는 `npx @playwright/mcp@latest`로 추가하고 "Playwright drives whichever Chrome is already installed on your machine" [MQ].

### 3. Claude Agent SDK 직접 스케줄러

- 언어: "The SDK is available as a library for Python and TypeScript only." 다른 언어는 `claude -p --output-format json` 서브프로세스 [SDK-O]. Node 18+ / Python 3.10+ [SDK-Q].
- 인증: `ANTHROPIC_API_KEY` 또는 Bedrock/Vertex/Foundry. "Anthropic does not allow third party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK." → 구독 사용량 아닌 API 과금 [SDK-Q][SDK-O].
- MCP 연결: `mcpServers` 옵션 또는 `.mcp.json`. 전송은 stdio / `http` / `sse` / in-process SDK 서버. 인증은 `env` 또는 `headers`로 전달. "The SDK doesn't open a browser or run an interactive OAuth flow" — OAuth 토큰은 앱이 직접 확보해 헤더로 넘겨야 함 [SDK-MCP]. Gmail·Google Calendar는 로컬 OAuth 자체를 지원하지 않음 [MCP].
- 권한 모드: `default`, `dontAsk`, `acceptEdits`, `bypassPermissions`, `plan`, `auto`. 무인 실행은 `allowedTools` + `dontAsk` 조합 권장. `acceptEdits`는 MCP 도구를 자동 승인하지 않음 [SDK-P][SDK-MCP].
- 스케줄: SDK 자체에 스케줄러 없음. 문서는 Docker/K8s/Modal 배포와 ephemeral 컨테이너 패턴을 안내. "No top-level session timeout" → `maxTurns`로 상한 설정. 컨테이너당 1 GiB RAM / 1 CPU 시작점 [SDK-H].
- 비밀: `ANTHROPIC_API_KEY`는 시크릿 매니저에서 주입하거나 `ANTHROPIC_BASE_URL` 프록시로 키 외부 보관 권장 [SDK-H].
- CLI 대안: `claude --bare -p` + `--mcp-config` + `--permission-mode dontAsk`를 OS cron에서 호출. `--bare`는 구독 로그인을 읽지 않으므로 API 키 필요 [H].

### 4. GitHub Actions (claude-code-action)

- `schedule` 트리거: "With a prompt input, the Claude Code GitHub Action runs in automation mode on any GitHub event, including a cron schedule." 예시 `cron: "0 9 * * *"`. 기본 브랜치에서만 실행되며 public repo는 60일 비활성 시 스케줄이 꺼짐 [GA]. repo docs에도 주간 유지보수 cron 예시 존재 [ACT-SOL].
- 스케줄 실행의 actor 검사: 쓰기 권한 검사는 건너뛰지만 human-actor 검사는 적용. cron을 마지막으로 수정한 사용자가 봇이면 `allowed_bots`에 등록 필요 [GA]. "scheduled runs have no external actor" [ACT-SEC].
- 비밀 관리: `ANTHROPIC_API_KEY` 또는 `CLAUDE_CODE_OAUTH_TOKEN`(`claude setup-token`)을 GitHub Secrets에 저장. OAuth 토큰은 구독 사용량으로 과금. OIDC workload identity federation으로 장기 시크릿 없이 인증 가능. "Never commit API keys or OAuth tokens directly to your repository." [GA][ACT-SEC]
- MCP: `claude_args: "--mcp-config /path/to/config.json"`으로 추가. 옛 `mcp_config` 입력은 DEPRECATED [GA][ACT-USAGE]. 기본 제공 MCP는 GitHub MCP 서버와 파일 조작 서버 2종 [ACT-FAQ]. claude.ai 커넥터(Gmail/Slack 등) 사용 여부는 문서에 없음 → 확인되지 않음.
- 도구 권한: 평문 prompt는 `--allowedTools` 또는 `settings`의 `permissions.allow`로 명시 허용해야 셸·API 사용 가능 [GA].
- 비용: GitHub Actions 분 + API 토큰(또는 구독). `--max-turns`, workflow timeout 권장 [GA].
- 브라우저: 공식 문서·repo docs(usage/solutions/faq/security)에 playwright·browser 언급 없음 → 확인되지 않음. (GitHub 호스트 러너의 브라우저 사전 설치 여부는 조사 범위 밖.)

### 5. Playwright 가능 여부 종합

- Claude Code on the web: 설치 도구 표는 Python/Node(20·21·22, npm, yarn, pnpm, bun, eslint, prettier, **chromedriver**)/Ruby/PHP/Java/Go/Rust/C-C++/Docker/PostgreSQL/Redis/git·gh·jq 등. Chrome·Chromium·Playwright 항목 없음. "Chromium이 사전 설치되어 있다"는 문장은 문서에 존재하지 않음 → 확인되지 않음 [CE]. 설치는 setup script(약 5분 예산, Trusted 네트워크는 npm/PyPI 등만 허용)로 시도해야 하며, Playwright 브라우저 바이너리 다운로드 호스트가 기본 allowlist에 있는지는 확인되지 않음.
- 웹 세션은 저장소의 `.mcp.json`을 읽으므로 Playwright MCP(stdio)를 정의할 수는 있음 [MQ][CE]. 실제 헤드리스 구동 가능 여부는 문서에 없음.
- CLI 로컬: Playwright MCP 공식 예시 있음. 로컬 Chrome 필요 [MQ]. Chrome 확장 경로는 로그인 상태 공유·CAPTCHA 시 수동 개입 [CH].
- Agent SDK: 자체 컨테이너이므로 브라우저 설치는 사용자 몫. 문서 언급 없음.
- GitHub Actions: 문서 언급 없음.

## 후보 결론

### 리서치 단계(공고 수집·요약·알림)
1. **1순위: Routines.** 기계 꺼져도 실행, 권한 프롬프트 없음, Slack/Gmail/Google Calendar 커넥터를 별도 OAuth 없이 사용 [R]. 환경을 **Custom**으로 두고 공모전 사이트 도메인을 allowlist에 추가(Trusted로는 403) [CE]. 최소 간격 1시간이므로 하루 1~2회 실행이면 충분. 결과 게시는 Slack 커넥터 또는 저장소 `claude/` 브랜치 커밋으로. 제약: 일일 실행 캡, 연구 프리뷰, 실행 결과는 트랜스크립트로 검증 필요.
2. **2순위: GitHub Actions `schedule`.** 저장소에 결과를 남기는 구조에 적합. API 키/OAuth 토큰 시크릿 관리 명확. 커넥터 없이 Slack 알림을 하려면 별도 MCP 서버·웹훅을 `--mcp-config`로 구성해야 함 [GA].
3. **보조: Agent SDK.** 브라우저·자체 인프라가 꼭 필요할 때. API 과금, OAuth는 자체 구현 [SDK-MCP][SDK-Q].
4. **비추천: `/loop`.** 7일 만료·세션 유지 필요 [ST].

### 응모 단계(폼 제출·파일 업로드 등 브라우저 조작)
1. **1순위: 로컬 CLI + Chrome 확장(`claude --chrome`) 또는 Desktop 스케줄 태스크.** 로그인 상태 공유, 파일 업로드 지원, CAPTCHA 시 사람 개입 [CH][DT]. 완전 무인은 아니지만 응모는 사람 확인이 필요한 단계라 적합.
2. **2순위: Agent SDK + Playwright MCP를 자체 컨테이너에.** 무인 가능하나 브라우저 설치·인증 토큰 관리는 사용자 책임 [SDK-H].
3. **Routines는 보류.** Chromium 사전 설치가 확인되지 않고, 브라우저 자동화 공식 예시가 없음 [CE].

## 미확인 사항

- 클라우드 세션 idle 만료 시간의 구체 수치(문서는 "a period of inactivity"만 명시) [W].
- Routines의 일일 실행 캡 수치(문서는 claude.ai/code/routines에서 확인하라고만 안내) [R].
- Claude Code on the web VM에 Chrome/Chromium·Playwright 브라우저가 설치되어 있는지, 또는 setup script로 설치 가능한지(다운로드 호스트의 allowlist 포함 여부) [CE].
- Routine 완료 시 모바일 푸시 알림 지원 여부 [MB].
- Notion이 claude.ai 커넥터로 Routine에서 쓸 수 있는지(문서에 커넥터로 명시된 문장 없음) [R][MCP].
- GitHub Actions에서 claude.ai 커넥터 사용 가능 여부, 러너의 브라우저 사용 가능 여부 [GA][ACT-FAQ].
- Agent SDK 컨테이너에서 Playwright 실행에 관한 공식 가이드 존재 여부 [SDK-H].
