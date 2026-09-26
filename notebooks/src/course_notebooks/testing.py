"""A scripted model that drives real Agent/tool loops, never fabricated final state."""
from collections.abc import Callable, Sequence
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.utils.function_calling import convert_to_openai_tool
from pydantic import Field


class ScriptedChatModel(BaseChatModel):
    """The chapter supplies an inspectable response function; tools execute normally."""

    responder: Callable[[list[BaseMessage], tuple[str, ...]], AIMessage] = Field(exclude=True)
    tool_names: tuple[str, ...] = ()

    @property
    def _llm_type(self) -> str:
        return "course-scripted-model"

    def bind_tools(self, tools: Sequence[Any], *, tool_choice=None, **kwargs):
        names = tuple(convert_to_openai_tool(tool)["function"]["name"] for tool in tools)
        return self.model_copy(update={"tool_names": names})

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        response = self.responder(messages, self.tool_names)
        if not isinstance(response, AIMessage):
            raise TypeError("脚本模型必须返回 AIMessage；Agent 状态由实际框架产生。")
        return ChatResult(generations=[ChatGeneration(message=response)])
