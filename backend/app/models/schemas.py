from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class SensorReading(BaseModel):
    timestamp: datetime

    air_temp: float = Field(..., gt=0)
    process_temp: float = Field(..., gt=0)

    rotational_speed: float = Field(..., ge=0)
    torque: float = Field(..., ge=0)
    tool_wear: float = Field(..., ge=0)


class AnalysisRequest(BaseModel):
    machine_id: str = Field(..., min_length=3)

    readings: List[SensorReading] = Field(
        ...,
        min_length=50,
        description="Minimum 50 readings required for LSTM window"
    )


class AnalysisResponse(BaseModel):
    analysis_id: UUID = Field(default_factory=uuid4)

    machine_id: str

    alert_tier: str

    ensemble_score: float
    lstm_failure_probability: float
    isolation_forest_score: float

    anomalous_features: List[str]

    recommended_action: str

    processing_time_ms: float

    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str


class WebSocketSensorResponse(BaseModel):
    machine_id: str

    timestamp: datetime

    readings: SensorReading

    alert_tier: str

    ensemble_score: float

    anomalous_features: List[str]