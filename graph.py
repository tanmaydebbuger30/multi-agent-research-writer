from langgraph.graph import END, START, StateGraph

from agents.critic import critic
from agents.researcher import researcher
from agents.writer import writer
from config import MAX_REVISIONS
from state import State

def route_after_critic(state: State) -> str:
    if state["critique"].approved or state["revisions"] >= MAX_REVISIONS:
        return END
    return "writer"


def build_graph():
    graph = StateGraph(State)

    graph.add_node("researcher", researcher)
    graph.add_node("writer", writer)
    graph.add_node("critic", critic)
    graph.add_edge(START, "researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", "critic")
    graph.add_conditional_edges("critic", route_after_critic, {"writer" : "writer", END : END}) 

    return graph.compile()