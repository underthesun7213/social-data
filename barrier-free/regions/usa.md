# 미국(USA) — 배리어 프리 비교 리포트 (클러스터: 북미)

> 작성일: 2026-10-13 · 지표 63행: `usa_indicators.csv` · 등급: `usa_ratings.csv`
> **수집 제약:** 이번 세션에서는 웹페치가 막혀(egress 403/DNS) 정부 원문 페이지를 직접 열지 못했고, 웹검색 할당량도 도중에 소진됐다. 따라서 수치는 검색 결과에 나온 1차·2차 출처에서 가져왔다. 원문을 다시 확인하지 못한 항목은 CSV notes에 "지식 기반·원문 재확인 못함", "2차 출처", "확인필요"로 표시했다.

## 1. 개요

미국은 **민권(civil rights)형 접근성 법제의 원형**이다. ADA(1990)와 ADAAA(2008), 2010 ADA 설계기준, 재활법 Section 504·508, 항공기접근법(ACAA, 1986)이 촘촘하게 짜여 있다. 다만 행정 규제보다 **사적 소송**이 주된 집행 수단이어서 지역별 편차가 크다. **CRPD는 2009년 서명했지만 비준하지 않았다.** 2012년 12월 상원 표결이 61대 38로 정족수 66표에 못 미쳐 부결됐고, 2014년에는 외교위원회만 통과한 뒤 본회의에 오르지 못했다. 선택의정서에도 가입하지 않았다.

## 2. 차원별 핵심 수치 (전국)

### LAW 법·제도
- ADA는 1990년 제정됐다(Title I 고용, II 공공, III 민간시설, IV 통신). ADAAA(2008)는 '장애'의 정의를 넓게 해석하도록 했다 — [ADA.gov](https://www.ada.gov/law-and-regs/ada/), [EEOC](https://www.eeoc.gov/statutes/ada-amendments-act-2008)
- 2025년 ADA Title III 연방소송은 **8,667건**이었다(2024년 8,800건, 2021년 정점 11,452건). 이 중 웹 접근성 소송은 **3,117건**으로 36%를 차지하며 전년보다 27% 늘었다 — [Seyfarth](https://www.adatitleiii.com/2026/03/federal-court-website-accessibility-lawsuit-filings-bounce-back-in-2025/)
- 연방 ADA로는 사인이 손해배상을 받을 수 없다. 반면 **캘리포니아 Unruh법**은 ADA 위반을 Unruh 위반으로 간주하고(§51(f)), 위반 1건당 **최소 4,000달러**의 법정손해배상을 인정한다(§52(a), Munson v. Del Taco 2009) — [JMBM](https://www.jmbm.com/docs/munson_v_del_taco.pdf)

### TRANS 교통
- ADA는 레거시 철도에 **'핵심역(key station)'**만 접근 의무를 지웠다(1993년까지, 연장 시 최대 2020년). 통근철도는 1994년까지, 연장 시 최대 2010년이다 — [49 CFR 37.51](https://www.law.cornell.edu/cfr/text/49/37.51). FY2004 기준 핵심역 547곳 중 437곳(82%)만 기한 안에 준수했다 — [FHWA](https://www.fhwa.dot.gov/reports/htffy04/mda_06_09.htm)
- FTA의 FY2026 전역 접근성 프로그램(ASAP)은 6.86억 달러를 공고해 8개 사업에 2.33억 달러를 선정했다 — [Railway Supply](https://www.railway.supply/all-stations-accessibility-program-awards-233m-after-686m-offer/)
- 항공: 2024년 휠체어·스쿠터 오취급률은 **1.26%**였다(899,385대 운송 중 약 11,000대). DOT는 아메리칸항공에 과징금 5,000만 달러를 부과했다(2024). 2024년 DOT 휠체어 규칙은 항공사 소송과 집행 연기로 묶여 있다 — [WheelchairTravel](https://wheelchairtravel.org/ranking-best-worst-airlines-wheelchair-users-2024/)

### BUILT 건축
- 2010 ADA Standards는 2012년 3월 15일부터 의무화됐다. 신축과 개축은 완전 준수해야 하지만, 기존 민간시설은 '용이하게 달성 가능한(readily achievable)' 범위에서만 장벽을 제거하면 된다 — [ADA.gov](https://www.ada.gov/law-and-regs/design-standards/2010-stds/)

### DIGI 디지털
- DOJ Title II 웹 규칙(2024)은 주·지방정부의 웹과 앱에 **WCAG 2.1 AA**를 적용한다. 2026년 4월 20일 임시최종규칙으로 준수기한이 1년 미뤄졌다. 인구 5만 이상 정부는 **2027-04-26**(원래 2026-04-24), 인구 5만 미만 정부와 특별구는 **2028-04-26**(원래 2027-04-26)까지다 — [Seyfarth](https://www.adatitleiii.com/2026/04/doj-extends-ada-title-ii-website-accessibility-deadlines-for-governmental-entities-but-litigation-and-compliance-risks-remain/), [CTAS](https://www.ctas.tennessee.edu/news/doj-extends-wcag-21-aa-compliance-deadlines-local-governments)
- Section 508 Refresh(2017년 공포, 2018년 시행)는 연방기관에 WCAG 2.0 AA를 적용한다 — [Access Board](https://www.access-board.gov/ict/)
- 민간(Title III) 웹에는 기술기준이 없다. 그 공백을 소송이 메우고 있다. 2025년 디지털 접근성 소송은 5,000건을 넘었다(UsableNet). WebAIM Million 2026에서는 홈페이지의 95.9%에서 WCAG 오류가 검출됐다(글로벌 표본).

### EMP 고용·사회참여
- BLS 2025 기준 장애인 고용률(16세 이상)은 **22.8%**, 비장애인은 65.2%로 **격차는 42.4%p**다. 16–64세 장애인 고용률은 38.1%, 장애인 실업률은 8.3%(비장애인 4.1%)다 — [BLS](https://www.bls.gov/news.release/archives/disabl_03032026.htm)
- ACS 기준 근로연령(21–64세) 장애인 고용률은 46.8%, 비장애인은 81.5%다(2023) — [Cornell](https://disabilitystatistics.org/report/2023/US)
- 의무고용 쿼터는 없다. 연방계약자에게 Section 503의 7% 활용 '목표'만 있다.
- 2025년 Medicaid HCBS 대기자는 **606,895명**이다. 41개 주에 대기명단이 있다 — [KFF](https://www.kff.org/medicaid/state-indicator/number-of-people-waiting-for-hcbs-by-target-population-and-whether-states-screen-for-eligibility/)

### TOUR 관광
- 국가 차원의 무장애 관광 전략은 없다. 대신 ADA Title III가 숙박·관광시설에 적용된다.
- 2018–19년 장애인 여행자 2,700만 명이 8,100만 회 여행해 **587억 달러**를 썼다. 이 중 항공여행 지출은 110억 달러다 — [Open Doors Organization](https://disabilityinsider.com/2020/11/02/travel/new-data-shows-economic-impact-of-disability-travel-reaches-58-7-billion/)

### DATA 기초통계
- CDC BRFSS(2022) 기준 성인 기능장애 출현율은 **28.7%**(약 7,000만 명)다. 65세 이상은 43.9%다 — [CDC](https://www.cdc.gov/disability-and-health/articles-documents/disability-and-health-data-now.html)
- ACS(2023) 기준으로는 약 13.5%다. 2차 출처라 확인이 필요하다. 문항 정의가 달라 BRFSS 수치와 큰 차이가 난다.
- WHO 추정치(16%)와 비교하면 BRFSS는 넓은 자기보고형 기능제한 정의를 쓰고, ACS는 좁은 6문항 정의를 쓴다.
- 고령화율(65세 이상)은 약 18%(2024)로 추정한다. 확인이 필요하다.

## 3. 미국 내부 상/중/하 비교 (15개 주·도시/교통망)

1차 탐색으로 지표를 모은 뒤, **교통 접근역 비율**, **장애인 고용률**(Cornell 2023, Everway 재가공), **AARP LTSS 스코어카드**(2023), **KFF HCBS 대기자**(2025), **주법의 강도**, **소송 빈도**를 종합해 묶었다.

| 등급 | 주·도시 | 핵심 근거 |
|---|---|---|
| **상** | 워싱턴 D.C. (WMATA) | Metrorail 98역 100% 엘리베이터(개통 때부터), AARP LTSS Tier 1 |
| 상 | 샌프란시스코 베이 지역 (BART) | 전 역 엘리베이터(소송으로 이룬 첫 사례), 캘리포니아 Unruh법 적용 |
| 상 | 미네소타 | AARP LTSS **1위**, 고용률 55.5%(5위), MHRA는 1인 사업장부터 적용, 미니애폴리스 WalletHub 최상위권 |
| 상 | 콜로라도 | 고용률 57.8%(3위), AARP LTSS Tier 1 |
| 상 | 매사추세츠 / 보스턴 (MBTA) | AARP LTSS 4위, MBTA 역 83% 접근(2026), 그린라인 2031년 68/70역 목표 |
| **중** | 캘리포니아 | 법은 최강(Unruh 최소 4,000달러/건, 장애인법)이지만 고용률은 45.5%로 평균 수준, Title III 소송 3,252건 최다 |
| 중 | 시카고 (CTA) | 146역 중 110역(75%), ASAP로 2038년 전역 접근 목표 |
| 중 | 로스앤젤레스 (LA Metro) | 신설 철도망으로 전 역 경사로·엘리베이터(3자 출처, 추정). 버스·보도 자료는 부족 |
| 중 | 사우스다코타 | 고용률 **61.5%로 1위**. 다만 교통·LTSS·법 지표 자료가 부족해 중으로 보수적으로 매김 |
| 중 | 필라델피아 (SEPTA) | 철도·지하철역 약 60% 접근, 브로드스트리트선은 25역 중 12역(2022) |
| **하** | 뉴욕 (NYC MTA / NY State) | 지하철 472역 중 **160역(약 34%)**만 완전 접근, 95% 목표 시점은 **2055년**, 주 고용률 41.4% |
| 하 | 텍사스 | HCBS 대기 **181,697명**(전국 최다), IDD 웨이버 대기 15–18년 |
| 하 | 플로리다 | HCBS 대기 77,123명(사전심사 없음), Title III 연방소송 1,823건(웹 소송 2배 증가) |
| 하 | 미시시피 | 고용률 40.6%, AARP LTSS 하위 5, Case for Inclusion 51위(2019), 잭슨·걸프포트 WalletHub 하위권 |
| 하 | 웨스트버지니아 | 고용률 **36.4%로 최하위**, AARP LTSS **51위** |

**해석.** 교통 접근성은 **개통 연도**가 사실상 결정한다. 1970년대 이후 개통한 WMATA·BART·LA Metro는 100%다. 반면 1904년 개통한 NYC, 시카고, 보스턴, 필라델피아는 ADA 핵심역 조항 때문에 30–80%에 머문다. 지역사회 통합(HCBS)과 고용은 남부(TX·FL·MS·WV)가 취약하고 중서부와 서부 산악 지대(MN·CO·SD)가 강하다. 법 강도와 성과가 일치하지 않는 대표 사례는 캘리포니아다.

## 4. 우수 사례 / 문제 사례
- **우수:** BART와 WMATA의 전 역 엘리베이터, 미네소타의 LTSS·지역사회 통합, 캘리포니아 Unruh법의 강한 사적 구제, CTA ASAP의 시한이 명시된 전역 접근 계획.
- **문제:** NYC 지하철의 장기 미접근(2055년 목표), Title II 웹 규칙 기한 1년 연기, 민간 웹 기술기준 부재와 반복 소송(반복 피소 1,427건), 텍사스 HCBS 대기 10년 이상, 항공 휠체어 파손과 DOT 규칙 집행 연기, CRPD 미비준.

## 5. 등급표 (전국)

| LAW | TRANS | BUILT | DIGI | EMP | TOUR | 종합 |
|---|---|---|---|---|---|---|
| 상 | 중 | 상 | 중 | 하 | 중 | **중** |

근거: 법·건축 기준은 세계 최고 수준이고 집행력도 있다. 그러나 CRPD를 비준하지 않았고, 고용 격차가 42%p에 달하며, 교통·디지털의 지역별·부문별 편차가 크다.

## 6. 데이터 공백
- 2026년 MTA 공식 역 목록을 확인하지 못했다(160역은 주지사 보도자료 기준).
- LA Metro 역별 공식 목록이 없다.
- WalletHub 2025 원문 순위가 확인되지 않았다(미니애폴리스 1위설과 세인트루이스 1위설이 상충).
- 주별 고용률은 Everway의 2차 가공 수치라 Cornell 원표로 검증해야 한다.
- 주별 웹 접근성 실태조사, 저상버스·휠체어 택시 비율, 보도·점자블록 자료는 수집하지 못했다(검색 할당량 소진).
- Census 65세 이상 비율과 ACS 출현율은 원표 확인이 필요하다.
- 주의: '접근역'의 정의가 시스템마다 다르다. MBTA는 전 역 기준, SEPTA는 통행 기준과 역 기준이 섞여 있고, NYC는 '완전 접근' 기준이다.
