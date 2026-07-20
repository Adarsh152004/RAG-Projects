from langchain.messages import HumanMessage, ToolMessage
# from langchain.agents import create_react_agent, AgentExecutor
# from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper
from langchain_experimental.tools import PythonREPLTool

# from langchain_tavily import TavilySearch  # Add apikey

# tavily = TavilySearch(max_results=5)

@tool
def calculator(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

duckduckgo = DuckDuckGoSearchRun()

wiki = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper()
)

arxiv = ArxivQueryRun(
    api_wrapper=ArxivAPIWrapper()
)

python_repl = PythonREPLTool()

TOOLS = [
    calculator,
    duckduckgo,
    wiki,
    arxiv,
    python_repl,
]

# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a helpful assistant."),
#     ("human", "{input}"),
#     ("placeholder", "{agent_scratchpad}"),
# ])

# agent = create_react_agent(
#     llm=model,
#     tools=[calculator],
#     prompt=prompt
# )

# agent_executor = AgentExecutor(
#     agent=agent,
#     tools=[calculator],
#     verbose=True
# )

# response = agent_executor.invoke({"input": "What is 1+1?"})

# print(response)