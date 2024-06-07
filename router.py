from typing import Literal, List
from langchain_core.messages import BaseMessage

def router(state: List[BaseMessage]) -> Literal["fetch_git_repo_info", "__end__"]:
    tool_calls = state[-1].additional_kwargs.get("tool_calls", [])
    if len(tool_calls):
        return "fetch_git_repo_info"
    else:
        return "__end__"
