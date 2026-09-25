"""Supervisor graph for the chapter 6 local ASGI experiment."""

import os
import uuid

from deepagents import AsyncSubAgent, create_deep_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_openai import ChatOpenAI


class ScriptedModel(BaseChatModel):
    """Offline control: select one tool per command, then acknowledge its result."""

    @property
    def _llm_type(self):
        return "chapter-6-scripted-control"

    def bind_tools(self, tools, *, tool_choice=None, **kwargs):
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        if isinstance(messages[-1], ToolMessage):
            answer = AIMessage(content="Tool result recorded.")
        else:
            command = next(
                message.content for message in reversed(messages) if isinstance(message, HumanMessage)
            )
            action, _, payload = command.partition("|")
            if action == "START":
                name, args = "start_async_task", {"description": payload, "subagent_type": "researcher"}
            elif action == "CHECK":
                name, args = "check_async_task", {"task_id": payload}
            elif action == "LIST":
                name, args = "list_async_tasks", {"status_filter": "all"}
            elif action == "UPDATE":
                task_id, _, message = payload.partition("|")
                name, args = "update_async_task", {"task_id": task_id, "message": message}
            elif action == "CANCEL":
                name, args = "cancel_async_task", {"task_id": payload}
            else:
                raise ValueError(f"Unsupported scripted command: {action}")
            answer = AIMessage(content="", tool_calls=[{"name": name, "args": args, "id": str(uuid.uuid4())}])
        return ChatResult(generations=[ChatGeneration(message=answer)])


if os.getenv("CH06_SCRIPTED_MODEL") == "1":
    model = ScriptedModel()
else:
    model = ChatOpenAI(
        model=os.getenv("MODEL_NAME", "deepseek-chat"),
        api_key=os.environ["MODEL_API_KEY"],
        base_url=os.getenv("MODEL_BASE_URL", "https://api.deepseek.com"),
        temperature=0,
    )

graph = create_deep_agent(
    model=model,
    system_prompt=(
        "This is an async-subagent tool experiment. For each user request, call exactly the "
        "requested async task tool once, then stop. Use researcher for starts. Never invent a "
        "task ID or report a cached status as live."
    ),
    subagents=[
        AsyncSubAgent(
            name="researcher",
            description="A slow local research graph for observing background tasks.",
            graph_id="researcher",
        )
    ],
)
