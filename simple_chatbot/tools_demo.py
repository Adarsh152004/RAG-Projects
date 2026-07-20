from langchain.tools import tool
from langchain.messages import HumanMessage, ToolMessage

@tool
def calculator(a: int, b: int) -> int:
    """Add two numbers and return the result"""
    return a + b

query = HumanMessage(content="What is the result of 2+2")

from config import model

tool_model = model.bind_tools([calculator])

# First LLM call
ai_msg = tool_model.invoke([query])

print(ai_msg.tool_calls)

# Execute tool
tool_call = ai_msg.tool_calls[0]
tool_result = calculator.invoke(tool_call["args"])

# create ToolMessage
tool_msg = ToolMessage(
    content=str(tool_result),
    tool_call_id=tool_call["id"]
)

# Second LLM call
final = tool_model.invoke([
    query, ai_msg, tool_msg
])

print(final.content)

