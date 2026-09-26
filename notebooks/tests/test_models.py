import pytest
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import tool

from course_notebooks.model_config import create_model, selected_mode
from course_notebooks.testing import ScriptedChatModel


@pytest.fixture(autouse=True)
def clean_config(monkeypatch):
    import os
    for key in list(os.environ):
        if key.startswith(("MODEL_", "SILICONFLOW_", "COURSE_")):
            monkeypatch.delenv(key)


def test_default_offline_ignores_credentials_and_dotenv(tmp_path, monkeypatch):
    monkeypatch.setenv("SILICONFLOW_API_KEY", "do-not-use")
    (tmp_path / ".env").write_text("COURSE_MODE=live\nMODEL_API_KEY=do-not-use\n")
    scripted = ScriptedChatModel(responder=lambda messages, tools: AIMessage(content="offline"))
    assert create_model(scripted, root=tmp_path) is scripted
    assert selected_mode() == "offline"


def test_live_requires_credentials_without_fallback(tmp_path):
    with pytest.raises(ValueError, match="SILICONFLOW_API_KEY"):
        create_model(None, root=tmp_path, mode="live")


def test_generic_provider_configuration_cannot_mix_with_siliconflow(tmp_path, monkeypatch):
    monkeypatch.setenv("MODEL_API_KEY", "example-generic-key")
    monkeypatch.setenv("SILICONFLOW_API_KEY", "example-siliconflow-key")
    with pytest.raises(ValueError, match="MODEL_BASE_URL"):
        create_model(None, root=tmp_path, mode="live")


def test_complete_generic_provider_and_unknown_mode(tmp_path, monkeypatch):
    monkeypatch.setenv("MODEL_API_KEY", "example-generic-key")
    monkeypatch.setenv("MODEL_BASE_URL", "http://127.0.0.1:9999/v1")
    monkeypatch.setenv("MODEL_NAME", "example-model")
    model = create_model(None, root=tmp_path, mode="live")
    assert model.model_name == "example-model"
    assert str(model.openai_api_base) == "http://127.0.0.1:9999/v1"
    with pytest.raises(ValueError, match="offline.*live"):
        selected_mode("automatic")


def test_scripted_model_runs_real_tool_and_receives_tool_result():
    seen = []

    @tool
    def echo(text: str) -> str:
        """Return the supplied text."""
        seen.append(text)
        return f"echo: {text}"

    def reply(messages, tools):
        assert "echo" in tools
        if isinstance(messages[-1], ToolMessage):
            assert messages[-1].content == "echo: hello"
            return AIMessage(content="done")
        return AIMessage(content="", tool_calls=[{
            "id": "echo-1", "name": "echo", "args": {"text": "hello"},
        }])

    agent = create_agent(model=ScriptedChatModel(responder=reply), tools=[echo])
    result = agent.invoke({"messages": [("user", "echo hello")]})
    assert seen == ["hello"]
    assert result["messages"][-1].content == "done"
