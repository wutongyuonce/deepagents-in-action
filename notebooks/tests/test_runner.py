import json
import sys
from pathlib import Path

import nbformat
import pytest

from course_notebooks.run import run_entries, validate_catalog


def make_repo(tmp_path, sources):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts/chapters.json").write_text(json.dumps({"ch01-agent-harness": {}}))
    entries = []
    for name, source in sources.items():
        relative = f"ch01/{name}.ipynb"
        path = tmp_path / "notebooks" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(source)]), path)
        entries.append({"id": name, "path": relative, "chapter_id": "ch01-agent-harness",
                        "title": name, "dependencies": [], "services": [], "model": "optional"})
    (tmp_path / "notebooks/catalog.json").write_text(json.dumps({"schema_version": 1, "notebooks": entries}))
    return entries


def test_project_kernel_ignores_user_kernel_and_offline_keys(tmp_path, monkeypatch):
    entries = make_repo(tmp_path, {"ok": f"import sys, os\nassert sys.executable == {sys.executable!r}\nassert not os.getenv('MODEL_API_KEY')\nassert os.getenv('COURSE_MODE') == 'offline'\nprint('isolated')"})
    bad = tmp_path / "foreign/kernels/python3"
    bad.mkdir(parents=True)
    (bad / "kernel.json").write_text(json.dumps({"argv": ["/nonexistent/python", "{connection_file}"], "language": "python", "display_name": "bad"}))
    monkeypatch.setenv("JUPYTER_PATH", str(tmp_path / "foreign"))
    monkeypatch.setenv("MODEL_API_KEY", "must-not-reach-kernel")
    report = run_entries(entries, tmp_path, tmp_path / "output", mode="offline", timeout=30)
    assert report["results"][0]["status"] == "passed"
    assert (tmp_path / "output/ok.html").exists()
    assert (tmp_path / "output/ok.md").exists()
    assert report["results"][0]["source_hash"]


def test_failed_cell_stops_batch_and_does_not_reuse_saved_outputs(tmp_path):
    entries = make_repo(tmp_path, {"bad": "assert False, 'deliberate failure'", "later": "print('not run')"})
    report = run_entries(entries, tmp_path, tmp_path / "output", mode="offline", timeout=30)
    assert [r["status"] for r in report["results"]] == ["failed", "not_run"]
    saved = nbformat.read(tmp_path / "output/bad.ipynb", as_version=4)
    assert saved.cells[0].outputs[0].output_type == "error"
    assert not (tmp_path / "output/later.ipynb").exists()


def test_catalog_rejects_unknown_chapter_and_missing_local_link(tmp_path):
    entries = make_repo(tmp_path, {"ok": "print('ok')"})
    entries[0]["chapter_id"] = "ch99-missing"
    with pytest.raises(ValueError, match="chapter"):
        validate_catalog(tmp_path, entries)
    entries[0]["chapter_id"] = "ch01-agent-harness"
    path = tmp_path / "notebooks/ch01/ok.ipynb"
    nb = nbformat.read(path, as_version=4)
    nb.cells.append(nbformat.v4.new_markdown_cell("[missing](does-not-exist.md)"))
    nbformat.write(nb, path)
    with pytest.raises(ValueError, match="does-not-exist"):
        validate_catalog(tmp_path, entries)
