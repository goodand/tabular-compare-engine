# 저장소 이름 검증 결과 (최종 2026-11-04)

> **확정: 저장소 `tabular-compare-engine`** — https://github.com/goodand/tabular-compare-engine.git (사용자가 생성)
> **GUI 유형(decision-labeling-studio `kind`): `table_compare`**
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

## GUI 유형 회차
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
