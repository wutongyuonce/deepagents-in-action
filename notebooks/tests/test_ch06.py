import asyncio
import importlib.util
from pathlib import Path
import socket

import pytest


def server_class():
    chapter = Path(__file__).parents[1] / "ch06"
    spec = importlib.util.spec_from_file_location("chapter_server", chapter / "local_server.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.LocalAgentServer, chapter


def test_pending_task_failure_closes_real_server(monkeypatch):
    monkeypatch.setenv("COURSE_MODE", "offline")
    cls, chapter = server_class()
    server = cls(chapter, chapter.parents[1])

    async def fail_after_start():
        async with server:
            state = await server.client.runs.wait(server.parent_id, "supervisor", input={"messages": [{"role": "user", "content": "START|cleanup regression"}]})
            assert state["async_tasks"]
            assert any(task["status"] == "running" for task in state["async_tasks"].values())
            # Do not manually register task IDs: cleanup must recover them from parent state.
            raise ValueError("injected notebook failure")

    with pytest.raises(ValueError, match="injected notebook failure"):
        asyncio.run(fail_after_start())
    assert server.process.poll() is not None
    assert not server.workdir.exists()
    with socket.socket() as sock:
        sock.settimeout(1)
        assert sock.connect_ex(("127.0.0.1", server.port)) != 0
    assert server.cleaned_task_ids
    assert server.log_path.exists()
    server.log_path.unlink()


def test_startup_failure_cleans_temporary_directory(tmp_path):
    cls, _ = server_class()
    server = cls(tmp_path / "missing-chapter", tmp_path)

    async def start():
        async with server:
            pytest.fail("missing service source must not start")

    with pytest.raises(FileNotFoundError):
        asyncio.run(start())
    assert not server.workdir.exists()
    server.log_path.unlink()
