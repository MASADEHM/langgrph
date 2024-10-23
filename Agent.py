import os, getpass
from langchain_core.messages import AnyMessage,SystemMessage,HumanMessage
from langgraph.graph import MessagesState,StateGraph,START,END
from langchain_openai.chat_models import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import ToolNode,tools_condition
from IPython.display import Image,display

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

_set_env("OPENAI_API_KEY")

#tool
@tool
def multiply(a:int,b:int)->int:
    """
    Multiply a and b
    Args:
        a: first number
        b: second number
    """
    return {a*b}


tools = [multiply]
# Define LLM with bound tools
llm=ChatOpenAI() #ChatOpenAI(model="gpt-4o")
llmwithtools=llm.bind_tools(tools)

#Initlaize system message
sys_msg= SystemMessage(content="your name is Emy you're helpful assistant!")

#Node using build in message state
def assistant(state:MessagesState):
    return {'messages':llmwithtools.invoke([sys_msg]+state["messages"])}

#build graph
builder=StateGraph(MessagesState)
builder.add_node("assistant",assistant)
builder.add_node("tools",ToolNode(tools))

builder.add_edge(START,"assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools","assistant")

graph=builder.compile()
#display(Image(graph.get_graph().draw_mermaid_png(output_file_path="./agent.png")))

response=graph.invoke({"messages":HumanMessage(content="hello, multiply 2 and 3")})
print(response)
