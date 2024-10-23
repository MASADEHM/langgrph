import random
from IPython.display import Image,display # type: ignore
from typing import Literal
from typing_extensions import TypedDict # type: ignore
from langgraph.graph import StateGraph,START,END # type: ignore

# State
class State(TypedDict):
    graphstate:str
    
# Nodes
def node_1(state):
    print("---Node 1---")
    return {"graph_state":state['graph_state'] +" I am"}

def node_2(state):
    print("---Node 2---")
    return {"graph_state":state['graph_state'] +" happy!"}

def node_3(state):
    print("---Node 3---")
    return {"graph_state":state['graph_state'] +" sad!"}



# Conditional edge
def decide_mood(state) -> Literal["node_2", "node_3"]:
    
    # Often, we will use state to decide on the next node to visit
    user_input = state['graph_state'] 
    
    # Here, let's just do a 50 / 50 split between nodes 2, 3
    if random.random() < 0.5:

        # 50% of the time, we return Node 2
        return "node_2"
    
    # 50% of the time, we return Node 3
    return "node_3"

#build the grpah
builder=StateGraph(State)
builder.add_node("node_1",node_1)
builder.add_node("node_2",node_2)
builder.add_node("node_3",node_3)

#logic
builder.add_edge(START,"node_1")
builder.add_edge("node_2",END)
builder.add_edge("node_3",END)
builder.add_conditional_edges("node_1",decide_mood)

#compile the graph
graph=builder.compile()
#view
display(Image(graph.get_graph().draw_mermaid_png(output_file_path="./graph.png")))