import uuid

from loguru import logger

from app.graph.state import (
    AlertState,
)


def log_node(
    state: AlertState,
) -> AlertState:
    """
    NORMAL alert handler.
    """

    logger.info(
        f"NORMAL machine state for "
        f"{state['machine_id']}"
    )

    state["notification_sent"] = False

    return state


def ticket_node(
    state: AlertState,
) -> AlertState:
    """
    ANOMALY ticket generator.
    """

    logger.warning(
        f"Creating maintenance ticket for "
        f"{state['machine_id']}"
    )

    ticket_id = (
        f"TICKET-{uuid.uuid4().hex[:8]}"
    )

    state["ticket_created"] = True

    state["ticket_id"] = ticket_id

    state["notification_sent"] = True

    return state


def diagnostic_node(
    state: AlertState,
) -> AlertState:
    """
    CRITICAL diagnostic generator.
    """

    logger.error(
        f"CRITICAL condition detected for "
        f"{state['machine_id']}"
    )

    report = (
        f"CRITICAL ALERT\n\n"
        f"Machine: {state['machine_id']}\n"
        f"Anomalous Features: "
        f"{', '.join(state['anomalous_features'])}\n\n"
        f"Immediate shutdown recommended.\n"
        f"Inspect spindle motor, cooling system, "
        f"and torque assembly."
    )

    dispatch_order = (
        f"DISPATCH-"
        f"{uuid.uuid4().hex[:6]}"
    )

    state["diagnostic_report"] = (
        report
    )

    state["dispatch_order"] = (
        dispatch_order
    )

    state["notification_sent"] = True

    return state


def route_alert(
    state: AlertState,
):
    """
    Conditional alert router.
    """

    tier = state["alert_tier"]

    logger.info(
        f"Routing alert tier: {tier}"
    )

    if tier == "NORMAL":
        return "log_node"

    elif tier == "ANOMALY":
        return "ticket_node"

    else:
        return "diagnostic_node"