from langgraph.graph import (
    END,
    StateGraph,
)

from app.graph.nodes import (
    diagnostic_node,
    log_node,
    route_alert,
    ticket_node,
)

from app.graph.state import (
    AlertState,
)

workflow = StateGraph(
    AlertState
)

workflow.add_node(
    "log_node",
    log_node,
)

workflow.add_node(
    "ticket_node",
    ticket_node,
)

workflow.add_node(
    "diagnostic_node",
    diagnostic_node,
)

workflow.set_conditional_entry_point(
    route_alert,
    {
        "log_node": "log_node",
        "ticket_node": "ticket_node",
        "diagnostic_node":
            "diagnostic_node",
    },
)

workflow.add_edge(
    "log_node",
    END,
)

workflow.add_edge(
    "ticket_node",
    END,
)

workflow.add_edge(
    "diagnostic_node",
    END,
)

alert_graph = workflow.compile()