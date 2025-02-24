# Import relevant functionality
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
import speech
import serial
from dotenv import load_dotenv
# Set your Google API Key (You need to replace "your-google-api-key" with your actual key)

conversation_history = []
load_dotenv()
@tool
def check_heart_rate():
    """Calls the esp32 to run the heart rate sensor to check heartrate and oxygen level. Tell the user to place their finger on the heart rate sensor when the led lights up."""
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    speech.tts("Sure! Just place your finger on the sensor when the light is on.")
    ser.write("ready".encode())
    heart_rate = ""
    while not (heart_rate):
        heart_rate = ser.readline().decode('utf-8').strip()
    print(heart_rate)
    return heart_rate
# Create the agent


memory = MemorySaver()
model = ChatGoogleGenerativeAI(model="gemini-pro")
tools = [check_heart_rate]
agent_executor = create_react_agent(model, tools, checkpointer=memory)
while True:
    speech.launch_fn()
    transcription = speech.transcribe()
    transcription = "You are a helpful assistant. Please respond to the following query: " + transcription
    conversation_history.append(HumanMessage(content=transcription))
    # Use the agent
    config = {"configurable": {"thread_id": "abc123"}}
    for step in agent_executor.stream(
        {"messages": conversation_history},
        config,
        stream_mode="values",
    ):
        pass
    ai_message = step["messages"][-1].content
    speech.tts(ai_message)
    conversation_history.append(AIMessage(content=step["messages"][-1].content))