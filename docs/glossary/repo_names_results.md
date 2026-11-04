# 저장소 이름 검증 결과 (최종 2026-11-04)

> **확정: 저장소 `tabular-compare-engine`** — https://github.com/goodand/tabular-compare-engine.git (사용자가 생성)
> **GUI 유형(decision-labeling-studio `kind`): `grid_compare_triage`** — g8 회차 사용자 채택(임시, 바뀔 수 있음). 이전 `table_compare`는 철회
> 막힌 질문: 없음.

## 확정된 정의
- **저장소**: 여러 소스의 표를 읽기 전용 사본으로 받아 같음·다름·한쪽에만 있음을 계산하고, studio `table_compare` 화면에 쓸 데이터셋을 계약 형식으로 만들어 주는 **화면 없는** 도구(CLI, 에이전트용). GUI는 만들지 않고 studio의 GUI 유형을 쓴다(README에 명시).
- **GUI 유형 `table_compare`**: 사람이 소스별 grid끼리 대조해 같음·다름·한쪽에만 있음 패턴을 파악하고, 범위·의미·대응·정제 여부를 고려해 보존·정제 후 보존·폐기·보류를 결정하며, 그 근거로 일관된 결정을 하도록 보조하는 스튜디오 화면 유형.
- studio 공통 틀: "사람이 XX끼리 대조해 YY를 파악하고 ZZ를 결정하며, 그 근거로 일관된 결정을 하도록 보조하는 화면 유형". 기존 kind(capture·record·conflict·program_link·quote)는 XX를 가리키는 관례.
- README에 반드시: 자동 판정 없음(결정은 사람이 studio에서), 원본 쓰기 없음, 로컬 전용, 결정 근거와 평가 데이터 분리, 규칙 버전·입력 해시 기록.

## 방법
하네스 v2.1(커밋 `f60ed11`): `scripts/collect_samples.py`(이름 하나당 단독 호출, 3회) + `scripts/check_terms.py`(규칙 판정) + **설명문 직접 읽기**(규칙만으로는 변별이 안 되어 최종 판정은 직접 읽기). 모델: gpt-6-luna(격리 실행기), Claude sonnet(`claude -p`, 도구·설정 없음). Qwen은 사용자 지시로 중단. 충돌: PyPI·npm·GitHub(PowerShell). 업무 용어 금지, 포괄어만. 모든 회차에 대조 이름(`auto-merge-tool` 등)을 넣어 규칙이 엉뚱한 이름을 통과시키는지 확인 — 전 회차 0/6.

## 최종 회차 (r12, 규칙 `repo_names_final.json`, 표본 `r12_final_*.jsonl`)
사용자 지정: 대상어 {grid, tabular} × 역할어 {builder, prep, dataset-prep, engine, core}, 조사 `compare` 허용 → 20개.

| 이름 | 충돌 | gpt | Claude | 직접 읽은 뜻 |
|---|---|---|---|---|
| **tabular-compare-engine** | 없음 | 3/3 | 3/3 | 표 데이터(CSV·엑셀·DB)를 비교해 행·열 추가·삭제·변경을 찾는 비교 엔진, diff 리포트용 핵심 로직. "자동 판정" 언급 0/6 |
| tabular-compare-core (차점) | 없음 | 3/3 | 3/3 | 표 비교 도구의 핵심 로직, UI·CLI 등 다른 패키지가 가져다 쓰는 core. 형제 패키지가 있다는 인상 |
| tabular-compare-prep | 없음 | 3/3 | 3/3 | 비교 전 열·타입·결측치 전처리 |
| tabular-compare-builder | 없음 | 3/3 | 3/3 | 비교 결과·비교 화면을 구성하는 빌더 |
| tabular-compare-dataset-prep | 없음 | 3/3 | 3/3 | Claude: 벤치마크 실험용 데이터 준비 |
| tabular-engine / tabular-core | 없음 | 3/3 | 3/3 | 범용 표 처리 라이브러리(비교 뜻 없음) |
| tabular-builder | 없음 | 3/3 | 3/3 | 콘솔·CSV·HTML 표 출력 빌더 패턴 |
| tabular-prep / tabular-dataset-prep | 없음 | 3/3 | 1/3, 0/3 | 머신러닝 전처리 |
| grid-compare-{prep,dataset-prep,engine,core} | 없음 | 1~3/3 | 2~3/3 | "표 또는 격자"로 흔들림, 시뮬레이션 격자·화면 비교 |
| grid-builder / grid-engine / grid-core | **GitHub 25★ / npm+283★ / PyPI+npm** | 0~3/3 | 0/3 | 레이아웃 생성·그리드 컴퓨팅·게임 렌더링 |
| grid-prep / grid-dataset-prep | 없음 | 2~3/3 | 0~1/3 | 격자 데이터 전처리 |

**결정 이유**: `tabular`는 10개 전부 "표 형태 데이터"로 안정, `grid`는 `compare`를 붙여도 격자로 흔들리고 순수 조합 3개는 이미 사용 중. `compare` 없는 10개는 비교 뜻을 전달하지 못함. `engine`은 "차이를 계산하는 핵심 로직"으로 읽혔고 판정 엔진 오독 없음. GUI 유형 `table_compare`와 계산 쪽/화면 쪽 짝. 어느 이름도 "사람이 결정"(ZZ)은 담지 못함 → README 몫.

## GUI 유형 최종 (g5~g8) — `grid_compare_triage`
경위: g4에서 `table_compare`를 골랐으나 사용자 기준(YY보다 XX·ZZ 중요, 사람의 action이 드러날 것)과 어긋나 철회. g5에서 처리 대상어(row·record·subset·case·mismatch), g6에서 집합어(record set·intersection·joint), g7에서 사용자가 원한 `grid`(사람 시야)와 `schema`(여러 DB 관계)를 시험. g6~g8은 **평가자 관점 3종**(개발자 / 최종 사용자 UX1 / UI·UX 설계자 UX2, `gui_kind_ux_variants.json`)으로 수집. 답변자 Sonnet·Haiku(gpt-6-luna는 이 기간 성공률 약 12%라 보조).

| 이름 | 개발자 | 사람(UX1·UX2) | 읽힌 화면 |
|---|---|---|---|
| **grid_compare_triage** (채택) | 2/6 오독("시뮬레이션 격자 출력") | 0/12 | 격자 형태 표에서 항목을 나란히 비교해 우선순위·범주로 분류 |
| grid_compare_record_triage | 0 | 0 | 레코드를 그리드로 나란히, 일치·불일치·누락·중복 확인 후 분류 (4단어라 제외) |
| tabular_compare_record_triage | 0 | 0 | 일치·다름·한쪽에만 있는 레코드 목록, 승인·무시·보류 (4단어라 제외) |
| tabular_compare_triage, *_case_triage | "자동화" 각 1건 → 게이트 제외 | | |
| *_intersection_triage | 0 | 0 | 교집합(양쪽 모두 있는 행) 중심으로 좁게 읽힘 |
| *_joint_triage | 0 | 0 | 흐릿함(joint가 더하는 뜻 없음) |
| *schema* 5개 | 2개 "자동" 제외 | 구조만 | 열 이름·타입 같은 **구조** 비교로 읽힘 → 레코드 처리 아님 |
| compare 없는 형태 | | | 대조 뜻 사라짐 |

**발견**: `grid`는 개발자 관점에서 격자·좌표로 읽히지만 사람 관점에서는 "행·열 격자로 나란히 놓은 표"로 읽힌다. 화면 유형 이름은 사람이 읽으므로 사용자가 **사람 관점 기준**으로 `grid_compare_triage`(3단어)를 채택. 개발자 관점 오독은 studio 맥락(다른 kind 목록)이 줄여 준다고 판단. `record`를 붙이면 개발자 관점 오독도 사라지지만 4단어.
**하네스 메모**: `collect_variants.py`가 출력 파일을 백엔드 이름으로 만들어 같은 백엔드의 두 모델(Sonnet·Haiku)이 한 파일에 섞이고 이어받기에서 서로 건너뜀(g6g7 UX2 Haiku 일부 누락). g8은 모델별 폴더로 분리해 회피.

## GUI 유형 g4 회차 (철회된 `table_compare` 근거, 규칙 `gui_kind_names_v4.json`, 표본 `g4_kind_*.jsonl`)
축: XX=`table`(grid·source·tabular는 앞 회차에서 격자·소스 코드·형용사로 탈락) × 동작 {YY: compare·diff / ZZ: triage·curate·curation·keep_drop·decide·verdict·review·select·judge·reconcile / 3단어 compare_triage·compare_decide·compare_review·diff_triage}. 대조 이름 `auto_merge`·`table_merge` 0/N. 판정: **6회 중 1회라도 오독이면 제외**(사용자 규칙) → 남은 것끼리 비교. gpt-6-luna 실행기가 이 회차에 약 75% "OMP prompt did not complete"로 실패해 gpt 표본은 이름당 0~4건, Claude는 전부 3/3.

| 이름 | Claude | gpt | 직접 읽은 뜻 | 판정 |
|---|---|---|---|---|
| **table_compare** | 3/3 | 4/4 | 두 표의 스키마·행 차이 확인, 마이그레이션·동기화 검증 | **확정**. XX+YY, 10건 오독 0 |
| table_compare_triage | 3/3 | 2/2 | 두 표를 비교해 차이를 분류·우선순위 정해 처리 | 차점. XX+YY+ZZ, 5건 오독 0. 3단어, "우선순위" 뉘앙스 |
| table_diff_triage | 3/3 | 1/1 | 위와 같음(diff) | 저장소 이름(compare)과 짝 안 맞음 |
| table_compare_review | 3/3 | 1/1 | 비교 후 검토, "리뷰 화면" 언급 | review는 보존·폐기 분류보다 약함 |
| table_diff | 3/3 | 2/2 | 추가·삭제·변경 행 찾기 | XX+YY, compare와 동의 |
| table_curate / table_curation | 3/3 | 2/2 | 불필요한 행·열 걸러 품질 좋은 데이터셋 만드는 **파이프라인** | ZZ는 읽히나 대조 없음, 도구가 수행 |
| table_keep_drop | 3/3 | 0/1 | 마이그레이션 때 남길 열·삭제할 열 **설정** | 대조 없음 |
| table_triage | 3/3 | 2/2 | **테이블 단위**로 어느 테이블을 먼저 처리할지 우선순위 | 단위 오독 → 제외 |
| table_reconcile | 3/3 | 2/2 | 불일치를 찾아 **맞춰 주는** 대사 | 도구가 결정 → 제외 |
| table_compare_decide | 3/3 | 1/1 | 비교 후 동기화·병합·업데이트를 **자동 선택하는 로직** | 제외 |
| table_decide | 3/3 | 1/1 | **의사결정 테이블** 룩업 분기 로직 | 제외 |
| table_verdict | 2/3 | 1/1 | 판정값 변수, **포커 게임 승패** | 제외 |
| table_review | 3/3 | 1/1 | 스키마 리뷰, **표 형식 리뷰 데이터** | 제외 |
| table_select | 3/3 | 2/2 | **SQL SELECT**, UI 행 선택 | 제외 |
| table_judge | 2/3 | 2/2 | 문서 이미지에서 **표 인식 판정**(capture와 겹침) | 제외 |

**결정 이유**: studio의 kind 관례(`capture`·`record`·`conflict`·`program_link`·`quote`)는 모두 **대조 대상(XX)**을 가리키고 결정(ZZ)을 이름에 넣은 유형이 없다. studio 자체가 "사람이 결정하는 화면" 틀이라 ZZ는 kind 이름이 아니라 틀이 담는다. `table_compare`는 저장소 `tabular-compare-engine`과 정확히 짝(엔진이 compare를 계산, studio가 compare를 보여 주고 사람이 결정)이고, 2단어라 `table_compare_server.py`·`ui/table_compare/` 관례에 맞으며, 표본이 가장 많고 전부 깨끗하다. ZZ를 이름에 꼭 넣으려면 `table_compare_triage`가 유일한 무오독 후보다.

## GUI 유형 회차 (이전)
| 회차 | 후보 | 결과 |
|---|---|---|
| g1 (`gui_kind_names.json`) | grid_diff, grid_match, grid_scope, grid_merge, grid_reconcile, table_diff, table_match, table_scope, table_merge, source_diff, source_grid, grid_decide | `table_diff`만 근접. source_diff=소스 코드, grid_*=격자·좌표·게임, *_merge=합치는 함수, *_scope=변수 |
| g2 (`gui_kind_names_v2.json`) | table_compare, table_diff, table_pair, grid_pair, table_region, source_table | **table_compare**·table_diff 6/6 의도대로. table_pair=자료구조, grid_pair=(행,열) 좌표, table_region=문서 표 바운딩박스(capture와 겹침), source_table=ETL 원본 → 사용자 `table_compare` 확정 |
| g3 (`gui_kind_names_v3.json`) | 사용자 후보 grid_region·grid_join·grid_join_condition + table_join·table_join_condition | 전부 SQL JOIN/ON 절·지도·전력망 격자로 읽힘. table_compare 유지 |

## 저장소 이름 회차 (요약)
| 회차 | 기준 | 결과 |
|---|---|---|
| r1~r4 (`repo_names.yaml` v1~4.1, 커밋 843fff8) | 엑셀·CSV→SQLite 탐색 | excel-csv-sqlite-explorer |
| r5 (5588253) | 포괄어 | local-tabular-data-explorer |
| r6 (8af3a3b) | 조회·탐색 | tabular-source-explorer |
| r7, r8 (`repo_names.yaml` v7~v8) | 통합 실행 / 통합 결정 지원 | consolidator / merge-decision-desk 근접. 목적 재정의로 폐기 |
| r9 (`repo_names_builder.json`) | studio 계열 접두어 + builder/engine | **전부 오독**: decision-=의사결정 테이블 규칙 엔진, studio-=노코드 편집기, dataset-builder=ML 학습용 |
| r10 (`repo_names_v10.json`) | table_compare 짝 + ZZ 필수 | XX만 읽히고 ZZ(보존·폐기) 안 읽힘. triage=우선순위 분류, keep-drop=열 선택, retention=보존 기간 |
| r11 (`repo_names_venn.json`) | venn(벤 다이어그램 연상) | 8개 전부 "벤 다이어그램을 그리는 도구". 이름 아닌 화면 설계 아이디어로만 유지 |
| **r12 (`repo_names_final.json`)** | 사용자 지정 조합 | **tabular-compare-engine** |

## 축적된 오독 사례 (다음 명명 때 피할 것)
`ldx`(약어)→뜻 불명 · `program-*`→앱 내부 데이터 · `grid`→격자·좌표·지도·게임 · `source_diff`→소스 코드 · `decision-`→의사결정 테이블 · `studio-`→노코드 편집기 · `*-dataset-builder`/`*-prep`→ML 학습·전처리 · `*_join*`→SQL · `merge_condition`→git · `*-condition-builder`→SQL ON 절 빌더 · `resolver`→자동 해결 · `reconciler`→도구가 맞춰 줌 · `venn`→차트 도구 · `table_region`→바운딩박스 · `compare`(초기 기준)→diff 도구(목적이 "나란히 보기"일 때는 오독, "차이 확인"일 때는 정답).

## 파일
규칙: `repo_names.yaml`(v8), `repo_names_builder.json`, `repo_names_v10.json`, `repo_names_venn.json`, `repo_names_final.json`, `gui_kind_names.json`, `gui_kind_names_v2.json`, `gui_kind_names_v3.json`. 표본: `repo_names_samples/`(옛 형식 `*_r?.json`·`*_p.json`은 하네스 v2.1에서 legacy, 새 형식 `r9_*`~`r12_*`, `g1_*`~`g3_*` jsonl). 위임 세션(self-naming) 파일 `*semh*`, `naming_*`, `repo_names_v11.json`은 이 커밋에 포함하지 않음.
