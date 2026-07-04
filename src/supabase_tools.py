"""
Supabase 연동 MCP 툴
.env에 SUPABASE_URL 과 SUPABASE_KEY 를 설정하세요.
"""
import os
import httpx
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

mcp = FastMCP(name="micro-skansen-supabase")


def _headers() -> dict:
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }


@mcp.tool()
def supabase_select(table: str, limit: int = 20) -> dict:
    """
    Supabase 테이블에서 데이터를 조회합니다.
    table: 테이블 이름, limit: 최대 행 수 (default 20)
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        return {"error": ".env에 SUPABASE_URL과 SUPABASE_KEY를 설정하세요."}
    url = f"{SUPABASE_URL}/rest/v1/{table}?limit={limit}"
    resp = httpx.get(url, headers=_headers(), timeout=10)
    return {"status": resp.status_code, "data": resp.json()}


@mcp.tool()
def supabase_insert(table: str, row: dict) -> dict:
    """
    Supabase 테이블에 새 행을 삽입합니다.
    table: 테이블 이름, row: 삽입할 데이터 dict
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        return {"error": ".env에 SUPABASE_URL과 SUPABASE_KEY를 설정하세요."}
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    resp = httpx.post(url, headers=_headers(), json=row, timeout=10)
    return {"status": resp.status_code, "data": resp.text}


@mcp.tool()
def supabase_delete(table: str, match: dict) -> dict:
    """
    Supabase 테이블에서 조건에 맞는 행을 삭제합니다.
    table: 테이블 이름, match: {"column": "value"} 형식
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        return {"error": ".env에 SUPABASE_URL과 SUPABASE_KEY를 설정하세요."}
    params = "&".join(f"{k}=eq.{v}" for k, v in match.items())
    url = f"{SUPABASE_URL}/rest/v1/{table}?{params}"
    resp = httpx.delete(url, headers=_headers(), timeout=10)
    return {"status": resp.status_code, "data": resp.text}


@mcp.tool()
def supabase_list_tables() -> dict:
    """
    Supabase 프로젝트의 public 스키마 테이블 목록을 반환합니다.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        return {"error": ".env에 SUPABASE_URL과 SUPABASE_KEY를 설정하세요."}
    url = f"{SUPABASE_URL}/rest/v1/"
    resp = httpx.get(url, headers=_headers(), timeout=10)
    return {"status": resp.status_code, "data": resp.json()}


if __name__ == "__main__":
    mcp.run(transport="stdio")
