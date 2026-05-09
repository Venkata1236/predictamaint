import numpy as np

from loguru import logger

from app.core.config import settings
from app.ml.isolation_forest import (
    IsolationForestDetector,
)
from app.ml.lstm_model import PredictiveLSTM


class PredictiveMaintenanceEnsemble:
    def __init__(
        self,
        lstm_model: PredictiveLSTM,
        isolation_detector: IsolationForestDetector,
    ):

        self.lstm_model = lstm_model

        self.isolation_detector = isolation_detector

    def calculate_ensemble_score(
        self,
        lstm_probability: float,
        isolation_score: float,
    ) -> float:

        ensemble_score = (
            0.7 * lstm_probability
        ) + (
            0.3 * isolation_score
        )

        ensemble_score = np.clip(
            ensemble_score,
            0,
            1,
        )

        return float(ensemble_score)

    def classify_alert_tier(
        self,
        ensemble_score: float,
    ) -> str:

        if (
            ensemble_score <
            settings.ALERT_NORMAL_THRESHOLD
        ):
            return "NORMAL"

        elif (
            ensemble_score <
            settings.ALERT_CRITICAL_THRESHOLD
        ):
            return "ANOMALY"

        return "CRITICAL"

    def generate_recommended_action(
        self,
        alert_tier: str,
        anomalous_features: list,
    ) -> str:

        if alert_tier == "NORMAL":

            return (
                "Machine operating normally. "
                "Continue routine monitoring."
            )

        if alert_tier == "ANOMALY":

            return (
                "Anomaly detected. "
                f"Inspect features: "
                f"{', '.join(anomalous_features)}. "
                "Create maintenance ticket."
            )

        return (
            "CRITICAL condition detected. "
            f"Immediate inspection required for: "
            f"{', '.join(anomalous_features)}. "
            "Dispatch maintenance team immediately."
        )

    def analyze_machine_state(
        self,
        window_data,
        latest_sensor_array,
        latest_sensor_dict,
        baseline_means,
    ):

        logger.info(
            "Running ensemble analysis"
        )

        lstm_probability = (
            self.lstm_model.predict_probability(
                window_data
            )
        )

        isolation_score = (
            self.isolation_detector.predict_anomaly_score(
                latest_sensor_array
            )
        )

        ensemble_score = (
            self.calculate_ensemble_score(
                lstm_probability,
                isolation_score,
            )
        )

        alert_tier = (
            self.classify_alert_tier(
                ensemble_score
            )
        )

        anomalous_features = (
            self.isolation_detector.detect_anomalous_features(
                latest_sensor_dict,
                baseline_means,
            )
        )

        recommended_action = (
            self.generate_recommended_action(
                alert_tier,
                anomalous_features,
            )
        )

        logger.info(
            f"Ensemble Score: {ensemble_score:.4f}"
        )

        logger.info(
            f"Alert Tier: {alert_tier}"
        )

        return {
            "alert_tier": alert_tier,
            "ensemble_score": ensemble_score,
            "lstm_failure_probability":
                lstm_probability,
            "isolation_forest_score":
                isolation_score,
            "anomalous_features":
                anomalous_features,
            "recommended_action":
                recommended_action,
        }