from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import END, MessageGraph
from langgraph.prebuilt import ToolNode
import io
from config import GITHUB_ACCESS_TOKEN

from langgraph.prebuilt import ToolNode
from tools.fetch_git_repo_info import fetch_git_repo_info
from router import router

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, streaming=True)
model_with_tools = model.bind_tools([fetch_git_repo_info])
from PIL import Image

# Create the MessageGraph
graph = MessageGraph()

# Add the model node to the graph
graph.add_node("chatbot", model_with_tools)

# Add the tool node to the graph
tool_node = ToolNode([fetch_git_repo_info])
graph.add_node("fetch_git_repo_info", tool_node)

# Connect the nodes
graph.add_edge("fetch_git_repo_info", END)
# graph.add_edge("oracle", END)

# Set the entry point
graph.set_entry_point("chatbot")

graph.add_conditional_edges("chatbot", router)

# Compile the graph
runnable = graph.compile()

# try:
#     mermaid_png = runnable.get_graph().draw_mermaid_png()
#     image = Image.open(io.BytesIO(mermaid_png))
#     image.save("graph_visualization.png")
#     print("Graph visualization saved as graph_visualization.png")
# except Exception as e:
#     print(f"Error generating or saving graph visualization: {e}")

# Example usage
repo_address = "langchain-ai/langchain"

# Invoke the graph with the repository information
response = runnable.invoke(
    HumanMessage(
        content="Fetch last 30 commits of a repository",
        variables={"repo_address": repo_address, "github_token": GITHUB_ACCESS_TOKEN}
    )
)

print(response)
