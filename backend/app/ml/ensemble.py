from typing import Dict, List

import joblib
import numpy as np
from loguru import logger

from app.ml.lstm_model import (
    PredictiveLSTM,
)


class PredictiveMaintenanceEnsemble:
    """
    Ensemble engine combining:
    - LSTM failure prediction
    - Isolation Forest anomaly detection
    """

    def __init__(
        self,
        lstm_model_path: str,
        scaler_path: str,
        isolation_model_path: str,
        isolation_scaler_path: str,
    ):
        logger.info(
            "Initializing ensemble engine"
        )

        self.lstm_model = (
            PredictiveLSTM.load_model(
                lstm_model_path
            )
        )

        self.scaler = joblib.load(
            scaler_path
        )

        self.isolation_forest = (
            joblib.load(
                isolation_model_path
            )
        )

        self.isolation_scaler = (
            joblib.load(
                isolation_scaler_path
            )
        )

    def _calculate_isolation_score(
        self,
        sensor_reading: np.ndarray,
    ) -> float:
        """
        Calculate normalized anomaly score.
        """

        scaled_reading = (
            self.isolation_scaler
            .transform(sensor_reading)
        )

        raw_score = (
            self.isolation_forest
            .decision_function(
                scaled_reading
            )[0]
        )

        normalized_score = (
            1 / (1 + np.exp(raw_score))
        )

        return float(normalized_score)

    def _detect_anomalous_features(
        self,
        sensor_reading: np.ndarray,
    ) -> List[str]:
        """
        Detect suspicious features.
        """

        feature_names = [
            "air_temp",
            "process_temp",
            "rotational_speed",
            "torque",
            "tool_wear",
        ]

        anomalous_features = []

        values = sensor_reading[0]

        thresholds = {
            "air_temp": 320,
            "process_temp": 330,
            "rotational_speed": 3000,
            "torque": 150,
            "tool_wear": 200,
        }

        for idx, feature in enumerate(
            feature_names
        ):
            if (
                values[idx]
                > thresholds[feature]
            ):
                anomalous_features.append(
                    feature
                )

        return anomalous_features

    def analyze_machine_state(
        self,
        sensor_reading: np.ndarray,
        sensor_window: np.ndarray,
    ) -> Dict:
        """
        Analyze machine state using ensemble.
        """

        logger.info(
            "Running ensemble analysis"
        )

        scaled_window = (
            self.scaler.transform(
                sensor_window.reshape(-1, 5)
            ).reshape(1, 50, 5)
        )

        lstm_probability = (
            self.lstm_model.predict(
                scaled_window
            )
        )

        isolation_score = (
            self._calculate_isolation_score(
                sensor_reading
            )
        )

        ensemble_score = (
            0.7 * lstm_probability
            + 0.3 * isolation_score
        )

        if ensemble_score < 0.45:
            alert_tier = "NORMAL"

        elif ensemble_score < 0.75:
            alert_tier = "ANOMALY"

        else:
            alert_tier = "CRITICAL"

        anomalous_features = (
            self._detect_anomalous_features(
                sensor_reading
            )
        )

        if alert_tier == "NORMAL":

            recommended_action = (
                "Machine operating normally. "
                "Continue routine monitoring."
            )

        elif alert_tier == "ANOMALY":

            feature_text = (
                ", ".join(anomalous_features)
                if anomalous_features
                else "sensor drift patterns"
            )

            recommended_action = (
                "Anomaly detected. "
                f"Inspect features: "
                f"{feature_text}. "
                "Create maintenance ticket."
            )

        else:

            recommended_action = (
                "CRITICAL condition detected. "
                "Immediate shutdown recommended. "
                "Dispatch maintenance team."
            )

        result = {
            "alert_tier": alert_tier,
            "ensemble_score": float(
                ensemble_score
            ),
            "lstm_failure_probability":
                float(lstm_probability),

            "isolation_forest_score":
                float(isolation_score),

            "anomalous_features":
                anomalous_features,

            "recommended_action":
                recommended_action,
        }

        logger.info(
            f"Ensemble analysis completed: "
            f"{alert_tier}"
        )

        return result