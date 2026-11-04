"""공개 전 검사. push 훅(.githooks/pre-push)과 수동 실행(python scripts/publish_check.py) 겸용.

검사 세 가지. 하나라도 걸리면 종료 코드 1.
1) 금지어: 추적되는 텍스트 파일에 내부 파일명·식별자가 있는가. 목록은 저장소 밖에서 읽는다
   (환경변수 PUBLISH_DENYLIST → 저장소의 .publish_denylist(gitignore됨) → ~/.publish_denylist).
   목록이 없으면 실패한다(fail-closed). 형식: 한 줄에 하나, # 주석.
2) 이미지: 추적되는 모든 이미지가 docs/benchmarking/gui_shots/MANIFEST.json에 masked:true로 올라 있는가.
   화면 캡처는 계정 아바타·이름·내부 경로를 가린 뒤 매니페스트에 적어야 커밋된다.
3) 데이터 파일: .gitignore가 막는 확장자(xlsx·csv·sqlite 등)가 어떤 경로로든 추적되고 있는가.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMG = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"}
DATA = {".xlsx", ".xlsm", ".xls", ".csv", ".tsv", ".db", ".sqlite", ".sqlite3", ".duckdb", ".parquet", ".hwp", ".hwpx", ".pdf"}
BIN = IMG | DATA | {".bin", ".lock", ".pyc", ".zip"}
MANIFEST = ROOT / "docs/benchmarking/gui_shots/MANIFEST.json"


def tracked() -> list[Path]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
    return [ROOT / p for p in out.decode("utf-8").split("\0") if p]


def denylist() -> list[str] | None:
    for p in (os.environ.get("PUBLISH_DENYLIST"), ROOT / ".publish_denylist", Path.home() / ".publish_denylist"):
        if p and Path(p).is_file():
            words = [w.strip() for w in Path(p).read_text(encoding="utf-8").splitlines()]
            return [w for w in words if w and not w.startswith("#")]
    return None


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    files = tracked()
    bad: list[str] = []

    words = denylist()
    if words is None:
        bad.append("금지어 목록 없음: PUBLISH_DENYLIST 또는 .publish_denylist(저장소 밖 보관, 커밋 금지)를 두세요")
    else:
        for f in files:
            if f.suffix.lower() in BIN:
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for w in words:
                if w.lower() in text.lower():
                    bad.append(f"금지어 '{w}': {f.relative_to(ROOT)}")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
    for f in files:
        if f.suffix.lower() in IMG:
            rel = f.relative_to(ROOT).as_posix()
            entry = manifest.get(rel)
            if not (isinstance(entry, dict) and entry.get("masked") is True):
                bad.append(f"매니페스트에 masked:true 없음: {rel}")

    for f in files:
        if f.suffix.lower() in DATA:
            bad.append(f"데이터 파일이 추적됨: {f.relative_to(ROOT)}")

    if bad:
        print("공개 전 검사 실패:\n  " + "\n  ".join(bad))
        return 1
    print(f"공개 전 검사 통과: 파일 {len(files)}개, 금지어 {len(words or [])}개, 이미지 {sum(f.suffix.lower() in IMG for f in files)}장")
    return 0


if __name__ == "__main__":
    sys.exit(main())
