# 공모전 제출 문서 포맷과 Linux 에이전트의 생성·양식 채우기 전략

조사일: 2026-09-02. 조사 환경: Ubuntu 24.04 샌드박스(Python 3.11.15, LibreOffice 24.2.7.2, Node 22).
정부·지자체·공모전 포털(sotong.go.kr, epeople.go.kr, moleg.go.kr, seoul.go.kr, gov.kr, wevity, linkareer, contestkorea 등)은 샌드박스 프록시에서 차단되어 **원문 페이지를 직접 열지 못했다**. 공고 서식 정보는 해당 페이지에 대한 검색 엔진 스니펫(WebSearch 결과)에 근거하며, 표에 그 사실을 명시했다. 도구 정보는 GitHub·PyPI·npm 원문과 샌드박스 실측에 근거한다.

## 요약

1. 공공기관 정책·시정 제안 공모전은 압도적으로 **HWP/HWPX 양식(표 형태 신청서)**을 요구하고, PDF는 "서명 스캔본 병행" 또는 소수 기관의 단독 제출 포맷으로 등장한다. 조사한 16건 중 DOCX·PPTX를 요구한 공고는 0건이다.
2. Linux에서 **HWPX는 python-hwpx(6.3.0, 2026-08-22, Apache-2.0)로 생성·편집·양식 채우기가 가능**하며, 샌드박스에서 표 양식 생성 → 재오픈 → `fill_by_path`로 3개 셀 채우기 → 검증 통과를 실측했다.
3. **구형 바이너리 HWP(5.x)는 Linux에서 쓰기 경로가 사실상 없다.** python-hwpx는 HWP를 거부하고, pyhwp는 읽기 전용에 2020년 이후 릴리스가 없으며 Python 3.11에서 설치가 실패했다. Java hwplib·Rust rhwp가 대안이지만 Python 생태계 밖이다.
4. **LibreOffice 내장 HWP 필터는 HWP 3.0(한글97) 읽기 전용**이고 HWPX·HWP 5.x·쓰기는 지원하지 않는다. H2Orestart 확장을 설치해야 HWP5/HWPX를 읽을 수 있고, 그래도 저장은 ODT/PDF뿐이다.
5. pyhwpx·한컴 COM 자동화는 Windows + 한/글 설치가 전제이므로 Linux 에이전트에서는 배제해야 하며, 최종 HWP 저장·시각 검수·서명은 사람 개입이 불가피하다.

## 1. 공고 샘플 포맷 표

근거 유형: **S** = 검색 스니펫(원문 미열람), **F** = 원문 열람. 이번 조사는 전부 S다.

| # | 공고 | 주최 | 요구/제공 서식 포맷 | 제출 경로 | 근거 |
|---|------|------|--------------------|-----------|------|
| 1 | 2026년 국민 아이디어 공모제 (공고 제2026-28호) | 법제처 | 서식 `.hwp`, 공고문 `.hwp`/`.pdf` | 국민참여입법센터 게시판 또는 우편 | S: [소통24](https://sotong.go.kr/front/epilogue/epilogueBbsViewPage.do?bbs_id=76029fd63ef440349317cc606ed80398&searchkey=A&searchtxt=&miv_pageNo=1), [법제처](https://www.moleg.go.kr/board.es?mid=a10504000000&bid=0010&list_no=147492&act=view&nPage=1) |
| 2 | 2025 국민생각함 정책 아이디어 공모전 | 국민권익위원회 | 참가신청서·아이디어 제출 서식 `.hwpx` | 국민생각함 온라인 첨부 | S: [국민생각함](https://www.epeople.go.kr/api/thk/pbsb/PbsbsrpnPrpslDetail.npaid?ideaRegNo=1AE-2504-0000457) |
| 3 | 2026 국민생각함 정책 아이디어 공모전 | 국민권익위원회 | "(2026) 참가 신청서 및 아이디어 제출 서식(청년성인일반)`.hwp`" 필수 첨부 | 국민생각함 온라인 첨부 | S: [국민생각함](https://www.epeople.go.kr/api/thk/pbsb/PbsbsrpnPrpslDetail.npaid?ideaRegNo=1AE-2603-0000819) |
| 4 | 2026 부산 인구활력 정책 아이디어 공모전 | 부산광역시 | 신청서·제안서 양식(확장자 확인되지 않음) | 이메일(gustp@korea.kr) | S: [소통24](https://sotong.go.kr/front/epilogue/epilogueNewViewPage.do?bbs_id=71bb3d2c54884ae8b94c33ae2609e2dd) |
| 5 | 2025년 제주시 정책 아이디어 공모전 | 제주시 | 제안서식 `HWPX` | 홈페이지·이메일·우편·방문 | S: [콘테스트코리아](https://www.contestkorea.com/sub/view.php?Txt_gbn=1&Txt_bcode=031410001&str_no=202503040106) |
| 6 | 2025년 화성형 기본사회 정책 공모전 | 화성시 | 서식 `.hwpx`; 서명본 PDF 제출 시 한글 파일 병행 필수 | 우편·이메일 | S: [콘테스트코리아](https://www.contestkorea.com/sub/view.php?int_gbn=1&Txt_bcode=031410001&str_no=202509100047) |
| 7 | 2026 화성형 기본사회 정책 공모전 | 화성특례시 | 참가신청서·제안서·개인정보동의서; 서명 후 PDF 제출 시 한글 파일 동봉 필수 | 우편·이메일(hohobro@korea.kr) | S: [씽크유](https://thinkyou.co.kr/contest/62716/) |
| 8 | 「우리가 바꾸는 경기도」 정책 제안 공모전 | 경기도 | 공모신청서 `HWPX`(한글), 청렴서약서는 서명 스캔 `PDF` | 온라인 | S: [경기도의 소리](https://vog.gg.go.kr/web/main/bbs/photo/647) |
| 9 | 혁신 아이디어 공모전 (연도 확인되지 않음) | 광복회 | "공고문 및 신청서 양식`.hwp`" | 확인되지 않음 | S: [광복회 첨부](https://www.i815.or.kr/flexer.php?code=notice&ntt_no=990218&atch_no=2) |
| 10 | 2026 청년연구 아이디어 공모전 | 청년재단 | 신청서(4쪽 이내)+개인정보동의서를 **PDF**로, 파일명 `성명_제목명.pdf` | 이메일(research@kyf.or.kr) | S: [청년재단](https://kyf.or.kr/user/boardDetail.do?bbsId=BBSMSTR_000000000367&nttNo=9803) |
| 11 | 2026 청년 정책 아이디어 공모전 '내가 대통령이라면' | 국민경제자문회의 | 양식 다운로드 후 첨부(확장자 확인되지 않음) | 네이버폼, 실패 시 이메일 | S: [2030DB](https://www.2030db.go.kr/user/ntt/BBS_0000000000000001/NTT_0000000000000684/selectNttDetail.do) |
| 12 | 2026 인천형 주거복지정책 시민 아이디어 공모전 | 인천시 광역주거복지센터 | 신청서 다운로드 후 이메일 첨부(스니펫상 `.hwp`, 약한 근거) | 이메일(ihwc_admin@ih.co.kr) | S: [한양대 공지](https://policy.hanyang.ac.kr/front/communication/notice/notice-view?id=2338&page=1), [로컬세계](https://localsegye.co.kr/news/view/1065593889932743) |
| 13 | 2026년 제1회 정책제안 공모 | 대구광역시 | 확인되지 않음 | 토크대구·국민신문고·우편·방문·팩스 | S: [헤럴드경제](https://biz.heraldcorp.com/article/10678858) |
| 14 | 2026 생활안전 R&D 아이디어 공모전 | 행정안전부 | 신청서(확장자 확인되지 않음) | 국민생각함 또는 이메일 | S: [행안부](https://mois.go.kr/frt/bbs/type013/commonSelectBoardArticle.do?bbsId=BBSMSTR_000000000006&nttId=125200) |
| 15 | 2026 기본사회위원회 정책 아이디어 공모전 | 기본사회위원회 | 확인되지 않음 | 이메일·우편·구글폼 | S: [위비티](https://www.wevity.com/index_university.php?c=find&s=_university&gbn=viewok&gp=5&ix=110214) |
| 16 | 2026년 시민참여예산 제안사업 공모 | 서울특별시 | 확인되지 않음 | 온라인 플랫폼 | S: [서울시](https://news.seoul.go.kr/gov/archives/565322?listPage=1) |

집계(16건): HWP 또는 HWPX 명시 **9건**(#1,2,3,5,6,7,8,9,12), 그중 HWPX 명시 4건(#2,5,6,8). PDF 등장 **4건**(#6,7,8 서명본 병행, #10 단독). DOCX·PPTX 요구 **0건** — "docx"/"word"/"pptx" 키워드를 붙인 검색에서는 위 표의 HWP/HWPX 공고(#5·#6·#16)만 다시 나왔고 DOCX·PPTX를 요구한 정책 공모전 공고는 나오지 않았다(검색 스니펫 기준, 부재 증명은 아님). 온라인 폼 직접 입력 또는 폼+파일 첨부 **6건**(#1,3,11,13,14,16). 서식 확장자를 스니펫으로 확정하지 못한 공고는 "확인되지 않음"으로 남겼다.

## 2. 도구별 상태 표

| 도구 | 최근 릴리스 | 플랫폼 | 지원 범위 | 알려진 한계 | 출처 |
|------|-------------|--------|-----------|-------------|------|
| **python-hwpx** | 6.3.0, 2026-08-22, Apache-2.0, Py≥3.10 | 순수 Python(Win/mac/Linux/CI) | HWPX 읽기·편집·생성. 표(병합·중첩), 이미지, 머리말/꼬리말, 각주, 변경추적. `doc.tables.fill_by_path` / `find_cell_by_label`로 라벨 기준 셀 채우기, 바이트 보존 패치 저장, `validate()` | HWP 5.x 바이너리 미지원(`BadZipFile`), 암호화 HWPX 미지원, 자체 렌더/미리보기 없음, 저수준 `add_shape`/`add_control`은 한/글이 못 여는 파일 생성 가능 | [PyPI](https://pypi.org/project/python-hwpx/), [GitHub](https://github.com/airmang/python-hwpx), [support-matrix](https://github.com/airmang/python-hwpx/blob/main/docs/support-matrix.md), [known-traps](https://github.com/airmang/python-hwpx/blob/main/docs/known-traps.md), [migration-6.0](https://github.com/airmang/python-hwpx/blob/main/docs/migration-6.0.md) |
| python-hwpx-automation | 7.0.3, 2026-08-22, Apache-2.0 | 순수 Python | python-hwpx 위의 작업 지향 계층: 양식 채우기+검증 워크플로, 표 연산, HTML/PNG 미리보기, 선택적 MCP 서버 | 세부 한계 확인되지 않음 | [PyPI](https://pypi.org/project/python-hwpx-automation/) |
| pyhwpxlib | 0.18.3, 2026-05-10 | 순수 Python | HWPX 생성·편집, 공문 서식, Markdown→HWPX, PNG 내보내기 | **PolyForm Noncommercial**(상업 이용 별도 라이선스), 복잡한 셀 병합은 수동 검토, 미리보기 없음 | [PyPI](https://pypi.org/project/pyhwpxlib/) |
| **pyhwp (hwp5)** | 0.1b15, 2020-05-30, AGPLv3, Py 2.7/3.5–3.8; 마지막 커밋 2023-04-09 | Python | HWP 5.0 **읽기 전용**: 스트림 추출, txt/odt/html 변환(실험적) | 쓰기 없음, HWPX 없음. **샌드박스 실측: Python 3.11에서 `pip install pyhwp` 빌드 실패(setuptools `install_layout` AttributeError, `--no-build-isolation`도 동일)**. PyPI의 `hwp5` 0.1.0은 달력 분석용 무관 패키지 | [PyPI](https://pypi.org/project/pyhwp/), [GitHub](https://github.com/mete0r/pyhwp), [commits](https://github.com/mete0r/pyhwp/commits/master) |
| pyhwpx | 1.7.2, 2026-03-19 | **Windows 전용** | 한/글 HwpAutomation(COM)을 pywin32로 래핑 | 한/글 설치 필수, Linux 불가 | [PyPI](https://pypi.org/project/pyhwpx/), [GitHub](https://github.com/martiniifun/pyhwpx) |
| hwplib (Java) | Maven 1.1.9(2025-04-30), 마지막 커밋 2026-07-13, Apache-2.0 | JVM(Linux 가능) | HWP 5.x **읽기+쓰기** | 암호화 HWP 미지원, 이미지/PDF 변환·페이지 수 산출 없음 | [GitHub](https://github.com/neolord0/hwplib) |
| hwpxlib / hwp2hwpx (Java) | hwpxlib 1.0.8(2025-11), 마지막 커밋 2026-08-31, Apache-2.0 | JVM | HWPX 읽기·쓰기; hwp2hwpx는 HWP→HWPX 변환 | Java 7+; 암호화는 확장 라이브러리 | [hwpxlib](https://github.com/neolord0/hwpxlib), [hwp2hwpx](https://github.com/neolord0/hwp2hwpx) |
| rhwp / @rhwp/core (Rust+WASM) | v0.8.6, 2026-09-02, MIT | Linux x86_64·macOS·Windows CLI 바이너리, npm | HWP 5.0·HWPX·HML 읽기, SVG/PDF/PNG 렌더, HWPX/HML 저장, HWP→HWPX 변환, MCP 서버 | "Foundation phase", 그림·임베디드 리소스는 손실 저장 차단, 수식 제약 | [GitHub](https://github.com/edwardkim/rhwp), [README_EN](https://github.com/edwardkim/rhwp/blob/main/README_EN.md), [releases](https://github.com/edwardkim/rhwp/releases/latest), [npm](https://www.npmjs.com/package/@rhwp/core) |
| openhwp (Rust) | 날짜 확인되지 않음, MIT | Rust | HWP 5.0 읽기, HWPX 읽기·쓰기, 상호 변환 | 성숙도 확인되지 않음 | [GitHub](https://github.com/openhwp/openhwp) |
| hwpx-skill (에이전트 스킬) | v1.10.0, MIT | Python 3 + python-hwpx/lxml; HWP 변환은 Windows COM 또는 @rhwp/core WASM 폴백 | 템플릿 플레이스홀더 치환, 표 셀 채우기, 공문 서식 | 표 음영·복잡한 도형·페이지 나눔 차이, OLE·수식 보장 없음, 한/글 시각 검수 필요 | [GitHub](https://github.com/jkf87/hwpx-skill) |
| **LibreOffice 내장 hwpfilter** | 24.2.7.2(샌드박스) | Linux | 필터 `writer_MIZI_Hwp_97`(UI명 "Hangul WP 97"), Flags `IMPORT ALIEN 3RDPARTYFILTER EXOTIC` → **가져오기 전용**. `hwpfile.cxx`는 V2.0/2.1/3.0 서명을 식별하되 `HWP_V30`이 아니면 `HWP_UNSUPPORTED_VERSION`으로 거부 | **HWP 5.x·HWPX 미지원, HWP 내보내기 없음**. 샌드박스 레지스트리에서 hwp 관련 필터는 `writer_MIZI_Hwp_97` 하나뿐 | [filters/writer_MIZI_Hwp_97.xcu](https://github.com/LibreOffice/core/blob/master/filter/source/config/fragments/filters/writer_MIZI_Hwp_97.xcu), [types xcu](https://github.com/LibreOffice/core/blob/master/filter/source/config/fragments/types/writer_MIZI_Hwp_97.xcu), [hwpfile.cxx](https://github.com/LibreOffice/core/blob/master/hwpfilter/source/hwpfile.cxx) |
| H2Orestart (LibreOffice 확장) | v0.7.13, 2024-06-27, GPLv3; Ubuntu 24.04 apt `libreoffice-h2orestart` 0.6.1-1 | Linux(apt/AUR/확장 저장소) | HWP 5.x·HWPX **읽기** → ODT/PDF 변환 | **HWP/HWPX 저장 불가**(ODT만). 샌드박스에는 미설치 | [GitHub](https://github.com/ebandal/H2Orestart), [releases](https://github.com/ebandal/H2Orestart/releases) |
| 한컴 한글 SDK | 확인되지 않음 | 확인되지 않음 | HWP/HWPX 생성·편집·변환 라이브러리(상용) | Linux 지원·라이선스 조건 원문 미열람(sdk.hancom.com 프록시 차단) | [sdk.hancom.com](https://sdk.hancom.com/), [한글 SDK](https://www.hancom.com/product/sdk/hwpSdk) |
| python-docx / docxtpl / python-pptx / reportlab | 1.2.0 / 0.20.2 / 1.0.2 / 5.0.1 (`pip index versions`, 2026-09-02) | 순수 Python | DOCX·PPTX·PDF 생성 | — | [python-docx](https://pypi.org/project/python-docx/), [docxtpl](https://pypi.org/project/docxtpl/), [python-pptx](https://pypi.org/project/python-pptx/), [reportlab](https://pypi.org/project/reportlab/) |
| docx / pptxgenjs / pdf-lib (npm) | 9.7.1 / 4.0.1 / 1.17.1 (`npm view`, 2026-09-02) | Node | DOCX·PPTX·PDF 생성 | — | [docx](https://www.npmjs.com/package/docx), [pptxgenjs](https://www.npmjs.com/package/pptxgenjs), [pdf-lib](https://www.npmjs.com/package/pdf-lib) |

샌드박스 실측 메모: python-hwpx 6.3.0을 스크래치 디렉터리에 설치해 3×2 표(제안명/제안자/제안 내용) 양식을 만들고, 파일을 다시 열어 `fill_by_path({"제안명 > right": ..., ...})`를 실행하니 `applied_count=3, failed_count=0`, `validate()` 이슈 0건, 재오픈 후 텍스트 추출로 채워진 값(줄바꿈 포함)을 확인했다. 6.x에서는 `fill_by_path`·`export_text`가 `doc.tables.fill_by_path`·`doc.text.plain`으로 이동했고 구 API는 7.0에서 제거 예정이라는 DeprecationWarning이 출력된다. 반면 `soffice --headless --convert-to`는 이 샌드박스에서 `.txt` 입력에도 "source file could not be loaded"로 실패해(샌드박스 해제 후에도 동일) LibreOffice 변환은 실측하지 못했고, 위 판단은 필터 레지스트리와 소스 코드에 근거한다.

## 3. 포맷별 권장 생성 경로 (Linux 에이전트)

| 포맷 | 1순위 경로 | 보조 경로 | 비고 |
|------|-----------|-----------|------|
| **HWPX** | python-hwpx: 주어진 양식을 열어 `doc.tables.find_cell_by_label` → `doc.tables.fill_by_path`로 채우고 바이트 보존 저장, `validate()` 통과 확인 | python-hwpx-automation(검증 워크플로·PNG 미리보기), 새 문서는 `add_table`/`add_paragraph`로 생성 | 시각 검수는 rhwp CLI의 SVG/PDF 렌더 또는 H2Orestart+LibreOffice PDF 변환으로 대체 가능(둘 다 한/글 렌더와 동일하다는 보장은 없음) |
| **HWP(5.x, 바이너리)** | 공고가 HWP만 받으면: 제출자가 한/글로 HWPX를 열어 "다른 이름으로 저장 → .hwp"(사람 개입) | rhwp(HWPX→HWP 변환 기능 명시, 단 그림·임베디드 리소스 손실 저장 차단) 또는 Java hwplib/hwp2hwpx 조합 | Python 순수 경로 없음. 주어진 HWP 양식은 rhwp/hwp2hwpx로 HWPX로 바꾼 뒤 python-hwpx로 채우는 2단계가 현실적. LibreOffice·pyhwp는 쓰기 불가 |
| **PDF** | 내용 문서를 DOCX/HWPX로 만든 뒤 변환: DOCX는 `soffice --convert-to pdf`, HWPX는 H2Orestart 설치 후 동일 명령 또는 rhwp `pdf` 내보내기 | reportlab(직접 조판), pdf-lib(병합·양식) | 서명이 필요한 서약서·동의서는 결국 사람이 출력·서명·스캔 |
| **DOCX** | python-docx 또는 docxtpl(Jinja 템플릿), Node는 docx | LibreOffice로 ODT/PDF 변환 | 공고 요구 빈도가 낮아 보조 산출물 용도 |
| **PPTX** | python-pptx 또는 pptxgenjs | — | 정책 공모전 1차 서류에서는 요구 사례 없음(발표 심사 단계에서 별도 안내 가능성) |

## 4. 주어진 HWP/HWPX 양식 채우기의 현실성 (조사 항목 5)

- **HWPX 양식**: 현실적으로 가능하다. python-hwpx는 기존 문서를 열어 라벨 셀 오른쪽/아래 셀을 찾아 값만 바꾸고 나머지 바이트를 보존하는 방식(497개 테스트로 바이트 보존 확인)을 지원하며, 병합·중첩 표도 생성·검증 대상이다([support-matrix](https://github.com/airmang/python-hwpx/blob/main/docs/support-matrix.md)). 샌드박스 실측도 성공했다.
- **HWP(5.x) 양식**: 직접은 불가능하다(python-hwpx가 `BadZipFile`로 거부). rhwp 또는 hwp2hwpx로 HWPX로 변환한 뒤 채우는 것이 유일한 자동 경로이며, 변환 손실(그림·OLE·수식·표 음영) 위험이 있다([rhwp README_EN](https://github.com/edwardkim/rhwp/blob/main/README_EN.md), [hwpx-skill 한계](https://github.com/jkf87/hwpx-skill)).
- **주의점**: 텍스트 치환 시 `<hp:linesegarray>` 캐시를 지워야 글자 겹침이 없고, 표 삭제는 역순으로, `render_checked=False`는 구조 검증만 통과한 상태라는 뜻이다([known-traps](https://github.com/airmang/python-hwpx/blob/main/docs/known-traps.md)). 암호화(배포용) 양식은 열 수 없다.

## 5. 윈도우 전용 도구를 배제하는 이유 (조사 항목 4)

- pyhwpx는 "Windows 환경에서 작동하며 한/글이 설치되어 있어야" 하고, 파일을 해석하는 것이 아니라 설치된 한/글을 pywin32(COM)로 구동하는 구조다([PyPI](https://pypi.org/project/pyhwpx/), [GitHub](https://github.com/martiniifun/pyhwpx)). COM 자체가 Windows 전용 IPC이며, 헤드리스 Linux 컨테이너에는 한/글 바이너리도 라이선스도 없다.
- hwpx-skill조차 HWP 변환을 "Windows에서는 한컴 COM, 그 외 OS는 @rhwp/core WASM 폴백"으로 갈라 두었다([GitHub](https://github.com/jkf87/hwpx-skill)). 즉 커뮤니티도 Linux에서는 COM 경로를 포기하고 있다.
- 한컴 공식 SDK의 Linux 지원 여부는 확인되지 않음(원문 차단). 확인되더라도 상용 라이선스 계약이 전제다.

## 6. 사람 개입이 불가피한 지점

1. **HWP(.hwp) 최종 저장**: 공고가 `.hwp`만 허용하면 한/글에서 다른 이름으로 저장하는 단계(또는 rhwp 변환 결과의 육안 확인)가 필요하다.
2. **시각 검수**: python-hwpx는 렌더 백엔드가 없어 "구조상 유효"까지만 보장한다. 한/글(또는 최소한 rhwp/H2Orestart 렌더)로 표 깨짐·글꼴·페이지 넘침을 확인해야 한다.
3. **서명 문서**: #6·#7·#8처럼 청렴서약서·개인정보동의서는 서명 후 스캔 PDF를 요구한다.
4. **온라인 폼 입력**: #1·#3·#11·#13·#14·#16은 국민생각함·네이버폼·토크대구 등 로그인 기반 폼이라 본인 인증과 업로드는 제출자가 한다.
5. **암호화·배포용 양식**: python-hwpx가 열지 못하므로 제출자가 한/글에서 일반 저장으로 풀어 줘야 한다.

## 7. 미확인 사항

- 공고 원문 16건 모두 프록시 차단으로 직접 열람하지 못했다. 서식 확장자는 검색 스니펫 기준이며 #4·#11·#13·#14·#15·#16은 확장자를 확정하지 못했다.
- LibreOffice 24.2의 HWPX·HWP 5.x 거부 동작을 샌드박스에서 실행으로 재현하지 못했다(`soffice --convert-to`가 `.txt`에도 실패). 결론은 설치된 필터 레지스트리(`writer_MIZI_Hwp_97`만 존재)와 업스트림 소스(`hwpfile.cxx`, xcu)에 근거한다.
- H2Orestart의 "HWP v5 또는 HWPX 읽기" 문구는 Debian ITP 메일 검색 결과에서 나왔고, 원문(mail-archive.com)은 차단되어 미확인이다. 저자 README에서 확인한 범위는 "HWPX 읽기, ODT로만 저장"이다.
- pyhwp GitHub 최신 커밋(2023-04-09)은 저장소 페이지 요약에서 얻은 값이며, 2024년 이후 커밋 유무는 직접 확인하지 못했다.
- 한컴 한글 SDK의 Linux 지원·가격·라이선스, 그리고 rhwp v0.8.6 릴리스 자산 목록(Linux x86_64 바이너리 포함 여부)은 페이지 로딩 실패로 확인되지 않음.
- python-hwpx가 생성한 HWPX를 실제 한/글 2022·2024가 여는지 이 환경에서는 검증할 수 없다(README는 "한/글 GUI 오라클로 검증"이라 주장).
