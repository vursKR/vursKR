# 한국 공모전(정책·시정 제안) 접수 채널 조사와 자동 제출 가능성

조사일: 2026-09-02. 조사 환경 제약: 세션의 네트워크 정책상 wevity.com, epeople.go.kr, policies.google.com, developers.google.com, support.google.com, playwright.dev 등 대부분의 원문 페이지에 직접 접속할 수 없었다. 따라서 아래 인용은 (a) 직접 열람한 1차 자료(Gmail API discovery 문서, Playwright 공식 문서의 GitHub 원본)와 (b) 검색 엔진이 반환한 해당 공식 페이지의 본문 발췌로 구분해 표기했다. 발췌 기반 항목은 "(발췌)"로 표시했고, 원문 재확인을 권장한다. 확인 불가 항목은 "확인되지 않음"으로 남겼다.

## 요약

1. 공고 18건을 표본으로 세면 이메일 접수(8건)와 우편·방문(7건)이 가장 흔하고, 국민생각함 등 공공 플랫폼(5건), 주최 측 자체 사이트(5건), 네이버폼(3건), 구글폼(1건)이 뒤따른다. 위비티에서 직접 접수하는 사례는 0건이었다(위비티는 정보 포털).
2. 이메일 접수는 로그인·본인인증·CAPTCHA가 전혀 없어 Gmail API로 완전 자동화가 가능하다. 단 API 메시지 상한 35MiB(36,700,160바이트), 개인 계정 하루 500통 제한을 지킨다.
3. 국민생각함·국민참여입법센터·청년몽땅정보통 등 공공 플랫폼은 로그인(간편인증·휴대전화·공동인증서 등)이 필수라서, 본인인증을 자동화 대상에서 제외하는 전제에서는 "사람이 로그인한 세션을 재사용해 폼 입력·파일 첨부만 자동화"하는 조건부 가능 채널이다.
4. 구글폼은 설정에 따라 Google 로그인이 강제되고(파일 업로드 질문은 항상 로그인 필수), Google 약관이 서비스 방해·robots.txt 위반 자동 접근을 금지하므로 조건부이다. 네이버폼은 도움말 원문을 확인하지 못해 판정을 보류한다.
5. 우선 지원 순서는 이메일 → 주최 측 자체 웹폼(비로그인형) → 국민생각함(세션 재사용) → 구글폼 → 네이버폼 순이며, 우편·방문은 자동화 대상이 아니다.

## 1. 접수 유형 표(표본 공고 18건)

한 공고가 복수 채널을 허용하면 각 채널에 모두 계수했다.

| # | 공고명(주최) | 접수 채널(공고 원문 기준) | 근거 URL |
|---|---|---|---|
| 1 | 2026 정보보호 정책제안 공모전(과기정통부/KISIA) | 이메일(kucis@kisia.or.kr) | https://linkareer.com/activity/340070 , https://www.dailysecu.com/news/articleView.html?idxno=207833 |
| 2 | 2026 국민생각함 정책 아이디어 공모전(국민권익위) | 국민생각함 플랫폼(배너 클릭 또는 생각모음 검색, 서식 파일 첨부 필수) | https://www.epeople.go.kr/api/thk/pbsb/PbsbsrpnPrpslDetail.npaid?ideaRegNo=1AE-2603-0000819 |
| 3 | 2026 제1회 구리시 정책제안 공모전 | 온라인·전자우편·방문·우편 중 택1(우편은 마감일 소인 유효) | https://www.guri.go.kr/www/selectBbsNttView.do?bbsNo=41&key=389&nttNo=139510 , https://www.efnews.co.kr/news/articleView.html?idxno=111881 |
| 4 | 한국국학진흥원 개원 30주년 대국민 혁신 아이디어 공모 | 이메일 접수 | https://gsis.snu.ac.kr/31590/ |
| 5 | 2026 장흥군 정책제안 공모전 | 국민생각함(epeople redirect URL 안내) | https://www.wevity.com/index_university.php?c=find&s=_university&gbn=viewok&gp=10&ix=107526 , https://www.epeople.go.kr/cmmn/idea/redirect.do?ideaRegNo=1AE-2605-0000929 |
| 6 | 2026 상반기 이천시 정책제안 공모전 | 온라인(이메일 또는 국민생각함), 방문, 우편 | http://www.ic119.co.kr/news/articleView.html?idxno=1631 |
| 7 | 2026 서울특별시 규제혁신 아이디어 공모전 | 제안서·개인정보동의서·청렴서약서 제출. 채널은 확인되지 않음(원문 접근 불가) | https://mediahub.seoul.go.kr/gongmo/2000705 |
| 8 | 2026 기본사회위원회 정책 아이디어 공모전 | 사무국 이메일, 우편, 구글폼 | https://newsseoul.co.kr/news/view/1065579019280778 , https://www.wevity.com/index_university.php?c=find&s=_university&gbn=viewok&gp=5&ix=110214 |
| 9 | 2026 법제처 국민 아이디어 공모제 | 국민참여입법센터(opinion.lawmaking.go.kr) 게시판 온라인 접수 + 우편 | https://thinkyou.co.kr/contest/61323 , https://www.moleg.go.kr/board.es?mid=a10501000000&bid=0048&list_no=147522&act=view&nPage=1 |
| 10 | 시흥시 기본사회 정책 아이디어 공모전(2026) | 담당자 이메일(korea.kr) 또는 시청 방문 | https://www.metroseoul.co.kr/article/20260824500319 |
| 11 | 2026 화성형 기본사회 정책 공모전 | 우편 또는 이메일(hohobro@korea.kr), PDF+HWP 동시 제출 | http://www.cnbnews.com/news/articleView.html?idxno=789813 , https://thinkyou.co.kr/contest/62716/ |
| 12 | 2026 아산시 시민 정책 공모전 | 온라인(네이버폼, 국민생각함, 이메일), 방문, 우편 중 택1 | https://asan.go.kr/main/cms/?m_mode=view&no=131&pds_no=2026022608144703989&tb_nm=city_news_notice |
| 13 | 기획재정부 2026 경제성장전략 대국민 공모전 | 주최 측 자체 공모전 사이트 | https://www.growthtogether.co.kr/ , https://www.all-con.co.kr/hit/contest/3561 |
| 14 | 2026 기본사회위원회 슬로건 국민 공모전 | 네이버폼 | https://sotong.go.kr/front/epilogue/epilogueNewViewPage.do?bbs_id=13654294a93f4d94a7e817b185a834bc |
| 15 | 국민경제자문회의 청년 정책 아이디어 공모전 '내가 대통령이라면' | 네이버폼(https://naver.me/5K694k4S) | https://www.2030db.go.kr/user/ntt/BBS_0000000000000001/NTT_0000000000000684/selectNttDetail.do |
| 16 | 2026 서울시 시민참여예산 제안사업 공모 | 자체 누리집(yesan.seoul.go.kr) 온라인 + 우편·방문 | https://news.seoul.go.kr/gov/archives/565322 |
| 17 | 2026 서울청년정책네트워크 하반기 정책제안 참가 위원 모집 | 청년몽땅정보통 온라인 접수(서울시 통합회원) | https://www.wevity.com/index_university.php?c=find&s=_university&gub=1&cidx=27&gbn=viewok&gp=2&ix=107607 , https://youth.seoul.go.kr/userSeoulLogin.do |
| 18 | 기후에너지환경부 2026 AX 아이디어 경진대회 | 공모전 홈페이지 온라인 접수 메뉴 | https://ipstr.korea.ac.kr/bbs/cdc/522/268305/artclView.do |

유형별 집계(18건, 중복 계수):

| 접수 유형 | 건수 | 해당 번호 |
|---|---|---|
| 이메일 | 8 | 1, 3, 4, 6, 8, 10, 11, 12 |
| 우편·방문 | 7 | 3, 6, 9, 10, 11, 12, 16 |
| 공공 플랫폼(국민생각함 4, 국민참여입법센터 1) | 5 | 2, 5, 6, 12 / 9 |
| 주최 측 자체 사이트·웹폼 | 5 | 3(온라인, 세부 확인되지 않음), 13, 16, 17, 18 |
| 네이버폼 | 3 | 12, 14, 15 |
| 구글폼 | 1 | 8 |
| 위비티 등 공모전 포털 내 제출 | 0 | 위비티는 정보 제공 포털이며 실제 접수는 주최사에서 진행한다는 설명(2차 자료): https://fauremusicstudio.com/227 , https://www.datanet.co.kr/news/articleView.html?idxno=82877 |
| 채널 미확인 | 1 | 7 |

## 2. 유형별 로그인·본인인증·CAPTCHA 요구

| 유형 | 로그인 | 본인인증 | CAPTCHA | 근거 |
|---|---|---|---|---|
| 이메일 | 없음(발신 계정만) | 없음 | 없음 | 공고 1, 4, 10, 11의 접수 안내(위 표) |
| 국민생각함·국민신문고 | 필수. 회원가입 또는 소셜 로그인 | 실명확인 로그인, 금융인증서, 간편인증, 공동인증서, 아이핀, 휴대전화, 외국인등록번호, 디지털원패스, 카카오·네이버 SNS(발췌) | 확인되지 않음 | https://www.epeople.go.kr/nep/crtf/userLognIdPw.npaid , https://idea.epeople.go.kr/nep/crtf/userLogn.npaid?returnUrl=/nep/utilHistory/myOnln/myOnlnList.paid |
| 국민참여입법센터 | 필수. 아이디 로그인, 간편인증(민간인증서, 최초 1회 휴대폰 본인확인), SNS(카카오·네이버), 본인인증 로그인(발췌) | 간편인증·본인인증 로그인 시 필요 | 확인되지 않음 | https://opinion.lawmaking.go.kr/login , https://community.lawmaking.go.kr/advc/ntcItm/3274 |
| 청년몽땅정보통(서울시 통합회원) | 필수 | "본인확인을 통한 로그인 서비스"(발췌) | 확인되지 않음 | https://youth.seoul.go.kr/userSeoulLogin.do , https://www.seoul.go.kr/member/userlogin/loginCheck.do |
| 구글폼 | 작성자 설정에 따름. "응답 1회로 제한" 설정 시 Google 계정 로그인 필수(발췌) | 파일 업로드 질문은 "응답자가 Google 계정에 로그인해야" 함(발췌) | 공식 문서에서 확인되지 않음. 커뮤니티에 reCAPTCHA 표시 사례 문의가 존재 | https://support.google.com/a/users/answer/9302966?hl=ko , https://support.google.com/docs/answer/7322334?hl=ko , https://support.google.com/docs/thread/204773711/removing-captcha-on-a-google-form?hl=en |
| 네이버폼 | 확인되지 않음(help.naver.com 접근 불가, naver.com은 검색 크롤러 차단) | 확인되지 않음 | 확인되지 않음 | 공고 14, 15가 naver.me 링크로 접수 |
| 주최 측 자체 사이트 | 사이트별 상이(회원가입형·비회원형 혼재), 개별 확인 필요 | 사이트별 상이 | 확인되지 않음 | 공고 13, 16, 18 |
| 우편·방문 | 해당 없음 | 서류 서명 등 | 해당 없음 | 공고 3, 11, 16 |

## 3. 이용약관의 자동화·봇 관련 조항

### 국민신문고·국민생각함 이용약관(발췌)
출처: https://www.epeople.go.kr/nep/gdnc/TermsConditions.npaid (국민생각함도 같은 약관을 사용: http://idea.epeople.go.kr/nep/gdnc/TermsConditions.npaid)

- 제12조(이용자의 의무): "이용자는 국민신문고의 안정적인 운영에 지장을 주거나 줄 우려가 있는 일체의 행위를 하지 않아야 합니다."
- 같은 조: "이용자는 회원의 비밀번호 관리 소홀, 부정사용에 의하여 발생하는 모든 결과에 대한 책임을 부담하여야 합니다."
- 회원 정의: "회원이란 서비스를 이용하기 위하여 회원가입을 하거나 다른 서비스 아이디로 로그인(소셜 로그인 포함)을 한 개인(재외국민, 국내거주 외국인 포함), 단체, 공공기관"
- 운영 정책: "로그인 후 약 120분 동안 서비스 이용이 없으면 자동 로그아웃"
- "자동화", "매크로", "봇"을 직접 지칭하는 문구는 검색 결과에서 확인되지 않음. 다만 "안정적인 운영에 지장" 조항이 과도한 자동 요청을 포괄할 수 있다.

### Google 서비스 약관(구글폼에 적용)
출처: https://policies.google.com/terms?hl=en-US (한국어판: https://policies.google.com/terms?hl=ko)

- "You must not abuse, harm, interfere with, or disrupt our services or systems"
- 금지 행위 예시: "using automated means to access content from any of our services in violation of the machine-readable instructions on our web pages (for example, robots.txt files)"
- "accessing or using our services or content in fraudulent or deceptive ways" 금지
- 한국어판 발췌: 컴퓨터 판독 가능 지시(robots.txt 등)를 위반하는 자동화된 수단의 콘텐츠 접근 금지. 즉, 폼 응답 자동 제출 자체를 명시적으로 금지하는 문구는 없으나, 서비스 방해·기만적 이용·robots.txt 위반은 금지된다.

### 위비티(WEVITY) 이용약관
- 확인되지 않음. wevity.com과 미러(wevity.mireene.co.kr)는 본 세션에서 접속이 차단됐고, 검색 엔진에도 약관 본문이 색인되어 있지 않았다.
- 위비티가 자체 접수 기능을 제공한다는 근거도 찾지 못했다. 2차 자료는 위비티를 "공모전 정보를 제공하는 포털 사이트이며, 실제 접수는 각 공모전의 주최사 홈페이지에서 진행"한다고 설명한다(https://fauremusicstudio.com/227). 표본 18건 중 위비티에서 접수하는 공고는 없었다.

### 네이버폼 이용약관
- 확인되지 않음(네이버 도움말·약관 페이지 접근 불가, naver.com 도메인은 검색 크롤러 차단).

## 4. Playwright 기반 브라우저 자동화의 범위

전제: 본인인증(휴대폰·공동인증서 등)과 CAPTCHA는 자동화하지 않는다.

가능한 범위(Playwright 공식 문서, GitHub 원본을 직접 열람):
- 텍스트 입력: `locator.fill()`이 "focuses the element and triggers an input event with the entered text". 체크박스·라디오: `locator.setChecked()`. 셀렉트: `locator.selectOption()` — https://github.com/microsoft/playwright/blob/main/docs/src/input.md (게시본: https://playwright.dev/docs/input)
- 파일 첨부: `locator.setInputFiles()`는 "expects first argument to point to an input element with the type 'file'"이며, 복수 파일·디렉터리·메모리 버퍼 업로드를 지원한다. 동적 파일 선택기는 `filechooser` 이벤트로 처리한다 — 같은 문서
- 로그인 세션 재사용: "Tests can load existing authenticated state. This eliminates the need to authenticate in every test." `storageState()`로 쿠키·localStorage·IndexedDB를 저장해 재사용한다. 단 "you need to delete the stored state when it expires", "Playwright does not provide API to persist session storage" — https://github.com/microsoft/playwright/blob/main/docs/src/auth.md (게시본: https://playwright.dev/docs/auth)
- 브라우저 선택: Chrome/Edge는 "new headless mode implementation that is closer to a regular headed mode"이며 `'chromium'` 채널로 "the real Chrome browser"를 쓸 수 있다 — https://github.com/microsoft/playwright/blob/main/docs/src/browsers.md (게시본: https://playwright.dev/docs/browsers)

불가능하거나 제외되는 범위:
- CAPTCHA: Playwright 공식 문서에 CAPTCHA 해결 기능은 없다. 2차 자료(Checkly)는 "it is beyond the point of a test to try and solve a captcha... if captchas could be automatically solved, that would defeat their whole purpose"라고 설명한다 — https://www.checklyhq.com/docs/learn/playwright/challenging-flows/
- 휴대폰 본인인증·간편인증·공동인증서: 제3자 인증창에서 SMS 인증번호나 인증서 비밀번호 입력이 필요하므로 전제상 제외. 사람이 한 번 로그인한 뒤 storageState를 넘겨받아 이후 단계만 자동화한다. 국민신문고는 120분 무활동 시 자동 로그아웃되므로 세션 유효 시간 안에 제출을 끝내야 한다(https://www.epeople.go.kr/nep/gdnc/TermsConditions.npaid, 발췌).
- 봇 탐지: Playwright 문서는 봇 탐지 회피를 다루지 않는다(emulation 문서에는 user agent 재정의만 있음: https://github.com/microsoft/playwright/blob/main/docs/src/emulation.md). 탐지 회피 목적의 조작은 위 약관의 "기만적 이용"에 해당할 수 있어 권장하지 않는다.

## 5. Gmail API 이메일 자동 제출 시 제한

| 항목 | 값 | 근거 |
|---|---|---|
| `users.messages.send` 업로드 최대 크기 | `maxSize: 36700160` 바이트(=35 MiB), `accept: message/*`, simple·resumable 프로토콜(둘 다 multipart 지원). `drafts.create`도 동일 | Gmail API discovery 문서 직접 열람: https://gmail.googleapis.com/$discovery/rest?version=v1 |
| 업로드 방식 | simple(`uploadType=media`, "5 MB or less"), multipart, resumable(`X-Upload-Content-Type: message/rfc822`) | https://developers.google.com/workspace/gmail/api/guides/uploads (발췌) |
| Gmail 첨부 한도(UI 기준) | 개인 계정 25 MB, 초과 시 Google Drive 링크로 자동 전환. Workspace는 관리자가 설정 | https://support.google.com/mail/answer/6584 (발췌) |
| 개인 Gmail 발신 한도 | 하루 500통, 메일 1통당 수신자 500명. 초과 시 1~24시간 발신 차단 | https://support.google.com/mail/answer/22839 (발췌) |
| Workspace 발신 한도 | 하루 2,000통(24시간 롤링). 무료 체험 계정은 더 낮고 체험 중 상향 불가 | https://support.google.com/a/answer/166852 (발췌) |
| API 쿼터 | `messages.send` 100 quota units, 사용자당 15,000 units/분, 프로젝트당 1,200,000 units/분 | https://developers.google.com/workspace/gmail/api/reference/quota (발췌) |
| 오류 처리 | 한도 초과 시 HTTP 429 "User-rate limit exceeded"; 일일 한도 초과는 수 시간 지속 가능; "per-user limits cannot be increased"; 배치는 50건 이하 권장 | https://developers.google.com/workspace/gmail/api/guides/handle-errors (발췌) |

실무 함의: 공모전 제출은 하루 수 통 수준이라 발신 한도는 문제가 되지 않는다. 첨부는 base64 인코딩 후 RFC 822 메시지 전체가 35 MiB 이내여야 하며, 수신 측(korea.kr 등 기관 메일) 수신 한도는 별도이므로 실제 운용 한도는 25 MB 이하로 잡는 편이 안전하다(수신 측 한도는 확인되지 않음).

## 6. 유형별 자동화 판정 표

| 접수 유형 | 판정 | 근거 |
|---|---|---|
| 이메일 | 가능 | 로그인·인증·CAPTCHA 없음. Gmail API `messages.send`로 첨부 포함 발송 가능(35 MiB 상한, 개인 500통/일). 공고 1, 4, 10, 11 |
| 주최 측 자체 웹폼(비회원형) | 조건부 가능 | Playwright `fill`/`setInputFiles`로 처리 가능하나 사이트마다 폼 구조·회원가입·CAPTCHA 유무가 달라 공고별 사전 점검 필요. 공고 13, 16, 18 |
| 국민생각함·국민신문고 | 조건부 가능 | 로그인이 본인인증 계열이라 사람이 로그인한 storageState를 재사용해야 함. 120분 세션 만료. 약관 제12조 "안정적인 운영에 지장" 조항 준수(저빈도·단건 제출). CAPTCHA 여부 확인되지 않음. 공고 2, 5, 6, 12 |
| 국민참여입법센터·청년몽땅정보통 등 기타 공공 플랫폼 | 조건부 가능 | 위와 동일(본인확인 로그인 후 세션 재사용). 공고 9, 17 |
| 구글폼 | 조건부 가능 | 로그인 불필요 설정이면 Playwright로 입력 가능. "응답 1회 제한"·파일 업로드 질문은 Google 로그인 필수 → 세션 재사용 필요. Google 약관의 서비스 방해·기만적 이용 금지 준수. 공고 8 |
| 네이버폼 | 보류(확인되지 않음) | 로그인 요구·약관을 원문으로 확인하지 못함. 공고 12, 14, 15 |
| 위비티 등 공모전 포털 | 해당 없음 | 표본에서 포털 내 접수 사례 없음. 약관 확인되지 않음 |
| 우편·방문 | 불가 | 물리적 제출. 서류 생성(PDF/HWP)까지만 자동화 가능. 공고 3, 11, 16 |

## 7. 결론: 자동 제출 우선 지원 채널 순서

1. 이메일(Gmail API) — 표본에서 가장 흔한 채널(8/18)이고 인증 장벽이 없다. 첨부 25 MB 이하, 발신 로그·수신 확인(자동 회신 여부) 처리를 포함해 먼저 구현한다.
2. 주최 측 자체 웹폼(비회원형) — Playwright 폼 자동화의 기본 골격을 만들되, 공고별 셀렉터 매핑을 사람이 확인하는 반자동 모드로 시작한다.
3. 국민생각함 — 정책 공모전에서 비중이 크다(4/18). 사람이 로그인한 세션(storageState)을 넘겨받아 "생각모음 → 공모전 → 서식 첨부 → 등록"만 자동화한다. 120분 내 완료, 단건 제출, 재시도 최소화로 약관 제12조를 지킨다.
4. 구글폼 — 로그인 불필요 폼만 자동 제출하고, 로그인 필요 폼은 Google 세션 재사용으로 확장한다.
5. 네이버폼 — 도움말·약관 원문 확인 후 판정. 그 전까지는 사람이 제출한다.
6. 우편·방문 — 자동화 제외. 제출 서류 패키징(PDF+HWP, 동의서·서약서 서식)까지만 지원한다.

## 8. 미확인 사항

- 위비티 이용약관 전문과 자동화 금지 조항 유무(사이트 접근 차단).
- 국민신문고·국민생각함 이용약관에 "자동화·매크로"를 직접 언급하는 조항이 있는지(발췌에서는 제12조 일반 조항만 확인).
- 국민생각함 아이디어 등록 화면의 CAPTCHA 유무와 첨부파일 용량 제한.
- 네이버폼 응답 시 네이버 로그인 요구 여부와 이용약관.
- 구글폼 응답 화면에 reCAPTCHA가 표시되는 조건(커뮤니티 문의는 있으나 공식 문서 미확인).
- 2026 서울시 규제혁신 아이디어 공모전(공고 7)의 실제 접수 채널.
- 구리시 공모전(공고 3)의 "온라인" 접수가 구체적으로 어떤 시스템인지.
- Gmail API 쿼터 수치(15,000 units/분 등)와 Workspace 2,000통 한도는 공식 페이지 발췌이며 원문 직접 열람은 하지 못함.
- 기관 메일(korea.kr 등) 수신 측 첨부 용량 한도.
