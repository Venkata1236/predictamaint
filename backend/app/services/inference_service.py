import uuid
from datetime import datetime
from time import perf_counter
from typing import Dict

import numpy as np
import pandas as pd
from loguru import logger

from app.ml.ensemble import (
    PredictiveMaintenanceEnsemble,
)
from app.models.schemas import (
    AnalysisRequest,
    AnalysisResponse,
)


class InferenceService:
    """
    Central inference orchestration service.
    """

    def __init__(self):
        logger.info(
            "Initializing inference service"
        )

        self.ensemble = (
            PredictiveMaintenanceEnsemble(
                lstm_model_path=(
                    "saved_models/lstm_model.h5"
                ),
                scaler_path=(
                    "saved_models/scaler.pkl"
                ),
                isolation_model_path=(
                    "saved_models/"
                    "isolation_forest.pkl"
                ),
                isolation_scaler_path=(
                    "saved_models/"
                    "if_scaler.pkl"
                ),
            )
        )

    async def analyze_batch(
        self,
        request: AnalysisRequest,
    ) -> AnalysisResponse:
        """
        Analyze sensor sequence.
        """

        start_time = perf_counter()

        logger.info(
            f"Analyzing machine: "
            f"{request.machine_id}"
        )

        readings_df = pd.DataFrame([
            {
                "Air temperature [K]":
                    reading.air_temp,

                "Process temperature [K]":
                    reading.process_temp,

                "Rotational speed [rpm]":
                    reading.rotational_speed,

                "Torque [Nm]":
                    reading.torque,

                "Tool wear [min]":
                    reading.tool_wear,
            }
            for reading in request.readings
        ])

        latest_reading = (
            readings_df.iloc[-1]
            .values
            .reshape(1, -1)
        )

        sequence_window = (
            readings_df.values
            .reshape(1, 50, 5)
        )

        result: Dict = (
            self.ensemble
            .analyze_machine_state(
                sensor_reading=latest_reading,
                sensor_window=sequence_window,
            )
        )

        processing_time = (
            perf_counter() - start_time
        ) * 1000

        response = AnalysisResponse(
            analysis_id=str(uuid.uuid4()),
            machine_id=request.machine_id,
            alert_tier=result[
                "alert_tier"
            ],
            ensemble_score=result[
                "ensemble_score"
            ],
            lstm_failure_probability=result[
                "lstm_failure_probability"
            ],
            isolation_forest_score=result[
                "isolation_forest_score"
            ],
            anomalous_features=result[
                "anomalous_features"
            ],
            recommended_action=result[
                "recommended_action"
            ],
            processing_time_ms=round(
                processing_time,
                2,
            ),
            timestamp=datetime.utcnow(),
        )

        logger.info(
            f"Inference completed for "
            f"{request.machine_id}"
        )

        return response