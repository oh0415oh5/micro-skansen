"""
micro-skansen MCP 서버 유닛 테스트
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.server import (
    get_project_status,
    read_file,
    write_file,
    list_directory,
    check_env_keys,
    save_note,
    list_notes,
)


def test_get_project_status():
    result = get_project_status()
    assert "project" in result
    assert result["project"] == "micro-skansen"
    assert "files" in result
    assert isinstance(result["total_files"], int)


def test_list_directory_root():
    items = list_directory()
    assert isinstance(items, list)
    assert len(items) > 0


def test_list_directory_src():
    items = list_directory("src")
    assert any("server.py" in item for item in items)


def test_read_file_readme():
    content = read_file("README.md")
    assert "[오류]" not in content
    assert len(content) > 0


def test_read_file_not_found():
    result = read_file("nonexistent_file.txt")
    assert "오류" in result


def test_write_and_read_file(tmp_path, monkeypatch):
    import src.server as srv
    monkeypatch.setattr(srv, "ROOT", tmp_path)
    write_result = write_file("test_output.txt", "hello skansen")
    assert "완료" in write_result
    read_result = read_file("test_output.txt")
    assert read_result == "hello skansen"


def test_check_env_keys_no_file():
    result = check_env_keys()
    assert "keys" in result


def test_save_and_list_notes(tmp_path, monkeypatch):
    import src.server as srv
    monkeypatch.setattr(srv, "NOTES_FILE", tmp_path / ".notes.json")
    save_result = save_note("테스트 메모", "내용입니다")
    assert "완료" in save_result
    notes = list_notes()
    assert any(n.get("title") == "테스트 메모" for n in notes)
