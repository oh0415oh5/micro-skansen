"""
micro-skansen MCP 서버

Cursor / Claude Desktop 에서 아래처럼 연결하세요:
  npx -y fastmcp run src/server.py
  또는
  python src/server.py
"""

import os
import json
from pathlib import Path
from datetime import datetime

from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

# ── MCP 서버 인스턴스 ──────────────────────────────────────────
mcp = FastMCP(
    name="micro-skansen",
    version="0.1.0",
    description="SKANSEN 프로젝트 전용 MCP 서버 — 파일 탐색, 문서 조회, 상태 점검 도구 제공",
)

ROOT = Path(__file__).resolve().parent.parent


# ── 도구 1: 프로젝트 상태 점검 ────────────────────────────────
@mcp.tool()
def get_project_status() -> dict:
    """
    micro-skansen 프로젝트의 현재 상태를 반환합니다.
    파일 목록, Python 버전, 환경 변수 여부 등을 포함합니다.
    """
    files = sorted(
        str(p.relative_to(ROOT))
        for p in ROOT.rglob("*")
        if p.is_file()
        and not any(part.startswith(".") for part in p.parts)
        and "__pycache__" not in str(p)
    )
    return {
        "project": "micro-skansen",
        "checked_at": datetime.utcnow().isoformat() + "Z",
        "root": str(ROOT),
        "total_files": len(files),
        "files": files,
        "has_requirements": (ROOT / "requirements.txt").exists(),
        "has_env": (ROOT / ".env").exists(),
        "python_version": os.popen("python3 --version").read().strip(),
    }


# ── 도구 2: 파일 읽기 ─────────────────────────────────────────
@mcp.tool()
def read_file(path: str) -> str:
    """
    프로젝트 내 파일의 내용을 읽어 반환합니다.
    path는 프로젝트 루트 기준 상대 경로입니다. (예: 'README.md', 'src/server.py')
    """
    target = ROOT / path
    if not target.exists():
        return f"[오류] 파일을 찾을 수 없습니다: {path}"
    if not target.is_file():
        return f"[오류] 디렉토리입니다: {path}"
    try:
        return target.read_text(encoding="utf-8")
    except Exception as e:
        return f"[오류] 파일 읽기 실패: {e}"


# ── 도구 3: 파일 쓰기 ─────────────────────────────────────────
@mcp.tool()
def write_file(path: str, content: str) -> str:
    """
    프로젝트 내 파일에 내용을 씁니다 (없으면 생성).
    path는 프로젝트 루트 기준 상대 경로입니다.
    """
    target = ROOT / path
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"[완료] {path} 저장됨 ({len(content)} bytes)"
    except Exception as e:
        return f"[오류] 파일 쓰기 실패: {e}"


# ── 도구 4: 디렉토리 목록 ─────────────────────────────────────
@mcp.tool()
def list_directory(subdir: str = "") -> list[str]:
    """
    지정 디렉토리의 파일/폴더 목록을 반환합니다.
    subdir를 비우면 프로젝트 루트를 탐색합니다.
    """
    target = ROOT / subdir if subdir else ROOT
    if not target.exists():
        return [f"[오류] 경로 없음: {subdir}"]
    return sorted(
        ("📁 " if p.is_dir() else "📄 ") + p.name
        for p in target.iterdir()
        if not p.name.startswith(".")
    )


# ── 도구 5: 환경 변수 점검 ────────────────────────────────────
@mcp.tool()
def check_env_keys() -> dict:
    """
    .env 파일에 정의된 환경 변수 키 목록을 반환합니다 (값은 노출하지 않음).
    """
    env_file = ROOT / ".env"
    if not env_file.exists():
        return {"status": "no .env file found", "keys": []}
    keys = []
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            keys.append(line.split("=", 1)[0])
    return {"status": "ok", "keys": keys, "count": len(keys)}


# ── 도구 6: 메모 저장/조회 ────────────────────────────────────
NOTES_FILE = ROOT / ".skansen_notes.json"


@mcp.tool()
def save_note(title: str, content: str) -> str:
    """프로젝트 메모를 로컬에 저장합니다."""
    notes = json.loads(NOTES_FILE.read_text()) if NOTES_FILE.exists() else []
    notes.append({"title": title, "content": content, "saved_at": datetime.utcnow().isoformat() + "Z"})
    NOTES_FILE.write_text(json.dumps(notes, ensure_ascii=False, indent=2))
    return f"[완료] 메모 저장됨: '{title}'"


@mcp.tool()
def list_notes() -> list[dict]:
    """저장된 프로젝트 메모 목록을 반환합니다."""
    if not NOTES_FILE.exists():
        return [{"info": "저장된 메모가 없습니다."}]
    return json.loads(NOTES_FILE.read_text())


# ── 엔트리포인트 ──────────────────────────────────────────────
def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
