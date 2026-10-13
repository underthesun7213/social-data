# 배리어 프리(Barrier-Free) 국가 비교 데이터 수집 — 공통 스펙

## 평가 차원 (dimension 코드)
| 코드 | 차원 | 대표 지표 예시 |
|---|---|---|
| LAW | 법·제도 | CRPD 비준/선택의정서, 장애차별금지법, 접근성 법(ADA·EAA 등), 집행·제재 수단 |
| TRANS | 교통 | 지하철·철도역 무단차(step-free)/엘리베이터 설치율, 저상버스 비율, 휠체어 택시, 항공 |
| BUILT | 건축·도시환경 | 건축 접근성 기준, 유니버설 디자인 의무, 기존 건물 소급, 보도·점자블록, 인증제도 |
| DIGI | 디지털 접근성 | 웹 접근성 법(WCAG 수준), 공공/민간 적용 범위, 실태 조사 결과(WebAIM 등) |
| EMP | 고용·사회참여 | 장애인 고용률·고용격차, 의무고용률(쿼터), 교육 통합 |
| TOUR | 관광·여가 | 무장애 관광 정책, 숙박·관광지 접근성, 국제 평가 |
| DATA | 기초 통계 | 공식 장애 출현율(%), 고령화율(65+ %) — WHO 추정 ~16%와 비교 |

## 등급
- 상(High) / 중(Mid) / 하(Low) — 차원별 + 종합(overall). 근거(rationale) 반드시 기재.
- 자료가 없거나 불확실하면 `확인필요`로 표기하고 추정치는 notes에 '추정' 명시.

## 산출물 형식 (지역별)
1. `regions/<slug>.md` — 서술형 리포트 (한국어): 국가별 개요, 차원별 핵심 수치(출처 링크), 우수/문제 사례, 등급표, 데이터 공백.
2. `regions/<slug>_indicators.csv` — 컬럼(UTF-8, 헤더 포함, 쉼표 포함 값은 큰따옴표):
   `cluster,country,sub_unit,dimension,indicator,value,unit,year,source_name,source_url,notes`
3. `regions/<slug>_ratings.csv` — 컬럼:
   `cluster,country,LAW,TRANS,BUILT,DIGI,EMP,TOUR,overall,rationale`
   (값: 상/중/하/확인필요)

## 원칙
- 1차 출처(정부 통계, 법령, 교통공사, OECD/EU/WHO/UN 보고서) 우선. 모든 수치에 연도와 URL.
- 국가 간 정의 차이(장애 정의, '무단차역' 정의)는 notes에 명시.
