from typing import Literal, List
from langchain_core.messages import BaseMessage

def router(state: List[BaseMessage]) -> Literal["tools", "__end__"]:
    tool_calls = state[-1].additional_kwargs.get("tool_calls", [])
    if len(tool_calls):
        return "tools"
    else:
        return "__end__"
