# tabular-compare-engine

여러 소스의 표(엑셀·CSV·SQLite)를 **읽기 전용 사본**으로 받아 같음·다름·한쪽에만 있음을 계산하고, 사람이 `decision-labeling-studio`의 `grid_compare_triage` 화면에서 보존·정제 후 보존·폐기·보류를 결정하는 데 쓸 데이터셋을 만들어 주는 **화면 없는** 도구. 에이전트는 CLI(JSON 출력)로 쓴다. PC 안에서만 동작한다.

## 역할 경계

- **이 저장소**: 소스 등록(원본 불변 사본), 엑셀·CSV→SQLite 변환, 카탈로그(무엇이 어디에 있는지), 검색 색인, 읽기 전용 SQL + 결과 봉투(잘림·못 읽은 항목 표시), 소스 간 대조 계산, 데이터셋 내보내기. **자동 판정은 하지 않는다.**
- **GUI는 만들지 않는다.** 화면은 `decision-labeling-studio`의 GUI 유형 `grid_compare_triage`를 쓴다.
  > `grid_compare_triage` (이름은 바뀔 수 있음): 사람이 소스별 grid끼리 대조해 같음·다름·한쪽에만 있음 패턴을 파악하고, 범위·의미·대응·정제 여부를 고려해 그 패턴에 해당하는 레코드 집합을 조건 단위로 처리(현재 라벨: 보존·정제 후 보존·폐기·보류)할지 결정하며, 그 근거로 일관된 결정을 하도록 보조하는 스튜디오 화면 유형.
- **연결**: 버전 붙은 데이터 계약 파일(JSON 스키마 + 예제)로만 이어진다. studio `datasets/CONTRACT.md`의 `--dataset` 계약을 따르고, 판정은 데이터셋 해시에 묶여 studio 쪽 `--votes`에 저장된다.
- 판정·라벨·사유 기록은 studio 몫이다. 결정 근거와 평가 데이터는 분리하고, 규칙 버전·입력 경로·해시를 남겨 재현 가능하게 한다.

## 결정 (2026-11-02 ~ 11-04)

- MVP는 재사용 우선 경량 구조. Docker·PostgreSQL·OpenSearch는 넣지 않는다.
- DuckLocal·Octa는 기반으로 쓰지 않고 패턴만 차용한다. 근거: `subflows.yaml`, `docs/dependencies.md`.
- 이름: `docs/glossary/repo_names_results.md`. 작업명 `ldx`는 약어라 이름만으로 뜻이 전달되지 않아 폐기했다. 패키지·CLI의 짧은 이름은 미정.
- 설계 v1→v3.2와 적대 검증: `docs/architecture/`. GUI·OSS 벤치마킹: `docs/benchmarking/`. 용어 검증: `docs/glossary/`.

## 구조 (예정)

```text
<package>/
  adapters/   csv.py  xlsx.py  sqlite.py          파일 형식별 읽기 (추가 = 파일 1개)
  core/       catalog.py  query.py  search.py  compare.py  contracts.py
  cli.py      에이전트용, JSON만 출력
```

`web/`는 두지 않는다. 확장 지점은 adapter 등록, Retriever 인터페이스(벡터 검색은 나중), catalog 저장소, 데이터셋 계약의 네 곳만 연다.

## 원본 보호 규칙 (필수)

1. SQLite는 `?mode=ro` 또는 `ATTACH ... (TYPE sqlite, READ_ONLY)`로만 연다.
2. 쿼리는 실행 전에 읽기 전용 단일 문장인지 검사한다 (`json_serialize_sql`, DuckLocal `src/spec/mod.rs:400-430` 패턴).
3. 소스를 붙인 뒤 DuckDB 설정을 잠근다.
4. CP949 CSV를 지원하고, 한글 테이블·열 이름을 바꾸지 않는다.
5. 파일 수 제한이나 결과 잘림이 생기면 JSON에 표시하고 경고한다.

## 데이터 금지

`.gitignore`가 엑셀·CSV·SQLite·HWP·PDF와 `.ldx/` 사본을 막는다. 원본과 사본은 어떤 경우에도 커밋하지 않는다.

## 공개 전 검사 (필수)

이 저장소는 공개다. push 전에 `scripts/publish_check.py`가 세 가지를 막는다.

1. **금지어**: 내부 DB 파일명·사람 이름 같은 식별자. 목록은 저장소에 두지 않고 `~/.publish_denylist`(또는 환경변수 `PUBLISH_DENYLIST`)에서 읽는다. 목록이 없으면 검사가 실패한다. 형식은 `.publish_denylist.example` 참고.
2. **이미지**: 추적되는 모든 이미지는 `docs/benchmarking/gui_shots/MANIFEST.json`에 `"masked": true`로 올라 있어야 한다. 화면 캡처는 계정 아바타·이름·내부 경로를 가린 뒤 매니페스트에 적는다. 가리기 전 원본은 `gui_shots/raw/`에 두면 `.gitignore`가 막는다.
3. **데이터 파일**: 엑셀·CSV·SQLite·HWP·PDF가 어떤 경로로든 추적되면 실패.

클론 직후 한 번: `git config core.hooksPath .githooks` — 이후 `git push`마다 자동 실행. 수동: `python scripts/publish_check.py`.
