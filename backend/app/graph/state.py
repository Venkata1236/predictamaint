from typing import List, Optional

from typing_extensions import TypedDict


class AlertState(TypedDict):
    """
    Shared LangGraph state.
    """

    machine_id: str

    alert_tier: str

    ensemble_score: float

    sensor_context: dict

    anomalous_features: List[str]

    ticket_created: bool

    ticket_id: Optional[str]

    diagnostic_report: Optional[str]

    dispatch_order: Optional[str]

    notification_sent: bool