# 공모전 공고 수집 소스 조사

조사일: 2026-09-02. 질문: 한국 공모전 공고를 프로그램으로 수집할 수 있는 소스는 무엇이고, 각 소스는 어떤 방식(RSS·공개 API·HTML 스크래핑)으로 접근 가능한가.

> 조사 환경 제약: 이 세션의 네트워크 정책이 조사 대상 도메인 전부(wevity.com, thinkcontest.com, linkareer.com, campuspick.com, all-con.co.kr, korea.kr, epeople.go.kr, seoul.go.kr, gg.go.kr, data.go.kr, data.seoul.go.kr, data.gg.go.kr)에 대한 직접 접속을 차단해 robots.txt·약관 원문을 직접 읽지 못했다. 아래 내용은 각 1차 페이지가 검색엔진에 색인된 본문 발췌(snippet)에 근거하며, 발췌로 확인되지 않은 항목은 "확인되지 않음"으로 표기했다. 구현 전 반드시 각 URL을 직접 열어 재확인해야 한다.

## 1. 요약

1. **정식 기계 접근(RSS·API)이 확인된 소스는 공공 쪽뿐이다.** 정책브리핑(korea.kr)은 RSS 8종을 공식 제공하고, 국민신문고는 data.go.kr에 "공개제안조회서비스" API가 있으며, 서울시 고시공고는 열린데이터광장 Open API(OA-2482)로 열려 있다.
2. **민간 5개 사이트(위비티·씽굿·링커리어·캠퍼스픽·올콘)는 RSS·공개 API가 확인되지 않았고, HTML 스크래핑만 가능하다.** 링커리어 약관은 크롤링·스크래핑을 명시적으로 금지하고, 씽굿·올콘 약관은 영리 목적 복제·배포를 금지한다. 위비티·캠퍼스픽 약관 조항은 확인되지 않음.
3. **공공기관 정책·시정 제안 공모전을 가장 잘 모으는 1차 소스는 국민신문고 "공모제안" 목록(epeople.go.kr/nep/prpl/selectPbsbsrpnPrpslOngoingList.npaid)이다.** 중앙·지자체·교육청이 특정 과제를 지정해 공모기간 동안 아이디어를 모집하는 제안이 한곳에 모인다. 다만 이 목록 자체의 API는 확인되지 않았고 HTML 접근이다.
4. 보조 소스로 서울시는 mediahub.seoul.go.kr/gongmo(공모 전용 게시판, HTML)와 OA-2482 API, 경기도는 gg.go.kr 고시공고 게시판(bsIdx=469, HTML)과 gnews.gg.go.kr RSS를 조합하면 지자체 공모의 상당 부분을 잡을 수 있다.
5. data.go.kr의 공모전 데이터셋은 대부분 **수상작·과거 개최 목록**(KIPRISPlus 공모전 아이디어, KIDP 개최공모전 목록)이라 "진행 중 공고" 수집용으로는 한국콘텐츠진흥원 지원사업공고 API 정도만 쓸모가 있다.

## 2. 소스별 표

| 소스 | RSS | 공개 API | HTML 구조 | robots.txt | 약관의 자동수집 조항 | 갱신 주기 | 공고 1건 필드(마감·주최·분야·자격·상금·접수) |
|---|---|---|---|---|---|---|---|
| 위비티 wevity.com | 확인되지 않음(검색상 없음) | 없음(확인되지 않음) | `index.php?c=find&s=1&gbn=viewok&ix={id}` 상세, `gbn=list&gp={page}` 목록 | 확인되지 않음 | 약관 존재는 확인, 조항 내용 확인되지 않음 | 확인되지 않음 | 분야·응모대상·주최/주관·접수기간·총 상금(1등 상금)·홈페이지 링크 |
| 씽굿 thinkcontest.com | 확인되지 않음 | 없음(확인되지 않음) | `thinkgood/user/contest/view.do?querystr=…` (난독화 파라미터) | 확인되지 않음 | 영리 목적 복제·전송·배포 금지 | 확인되지 않음 | 접수기간·주최·시상내역 (검색 발췌 수준) |
| 링커리어 linkareer.com | 확인되지 않음 | 비공개(내부 API 문서 없음) | `/list/contest` 목록, `/activity/{id}` 상세 | 확인되지 않음 | **크롤링·스크래핑 명시 금지** | 확인되지 않음(실시간 표방) | 상금·수상혜택·분야(디자인/영상/슬로건/아이디어/창업) |
| 캠퍼스픽 campuspick.com | 확인되지 않음 | 없음(확인되지 않음) | `/contest` 목록, `/contest/view?id={id}` 상세 | 확인되지 않음 | 확인되지 않음(약관 2025-04-15 개정) | 확인되지 않음 | 활동명·주최·마감일·조회수·썸네일 (제3자 크롤러 사례 기준) |
| 올콘 all-con.co.kr | 확인되지 않음 | 없음(확인되지 않음) | `/list/contest/{1~5}?page=&sst=cl_is_end…` 목록 | 확인되지 않음 | 영리 목적 복제·전송·배포 금지 | 확인되지 않음 | 확인되지 않음 |
| 정책브리핑 korea.kr | **있음** `korea.kr/rss/{policy,pressrelease,media,…}.xml` | 없음 | `/news/policyNewsView.do?newsId=`, `/multi/visualNewsView.do?newsId=` | 확인되지 않음 | 공공누리(출처표시) 자유이용 | 수시(보도자료 단위) | 본문 텍스트에 포함(구조화 안 됨): 기간·자격·상금 |
| 국민생각함 idea.epeople.go.kr | 확인되지 않음 | 없음(확인되지 않음) | `/nep/thk/subj/SubjThinkList.npaid?pageIndex=` | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 |
| 국민신문고 국민제안 epeople.go.kr | 확인되지 않음 | **공개제안조회서비스**(data.go.kr 15059423) — 단, 공모제안 목록 포함 여부 확인되지 않음 | `/nep/prpl/selectPbsbsrpnPrpslOngoingList.npaid` 공모제안, `/nep/prpsl/opnPrpl/opnpblPrpslList.npaid` 공개제안 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 공모기간·개최기관·특정과제 |
| 서울시 | 확인되지 않음 | **OA-2482 고시공고 Open API** | `seoul.go.kr/news/news_notice.do` 고시공고, `mediahub.seoul.go.kr/gongmo/{id}` 공모 | 확인되지 않음 | 열린데이터광장 인증키·1회 1,000건 | 확인되지 않음 | (OA-2482) 제목·작성자·담당기관·담당부서·내용·첨부 / (mediahub) 공모명·응모자격·접수기간·담당부서 |
| 경기도 | **있음** `gnews.gg.go.kr/rss/gnews_rss_main.do` | 고시공고 전용 API 확인되지 않음(openapi.gg.go.kr 일반) | `gg.go.kr/bbs/board.do?bsIdx=469&menuId=1547`, 상세 `boardView.do?bIdx=` | 확인되지 않음 | 경기데이터드림: 호출횟수 제한 없음, Key 필수 | 확인되지 않음 | 확인되지 않음 |
| 부산시(3번째 샘플) | 확인되지 않음 | 고시공고 API 확인되지 않음 | `busan.go.kr/nbgosi` 고시공고 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 |
| 공공데이터포털 data.go.kr | 해당 없음 | 15134251 콘진원 지원사업공고, 15056752 KIPRIS 공모전 아이디어(수상작), 15085852 해외인턴 공모전, 15121448/15133752 KIDP(파일) | 해당 없음 | 확인되지 않음 | 개발계정 일 1,000건, 운영계정 일 10만 건, 상업적 이용 가능 여부 API별 상이 | API별 상이(대부분 확인되지 않음) | 콘진원: 제목·사업번호·카테고리·등록일·링크·접수시작/종료·내용 |

## 3. 소스별 상세

### 3.1 위비티 (wevity.com)
- 접근: 목록·상세 모두 GET 파라미터 기반 PHP 페이지. 상세 예 `https://www.wevity.com/index.php?c=find&s=1&gub=4&cidx=8&gbn=viewok&gp=1&ix=106965`, 목록 예 `https://wevity.com/index.php?c=find&cidx=1&gp=29&gub=1&mode=end&s=1` (cidx=분야, gp=페이지, mode=end/ing). 대학생용 별도 경로 `index_university.php` 존재. 출처: https://www.wevity.com/index.php?c=find&s=1&gub=4&cidx=8&gbn=viewok&gp=1&ix=106965 , https://wevity.com/index.php?c=find&cidx=1&gp=29&gub=1&mode=end&s=1
- RSS: 검색으로 RSS 엔드포인트가 나오지 않음. 사이트는 이메일 메일링 서비스를 제공. 출처: https://www.wevity.com/
- 필드: 분야, 응모대상(일반인/대학생/제한없음 등), 주최/주관, 접수기간, 총 상금·1등 상금, 홈페이지 링크. 출처: https://www.wevity.com/index_university.php?c=find&s=_university&gbn=viewok&gp=1&ix=106321
- 약관: 하단에 이용약관·개인정보처리방침·책임한계와 법적고지 링크 존재. 자동수집 조항 내용 확인되지 않음. 출처: https://www.wevity.com/
- robots.txt: 확인되지 않음. 갱신 주기: 확인되지 않음.

### 3.2 씽굿 (thinkcontest.com)
- 접근: 상세 URL이 `thinkgood/user/contest/view.do?querystr=<난독화 문자열>` 형태라 id 열거가 어렵고 목록 페이지 링크를 따라가야 함. 출처: https://thinkcontest.com/thinkgood/user/contest/view.do?querystr=_I2r2ZjZXpMPqyflcNFyALubX-e7L1z7zNkhbiksJC0
- 약관(https://www.thinkcontest.com/thinkgood/user/info/userTerm.do): 서비스로 얻은 정보를 회사 사전 승낙 없이 영리 목적으로 복제·송신·출판·배포·방송·기타 방법으로 이용하거나 제3자에게 이용하게 할 수 없음. 회사 허락 없는 영리활동 시 가입 거부 가능. 출처: https://www.thinkcontest.com/thinkgood/user/info/userTerm.do
- RSS·API·robots.txt·갱신 주기: 확인되지 않음. 필드는 접수기간·주최·시상내역이 상세에 노출되는 것까지만 확인. 출처: https://thinkyou.co.kr/contest/41989

### 3.3 링커리어 (linkareer.com)
- 접근: `https://linkareer.com/list/contest` 목록(상금·수상혜택·분야 필터), `https://linkareer.com/activity/{숫자id}` 상세. SPA 형태로 추정되나 렌더링 방식은 확인되지 않음. 출처: https://linkareer.com/list/contest , https://linkareer.com/activity/231947
- 약관(https://linkareer.com/terms/2025-12-23): 정상적인 서비스 흐름을 벗어난 기술적 조작·**크롤링·스크래핑** 등 비정상적 방법으로 자료를 수집하는 행위를 금지. 출처: https://linkareer.com/terms/2025-12-23
- 내부 API(`api.linkareer.com` 등): 공개 문서 없음. 출처: 검색 결과 없음(https://linkareer.com/)
- RSS·robots.txt·갱신 주기: 확인되지 않음.

### 3.4 캠퍼스픽 (campuspick.com)
- 접근: `https://www.campuspick.com/contest` 목록, `https://www.campuspick.com/contest/view?id=12532` 상세. 제3자(해시스크래퍼)가 Python 크롤러 튜토리얼을 공개했고, 수집 컬럼은 키워드·활동명·주최·마감일·조회수·썸네일 URL. 출처: https://www.campuspick.com/contest/view?id=12532 , https://blog.hashscraper.com/campuspick-crawler-python-series-1/
- 약관: 공모전·대외활동 관리 서비스가 비누커리어(주)로 이관되며 2025-04-15 개정. 자동수집 조항 본문 확인되지 않음. 출처: https://www.campuspick.com/page/notice , https://www.campuspick.com/page/managerprivacy
- RSS·API·robots.txt·갱신 주기: 확인되지 않음.

### 3.5 올콘 (all-con.co.kr, 한국경제신문)
- 접근: `https://www.all-con.co.kr/list/contest/1`(대학생·일반인 공모전), `/2` 대외활동, `/3` 청소년, `/5` 행사. 목록 정렬 파라미터 `sst=cl_is_end = 0 DESC, cl_end_date`(마감일순), `cl_reg_date`(등록일순), `cl_view`(조회순) 등이 URL에 노출. 출처: https://www.all-con.co.kr/list/contest/1 , https://www.all-con.co.kr/list/contest/3?sst=cl_is_end0DESC2Ccl_end_date&sc=2&st=4&sstt=f&page=27
- 약관(https://www.all-con.co.kr/content/provision, 시행 2012-04-10): 올콘이 제공하는 서비스를 사전 승낙 없이 영리 목적으로 복제·송신·출판·배포·방송·기타 방법으로 이용하거나 제3자에게 이용하게 할 수 없음. 출처: https://www.all-con.co.kr/content/provision
- RSS·API·robots.txt·갱신 주기·상세 필드: 확인되지 않음.

### 3.6 정책브리핑 (korea.kr)
- RSS 공식 제공(https://www.korea.kr/etc/rss.do). 확인된 피드: 정책뉴스 `https://www.korea.kr/rss/policy.xml`, 보도자료 `https://www.korea.kr/rss/pressrelease.xml`, 멀티미디어 `https://www.korea.kr/rss/media.xml`, 국민이 말하는 정책 `rss/reporter.xml`, 정책기고 `rss/column.xml`, 이슈인사이트 `rss/insight.xml`, 사실은 이렇습니다 `rss/fact.xml`. http→https 전환됨. 출처: https://www.korea.kr/etc/rss.do
- 공모전 노출 위치: 카드뉴스(`/multi/visualNewsView.do?newsId=…`)와 정책뉴스에 "공모" 제목으로 게시되며, 기간·자격·총상금이 본문 텍스트에 들어 있음(구조화 필드 아님). 예: 애국가 배경영상 국민참여 공모전(2026-04-15~28, 전 국민, 총상금 표기). 출처: https://www.korea.kr/multi/visualNewsView.do?newsId=148962226&call_from=rsslink , https://www.korea.kr/multi/visualNewsView.do?newsId=148902091
- 저작권(https://www.korea.kr/guide/copyRight.do): 텍스트는 공공누리 출처표시 조건 자유이용, 사진·이미지·영상은 별도 권리자 허락 필요, 기사 이용 시 출처 표기. 출처: https://www.korea.kr/guide/copyRight.do
- robots.txt: 확인되지 않음. 갱신: 보도자료 단위 수시(RSS 항목 타임스탬프 기준).

### 3.7 국민생각함 (idea.epeople.go.kr)
- 접근: 생각참여>생각모음 `https://idea.epeople.go.kr/nep/thk/subj/SubjThinkList.npaid?pageIndex=N`, 국민패널 안건 `/nep/thk/ptcnr/ptcnrThinkList.npaid`, 생각실현 `/nep/thk/change/ThinkBoxChangeTopView.npaid`. 개별 안건 상세는 `epeople.go.kr/api/thk/qstnr/selectQstnrThinkBoxDetail.npaid?ideaRegNo=1AE-…` 형식. 출처: https://idea.epeople.go.kr/nep/thk/subj/SubjThinkList.npaid?pageIndex=29 , https://www.epeople.go.kr/api/thk/qstnr/selectQstnrThinkBoxDetail.npaid?ideaRegNo=1AE-2205-0002123
- 성격: 국민권익위원회가 국민 아이디어를 정책·행정개선에 반영하려 운영하는 참여 플랫폼(설문·토론 중심). 공모전 목록 전용 메뉴는 확인되지 않음. 출처: https://www.mois.go.kr/frt/sub/a03/ideaepeople/screen.do
- RSS·API·robots.txt·갱신 주기·필드: 확인되지 않음. data.go.kr에서 "국민생각함" 데이터셋은 검색되지 않음.

### 3.8 국민신문고 국민제안 (epeople.go.kr)
- **공모제안** 목록: `https://www.epeople.go.kr/nep/prpl/selectPbsbsrpnPrpslOngoingList.npaid` (진행중, pageIndex 페이징). 정의: 소관 행정기관 또는 다수 기관이 특정과제를 지정해 공모기간 동안 아이디어를 모집하는 제안. 심사기간은 공모 종료일부터 1개월 이내. 출처: https://www.epeople.go.kr/nep/prpl/selectPbsbsrpnPrpslOngoingList.npaid
- 공개제안 목록: `https://www.epeople.go.kr/nep/prpsl/opnPrpl/opnpblPrpslList.npaid?pageIndex=N`. 출처: https://www.epeople.go.kr/nep/prpsl/opnPrpl/opnpblPrpslList.npaid?pageIndex=58
- 공개 API: **국민권익위원회_공개제안조회서비스**(https://www.data.go.kr/data/15059423/openapi.do) — 국민신문고에 제출된 공개제안 목록·상세 조회. 공모제안(공모 공고) 자체를 반환하는지는 확인되지 않음. 요청변수·출력항목·갱신주기 확인되지 않음(Swagger는 data.go.kr 페이지에서 제공). 출처: https://www.data.go.kr/data/15059423/openapi.do
- `https://api.epeople.go.kr/`: 국민신문고 API를 공공데이터포털을 통해 제공한다는 안내 페이지. 출처: https://api.epeople.go.kr/
- 필드(공모제안): 공모기간·개최기관·특정과제. 상금·자격은 확인되지 않음. robots.txt·RSS·갱신 주기: 확인되지 않음.

### 3.9 지자체 샘플
**서울시**
- 고시공고 게시판 `https://www.seoul.go.kr/news/news_notice.do` (12,130건/1,213페이지, bbsNo=277, article_num 상세). 출처: https://www.seoul.go.kr/news/news_notice.do
- Open API **OA-2482 서울시 고시공고 정보**(SHEET/OPEN API, 일반행정): 게시물 제목·작성자·담당기관·담당부서·내용·트랙백 주소·첨부파일 주소. 인증키 필요, 1회 최대 1,000건. 활용사례 등록 시 제한 해제. 출처: https://data.seoul.go.kr/dataList/OA-2482/S/1/datasetView.do , https://data.seoul.go.kr/together/guide/useGuide.do
- 공모 전용 게시판 `https://mediahub.seoul.go.kr/gongmo/{id}`: 공모명·응모자격·접수기간(시각 포함)·담당부서 표기. 예: 짧은 시 공모(자격 제한 없음, 2022-09-15 00:00~10-05 23:59). 출처: https://mediahub.seoul.go.kr/gongmo/2000294 , https://mediahub.seoul.go.kr/gongmo/2000683
- 자치구 단위 고시공고 API도 별도 존재(예: 노원구 OA-12727). 출처: https://data.seoul.go.kr/dataList/OA-12727/S/1/datasetView.do

**경기도**
- 고시공고 게시판 `https://www.gg.go.kr/bbs/board.do?bsIdx=469&menuId=1547`, 상세 `boardView.do?bIdx={id}&bsIdx=469`. 공모 성격 공고(평가위원 모집, 공개모집 등) 혼재. 출처: https://www.gg.go.kr/bbs/board.do?bsIdx=469&menuId=1547 , https://www.gg.go.kr/bbs/boardView.do?bIdx=213349044&bsIdx=469&menuId=1547
- RSS: 경기도 뉴스포털 `https://gnews.gg.go.kr/rss/gnews_rss_main.do`. 고시공고 전용 피드인지 확인되지 않음. 출처: https://gnews.gg.go.kr/rss/gnews_rss_main.do
- Open API: 경기데이터드림(https://openapi.gg.go.kr) — Key 필수(없으면 sample 5건), Type=xml/json, 호출횟수 제한 없음. 고시공고·공모 데이터셋은 검색되지 않음. 출처: https://data.gg.go.kr/portal/openapi/usagePage.do

**부산시**
- 고시공고 `https://www.busan.go.kr/nbgosi`, 시보 고시공고 `busan.go.kr/news/gosiboard`. 고시공고 Open API 확인되지 않음. 출처: https://www.busan.go.kr/nbgosi

### 3.10 공공데이터포털 (data.go.kr)
- 이용 조건: 파일데이터는 로그인 없이 다운로드, Open API는 회원가입 후 활용신청. 개발계정 일평균 1,000건, 운영계정 일 최대 10만 건(활용사례 등록·승인 필요). 상업적 이용 불가 API를 상업 활용하거나 트래픽 초과 시 이용 제한. 출처: https://www.data.go.kr/ugs/selectPublicDataUseGuideView.do , https://www.data.go.kr/bbs/faq/selectFaqList.do
- 공모전 관련 데이터셋(확인분):
  - **한국콘텐츠진흥원_지원사업공고**(15134251, API): 제목·사업번호·카테고리·조회수·등록일·게시물 링크·접수시작일·접수종료일·내용. 진행 중 공고 수집에 직접 유효. 갱신주기 확인되지 않음. 출처: https://www.data.go.kr/data/15134251/openapi.do
  - **지식재산처_KIPRISPlus_공모전 아이디어**(15056752, REST/XML): 13개 중앙부처·지자체 공모전 **수상작·공개작** 정보(아이디어명·공모전명·공모년도·수상정보·주최기관·주관기관·공개일자 등). 월 1,000회 무료. 과거 공모전 파악용. 출처: https://www.data.go.kr/data/15056752/openapi.do
  - **한국산업인력공단_해외인턴 공모전 정보**(15085852, API): 공모전 연도·명칭·접수 시작/종료일. 출처: https://www.data.go.kr/data/15085852/openapi.do
  - **한국디자인진흥원_개최공모전 목록**(15121448, 파일, 2019~2025): 공모전 구분·개최년도·공모전명·공고 여부. 3단계 이상 파일은 포털이 자동 API(JSON/XML) 변환 제공. 출처: https://www.data.go.kr/data/15121448/fileData.do
  - **한국디자인진흥원_공모전 공지사항**(15133752, CSV): 구분·제목·내용·파일명·게시일. 출처: https://www.data.go.kr/data/15133752/fileData.do
  - 서울특별시_고시공고 정보(15072128, 파일, 2020 기준). 출처: https://www.data.go.kr/data/15072128/fileData.do
- 전국 단위 "공모전 공고" 통합 API는 검색되지 않음. 지자체 고시공고 API는 서울 외 확인되지 않음.

## 4. 결론: 공공기관 정책·시정 제안 공모전을 가장 잘 모아주는 소스

1. **1순위 — 국민신문고 공모제안 목록**(https://www.epeople.go.kr/nep/prpl/selectPbsbsrpnPrpslOngoingList.npaid). 중앙·지자체·교육청의 "특정과제 지정 + 공모기간" 제안 공모가 제도적으로 한곳에 접수되므로 커버리지가 가장 넓다. 접근은 HTML(pageIndex 페이징). 공개제안조회서비스 API(15059423)가 이를 대체하는지 검증 필요.
2. **2순위 — 정책브리핑 RSS**(policy.xml, pressrelease.xml, media.xml). 부처 공모전이 보도자료·카드뉴스로 거의 빠짐없이 올라오고 공공누리 자유이용이라 법적 부담이 가장 적다. 단, 필드가 본문 텍스트라 LLM 추출이 필요하다.
3. **3순위 — 지자체 공모 전용 게시판**: 서울 mediahub.seoul.go.kr/gongmo(공모명·자격·기간·부서가 구조화됨) + OA-2482 API, 경기 gg.go.kr bsIdx=469 + gnews RSS.
4. 민간 포털(위비티 등)은 커버리지는 넓지만 링커리어는 약관상 크롤링 금지, 씽굿·올콘은 영리 목적 복제 금지라 **공공 소스를 주(主), 민간 포털은 누락 점검용 보조**로 두는 편이 안전하다.

## 5. 미확인 사항

- 12개 도메인 전부 robots.txt 원문 미확인(네트워크 차단). Disallow 경로·Crawl-delay 존재 여부 전부 "확인되지 않음".
- 위비티·캠퍼스픽·국민신문고·국민생각함·지자체 3곳의 이용약관 자동수집 조항 원문.
- 공개제안조회서비스(15059423)의 요청변수·출력항목·갱신주기, 그리고 "공모제안" 공고가 응답에 포함되는지.
- 민간 5개 사이트의 갱신 주기(등록 빈도) 및 RSS 부재의 확정(검색상 미노출일 뿐 존재 부정은 아님).
- 링커리어·캠퍼스픽의 클라이언트 렌더링 방식(SSR/CSR) 및 내부 JSON 엔드포인트.
- 경기도 gnews RSS에 고시공고 카테고리가 포함되는지, 경기데이터드림에 고시공고 데이터셋이 있는지.
- 부산·인천 등 서울 외 광역지자체의 고시공고 Open API 존재 여부.
- data.go.kr 각 API의 갱신주기·상업적 이용 가능 표시(페이지별 메타 필드).
