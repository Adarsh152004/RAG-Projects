from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from config import model
from tools import calculator

messages = []

llm_with_tools = model.bind_tools([calculator])

def start_chat(system_prompt):
    global messages
    messages = [SystemMessage(content=system_prompt)]

def chat(user_input):
    messages.append(HumanMessage(content=user_input))

    # This will store the complete AI response
    full_response = ""

    # Stream the response
    for chunk in llm_with_tools.stream(messages):
        print(chunk.content, end="", flush=True)
        full_response += chunk.content

    print()
    
    messages.append(AIMessage(content=full_response))
    return full_response
