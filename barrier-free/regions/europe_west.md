# 배리어 프리 비교 — 영국·서유럽·북유럽 (slug: europe_west)

> 작성일 2026-10-13. 클러스터: **영국**(UK), **서유럽**(프랑스·네덜란드·벨기에·룩셈부르크·아일랜드 + EU 공통), **북유럽**(스웨덴·노르웨이·덴마크·핀란드). 독일은 중부유럽 담당이라 제외했습니다.
> 세부 수치는 `europe_west_indicators.csv`(63행), 등급은 `europe_west_ratings.csv`에 있습니다.
> **수집 한계:** 이번 세션에서는 WebFetch로 원문 페이지를 열 수 없었고(DNS 실패), 웹검색 호출 한도도 중간에 소진됐습니다. 그래서 수치는 검색 결과의 1차·2차 출처 요약으로 확인했습니다. 일부 법령의 기본 사항(제정연도 등)은 기존 지식을 바탕으로 적었고, CSV notes에 `확인필요`로 표시했습니다.

---

## 1. EU 공통 프레임
| 항목 | 내용 | 연도 | 출처 |
|---|---|---|---|
| 유럽접근성법(EAA, 2019/882) | 민간 제품·서비스(전자상거래·은행·전자책·발권 등) 접근성 의무 **2025-06-28 적용** | 2025 | [Norton Rose Fulbright](https://connections.nortonrosefulbright.com/post/102mmcn/european-accessibility-act-not-a-nice-to-have-anymore) |
| 웹접근성지침(WAD, 2016/2102) | 공공부문 웹·앱 대상. 회원국은 3년마다 모니터링 보고서를 냄(2022–2024 주기). EU 통합 준수율은 없음 | 2025 | [EC](https://digital-strategy.ec.europa.eu/en/library/web-accessibility-directive-monitoring-reports) |
| EU 장애인카드·주차카드 (2024/2841) | 국내법 전환 기한 2027-06-05, 발급·상호인정 기한 2028-06-05 | 2024 | [EDF](https://www.edf-feph.org/1-year-left-to-adopt-european-disability-card-national-law/) |
| 장애 출현율(GALI, 16세+) | **23.9%**(일부 17.2 + 심각 6.7). 국가별 12.7%(BG)~41.2%(LV) | 2024 | [Eurostat](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Population_with_disability) |
| 장애 고용격차(20–64세) | **24.0%p**(2024). 2022년 21.4%p, 2014년 22.7%p | 2024 | [Eurostat](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20250527-1), [ETUI](https://www.etui.org/publications/narrowing-employment-gap-people-disabilities) |
| Access City Award | 2026 1위 사라고사, 3위 **렌(프랑스)**. 2025 빈 | 2025 | [EC](https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/access-city-award-aca/winners-access-city-award-2026-easy-read_en) |

**정의 주의:** GALI는 자기보고 방식이라 WHO 추정치(약 16%)보다 높게 나오고, 핀란드(34.9%)처럼 응답 성향 때문에 높게 나오는 나라도 있습니다. 국가별 고용격차는 EU-SILC '일부 또는 심각한 활동 제한' 기준입니다. 영국 DWP 수치(LFS·평등법 정의)와는 직접 비교하지 않아야 합니다.

---

## 2. 영국 (클러스터: 영국)
**개요:** 법과 디지털 규제는 유럽에서 가장 정교한 편입니다. 반면 교통 인프라, 고용격차, 복지 축소 측면의 평가는 낮습니다.

- **LAW**: [평등법 2010](https://www.legislation.gov.uk/ukpga/2010/15/contents)은 합리적 조정 의무를 두고, 공공부문 평등의무도 있습니다. UN CRPD 위원회는 2016년 선택의정서에 따른 첫 조사에서 복지개혁(PIP 기준, ILF 폐지, ESA 제재)이 **"중대하거나 체계적인 위반"**에 해당한다고 판단했습니다([CRPD/C/15/4](https://digitallibrary.un.org/record/1311200/files/CRPD_C_15_4-EN.pdf)). 정부는 이를 반박했고, 2024년 후속평가는 "유의미한 진전 없음"이었습니다(옹호단체 보도 기준).
- **TRANS**: 런던 지하철 무단차역은 **94개**로, 2025년 12월 Colindale이 94번째였습니다. 전체 역의 1/3 남짓입니다([TfL](https://tfl-newsroom.prgloo.com/news/five-additional-tube-stations-to-be-assessed-for-step-free-access-feasibility-as-part-of-the-mayor-and-tfls-ongoing-work-to-improve-transport-network-accessibility)). 2030년께 절반이 목표지만 비용 압박이 있습니다([Rail Magazine](https://www.railmagazine.com/news/2025/02/27/cost-pressures-set-to-curtail-plans-for-total-london-underground-step-free-access)).
  - GB 철도역의 무단차 비율은 **61%**인데, 2019년 데이터입니다([ORR](https://www.orr.gov.uk/media/17408/download)).
  - Access for All은 2006년부터 **260여 역**을 개선했습니다(2025). 승객 이용 기준으로는 75% 이상이 무단차역을 지납니다.
  - 블루배지 보유는 잉글랜드에서 2.84백만 장(2024, 인구의 4.9%)에서 **3.07백만 장**(2025)으로 늘었습니다([DfT](https://www.gov.uk/government/statistics/blue-badge-scheme-statistics-april-2024-to-march-2025/blue-badge-scheme-statistics-april-2024-to-march-2025)).
  - 2018년 포용적 교통 전략은 2030년까지 장애인의 동등한 교통 접근을 목표로 합니다.
- **BUILT**: 건축규정 [Part M](https://www.gov.uk/government/publications/access-to-and-use-of-buildings-approved-document-m)은 신축·대규모 개축에만 적용됩니다. 주택은 M4(1)~(3) 등급으로 나뉩니다. 기존 건물에 소급하는 의무는 없고, 평등법의 합리적 조정으로 보완합니다.
- **DIGI**: [PSBAR 2018](https://www.gov.uk/guidance/public-sector-website-and-mobile-application-accessibility-monitoring)에 따라 GDS가 모니터링하며, 2024년 10월부터 WCAG 2.2 AA 기준을 씁니다. 공공기관의 접근성 성명 게시율은 97%이지만, 필수 항목을 모두 갖춘 성명은 65%입니다(2022–24).
- **EMP**: 장애인 고용률은 52.8%, 비장애인은 82.5%로 **격차 29.7%p**입니다(2025 Q2, [DWP](https://www.gov.uk/government/statistics/the-employment-of-disabled-people-2025/the-employment-of-disabled-people-2025)). 2019년(28.8%p)보다 오히려 커졌습니다. 의무고용 쿼터는 없습니다.
- **DATA**: FRS 기준 출현율은 **24%**(2022/23)이고, 2023/24 발표는 "4명 중 1명"이었습니다([FRS](https://www.gov.uk/government/statistics/family-resources-survey-financial-year-2023-to-2024/family-resources-survey-financial-year-2023-to-2024)).

---

## 3. 서유럽
### 프랑스
- **LAW/BUILT**: [Loi 2005-102](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000809647)는 공중이용시설(ERP)과 교통을 2015년까지 접근 가능하게 하도록 정했습니다. 그러나 2015년 시점에 이행한 ERP는 **5만 개 미만**이었습니다. 이에 Ad'AP(접근성 일정계획)로 기한을 연장했습니다.
  - 2018년 기준 100만 개 이상이 Ad'AP 제도에 들어왔고, 접근 가능한 ERP는 35만 개였습니다.
  - 2025년에는 약 200만 ERP 중 **절반이 미착수** 상태였고, 정부는 단속 강화를 지시했습니다([Maire-info](https://www.maire-info.com/mise-en-accessibilite-des-erp-le-temps-de-la-sanction-est-il-venu-article2-29851)).
- **TRANS**: 파리 지하철의 접근 가능 역은 **3%**입니다. 원래는 14호선 9개 역뿐이었습니다([Handicap.fr](https://informations.handicap.fr/a-metro-paris-2024-10792.php)).
  - 연장 구간을 포함해 29개 역이 접근 가능하고, 2031년까지 68개 역을 추가할 계획입니다. 'Métro pour tous'는 약 200억 유로 규모입니다([EU UMO](https://urban-mobility-observatory.transport.ec.europa.eu/news-events/news/paralympic-games-leave-lasting-accessibility-legacy-paris-2025-09-04_en)).
  - **파리 2024 레거시:** 버스망 100% 접근(2개 노선 제외), 휠체어 택시 200~250대에서 **1,000대**로 증가.
- **DIGI**: 공공부문에는 RGAA 4.1을 적용합니다. EAA는 Loi 2023-171로 국내법에 들어왔고 DGCCRF가 감독합니다. 2025년 11월 장애단체가 대형 유통사를 상대로 첫 소송을 냈습니다.
- **EMP**: 20인 이상 사업체에 **OETH 6%** 의무고용률이 있습니다. 직접고용률은 3.6%(2023)에서 **4.0%**(2024)로 올랐고, 가중치를 적용하면 5.1%입니다([DARES](https://www.unea.fr/sites/default/files/dares_dr_oeth_2024.pdf)). EU-SILC 고용격차는 20.8%p(2022)입니다.
- **DATA**: 15세 이상 재가 인구 중 **7.6백만 명**(약 7명 중 1명)이 장애가 있습니다(2021, [DREES](https://drees.solidarites-sante.gouv.fr/publications-communique-de-presse/etudes-et-resultats/en-france-une-personne-sur-sept-de-15-ans-ou)).

### 네덜란드
- 고용격차는 **25.2%p**(2022)로 EU 평균보다 큽니다([EDF](https://www.edf-feph.org/publications/european-semester-outcomes-spring-package-2024-european-disability-forum/)).
- 일자리 협약(Banenafspraak)은 2025년까지 추가 일자리 91,812개를 만들어 목표 12.5만 개에 못 미쳤습니다. 특히 공공부문 실적이 저조합니다([상원 서한 2026-09](https://www.eerstekamer.nl/behandeling/20260909/brief_regering_resultaten/document3/f=/vn0wlh7ajqpi.pdf)).
- CRPD는 2016년에 늦게 비준했고, 선택의정서 비준 여부는 확인이 필요합니다.
- 기본활동에 어려움이 있다고 답한 비율이 50%를 넘습니다(2022, Eurostat).

### 벨기에
- 고용격차는 **35.3%p**(2022, EU 3위, [Euronews](https://www.euronews.com/2024/04/02/where-is-it-hardest-to-live-in-europe-as-a-person-with-a-disability)) 또는 33.6%p(2023, [EC](https://ec.europa.eu/social/BlobServlet?docId=27971&langId=en))입니다. EU 최하위권입니다.
- 교통·건축·디지털 정량자료는 이번에 수집하지 못했습니다.

### 룩셈부르크
- 고용격차는 **8.5%p**로 EU 최저입니다(2022). 실업률 격차도 0.4%p로 EU 최저입니다(2024).
- 룩셈부르크시는 Access City Award를 받았습니다(2022, 확인필요).

### 아일랜드
- CRPD는 2018년에야 비준했고, 선택의정서는 **2024-11-30에 발효**됐습니다([PILA](https://pila.ie/resources/bulletin/2025/01/15/optional-protocol-to-the-convention-on-persons-with-disabilities-came-into-effect-in-ireland-on-30-november-2024)).
- 고용격차는 **37%p**로 EU 최대입니다(2022).
- 공공부문 법정 고용목표는 3%에서 2025년 **6%**로 올랐습니다. 2022년에는 기관의 48.4%가 6%를 넘었습니다([NDA](https://nda.ie/monitoring/monitoring/employment-of-persons-with-disabilities-in-the-public-sector)).
- WAD 모니터링(2024)은 간이검토 232건, 심층검토 23건, 모바일앱 8건입니다.

---

## 4. 북유럽 (클러스터: 북유럽)
- **스웨덴**
  - 2015년부터 '불충분한 접근성'을 차별로 규정합니다(확인필요).
  - [디지털 공공서비스 접근성법 2018:1937](https://www.w3.org/WAI/policies/sweden/)이 2019년 시행됐고 DIGG가 감독합니다.
  - Access City Award 1위를 세 번 받았습니다: 예테보리 2014, 옌셰핑 2021, 셸레프테오 2023(연도 확인필요).
  - 다만 고용격차는 **25.7%p**(2022)로 커졌습니다.
- **노르웨이**
  - 국가 차원의 [유니버설 디자인 정책](https://www.regjeringen.no/en/topics/equality-and-social-inclusion/likestilling-og-inkludering/funksjonsnedsetjingar/universal-design/id670423/)이 있고, 2025년까지 UD 사회를 이룬다는 비전을 세웠습니다.
  - 2013년 ICT 규정으로 **민간까지** 웹 접근성 의무를 집니다.
  - 공공웹 시범 모니터링 점수는 **91/100**입니다(2024, [Uutilsynet](https://www.uutilsynet.no/media/2393/download)).
- **덴마크**: 고용격차는 **9.9%p**로 EU 최저 수준입니다. 일반 장애차별금지법은 늦게 도입됐습니다(2018, 확인필요).
- **핀란드**: GALI 출현율은 **34.9%**로 EU 2위입니다(2024). 고용격차는 19.0%p(2022)입니다.

---

## 5. 등급표
| 클러스터 | 국가 | LAW | TRANS | BUILT | DIGI | EMP | TOUR | 종합 |
|---|---|---|---|---|---|---|---|---|
| 영국 | 영국 | 상 | 중 | 중 | 상 | 하 | 중 | **중** |
| 서유럽 | 프랑스 | 중 | 하 | 중 | 중 | 중 | 중 | **중** |
| 서유럽 | 네덜란드 | 중 | 확인필요 | 확인필요 | 중 | 하 | 확인필요 | **중** |
| 서유럽 | 벨기에 | 중 | 확인필요 | 확인필요 | 확인필요 | 하 | 확인필요 | **중** |
| 서유럽 | 룩셈부르크 | 중 | 확인필요 | 중 | 확인필요 | 상 | 확인필요 | **중** |
| 서유럽 | 아일랜드 | 중 | 확인필요 | 확인필요 | 중 | 하 | 확인필요 | **하** |
| 북유럽 | 스웨덴 | 상 | 확인필요 | 상 | 상 | 중 | 확인필요 | **상** |
| 북유럽 | 노르웨이 | 상 | 확인필요 | 상 | 상 | 확인필요 | 확인필요 | **상** |
| 북유럽 | 덴마크 | 중 | 확인필요 | 확인필요 | 확인필요 | 상 | 확인필요 | **중** |
| 북유럽 | 핀란드 | 상 | 확인필요 | 확인필요 | 상 | 중 | 확인필요 | **중** |

등급 근거는 `europe_west_ratings.csv`의 rationale 열에 있습니다. 영국과 프랑스의 TOUR 등급은 정량자료 없이 정성적으로 판단했습니다.

## 6. 우수 사례 / 문제 사례
- **우수**
  - 노르웨이: 민간까지 포괄하는 ICT 유니버설 디자인 의무.
  - 스웨덴: 접근성 결여를 차별로 규정하고, Access City Award를 여러 번 수상.
  - 룩셈부르크·덴마크: 고용격차 10%p 미만.
  - 영국: GDS의 체계적인 공공웹 모니터링.
  - 파리 2024: 버스와 택시의 빠른 개선.
- **문제**
  - 파리 지하철 접근 3%.
  - 프랑스 Ad'AP 이행 지연(ERP 절반 미착수).
  - 아일랜드·벨기에 고용격차 35%p 이상.
  - 영국 CRPD '중대·체계적 위반' 판정, 고용격차 약 30%p.
  - 네덜란드 일자리 협약 목표 미달.

## 7. 데이터 공백 (후속 수집 필요)
1. Eurostat의 국가별 GALI(hlth_silc_12)와 2024 고용격차(tepsr_sp200)는 이번 세션에서 DB에 직접 접근하지 못해 일부 국가만 확보했습니다. 국가별 값은 대부분 2022년 기준입니다.
2. 고령화율(65세 이상 %)은 출처 URL을 확인하지 못해 모든 국가에서 빠졌습니다.
3. 아래 교통 자료는 미수집입니다.
   - 네덜란드: NS/ProRail
   - 벨기에: SNCB, 브뤼셀 STIB
   - 아일랜드: Iarnród Éireann, DART
   - 북유럽 각국 지하철·철도 접근률
   - 룩셈부르크: 2020년 대중교통 무료화와 접근성의 관계
4. 아래 법령은 원문 재확인이 필요합니다(CSV notes에 `확인필요`로 표시).
   - 룩셈부르크 2022 접근성법
   - 덴마크 2018 차별금지법
   - 핀란드 디지털서비스제공법(306/2019)
   - 네덜란드·노르웨이 선택의정서 비준 여부
5. TOUR 차원은 전 국가에서 정량지표를 확보하지 못했습니다(프랑스 Tourisme & Handicap 라벨, 영국 VisitEngland 등 확인 필요).
