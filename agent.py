# Import relevant functionality
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
import test
import os

# Set your Google API Key (You need to replace "your-google-api-key" with your actual key)
os.environ["GOOGLE_API_KEY"] = "AIzaSyBAubIEIMx7Es1bKIs-n9e6pxHEajcDsPg"
conversation_history = []

@tool
def hello_world_tool() -> str:
    """Returns a simple Hello World message."""
    return "Hello World!"
# Create the agent


memory = MemorySaver()
model = ChatGoogleGenerativeAI(model="gemini-pro")
tools = [hello_world_tool]
agent_executor = create_react_agent(model, tools, checkpointer=memory)
while True:
    test.launch_fn()
    transcription = test.transcribe()
    transcription = "You are a helpful assistant. Please respond to the following query: " + transcription
    conversation_history.append(HumanMessage(content=transcription))
    # Use the agent
    config = {"configurable": {"thread_id": "abc123"}}
    for step in agent_executor.stream(
        {"messages": conversation_history},
        config,
        stream_mode="values",
    ):
        step["messages"][-1].pretty_print()
        conversation_history.append(AIMessage(content=step["messages"][-1].content))