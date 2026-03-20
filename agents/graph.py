from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from agents.nodes import analyze_room, generate_options, retrieve_candidates
from agents.state import DesignState


def build_graph():
    graph = StateGraph(DesignState)
    graph.add_node("analyze_room", analyze_room)
    graph.add_node("retrieve_candidates", retrieve_candidates)
    graph.add_node("generate_options", generate_options)

    graph.add_edge(START, "analyze_room")
    graph.add_edge("analyze_room", "retrieve_candidates")
    graph.add_edge("retrieve_candidates", "generate_options")
    graph.add_edge("generate_options", END)

    return graph.compile()
