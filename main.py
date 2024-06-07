from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode
import io
from config import GITHUB_ACCESS_TOKEN

from langgraph.prebuilt import ToolNode, tools_condition
from tools.fetch_git_repo_info import GitHubAction
from router import router
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from PIL import Image
from langgraph.checkpoint.sqlite import SqliteSaver

memory = SqliteSaver.from_conn_string(":memory:")



# Setting up llm
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, streaming=True)
tool = GitHubAction
tools = [tool]

llm_with_tools = llm.bind_tools(tools)

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Create the MessageGraph
graph = StateGraph(State)

# Add the model node to the graph
graph.add_node("chatbot", chatbot)

# Add the tool node to the graph
tool_node = ToolNode(tools = tools)
graph.add_node("tools", tool_node)

# Set the entry point
graph.set_entry_point("chatbot")

graph.add_conditional_edges("chatbot", router)
# graph.set_finish_point("chatbot")

graph.add_edge("tools", "chatbot")


# Compile the graph
runnable = graph.compile(checkpointer=memory)

try:
    mermaid_png = runnable.get_graph().draw_mermaid_png()
    image = Image.open(io.BytesIO(mermaid_png))
    image.save("graph_visualization.png")
    print("Graph visualization saved as graph_visualization.png")
except Exception as e:
    print(f"Error generating or saving graph visualization: {e}")

# runnable.invoke("Who is the repository owner")

user_input = "find the last 30 commits in the repository"
config = {"configurable": {"thread_id": "1"}}

# The config is the **second positional argument** to stream() or invoke()!
events = runnable.stream(
    {"messages": [("user", user_input)]}, config, stream_mode="values"
)
for event in events:
    event["messages"][-1].pretty_print()

# Example usage
# repo_address = "langchain-ai/langchain"

# # Invoke the graph with the repository information
# response = runnable.invoke(
#     HumanMessage(
#         content="Fetch last 30 commits of a repository",
#         variables={"repo_address": repo_address, "github_token": GITHUB_ACCESS_TOKEN}
#     )
# )

# print(response)
