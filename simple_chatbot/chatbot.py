from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    ToolMessage,
)
from config import model
from tools import TOOLS


messages = []

# Dictionary of all available tools
# tools = {
#     "calculator": calculator,
# }

llm_with_tools = model.bind_tools(TOOLS)

# Create a name -> tool mapping
tools = {tool.name: tool for tool in TOOLS}

def start_chat(system_prompt):
    global messages
    messages = [SystemMessage(content=system_prompt)]


def chat(user_input):
    global messages

    # Add user's message
    messages.append(HumanMessage(content=user_input))

    # First LLM call
    response = llm_with_tools.invoke(messages)

    # Keep executing tools until the model stops requesting them
    while response.tool_calls:

        # Save AI message containing the tool call
        messages.append(response)

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool = tools[tool_name]

            # Execute the tool
            result = tool.invoke(tool_call["args"])

            # Send tool result back to the model
            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"],
                )
            )

        # Ask the model again
        response = llm_with_tools.invoke(messages)

    # Print final answer
    print(response.content)

    # Save final AI response
    messages.append(response)

    return response.content