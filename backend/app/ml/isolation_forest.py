from typing import Optional

import joblib
import numpy as np
import pandas as pd
from loguru import logger
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


class IsolationForestDetector:
    """
    Isolation Forest anomaly detector.
    """

    FEATURES = [
        "Air temperature [K]",
        "Process temperature [K]",
        "Rotational speed [rpm]",
        "Torque [Nm]",
        "Tool wear [min]",
    ]

    def __init__(self):
        self.model: Optional[
            IsolationForest
        ] = None

        self.scaler = (
            StandardScaler()
        )

    def train(
        self,
        df: pd.DataFrame,
    ):
        """
        Train only on healthy samples.
        """

        logger.info(
            "Training Isolation Forest"
        )

        normal_df = df[
            df["Machine failure"] == 0
        ]

        X_train = normal_df[
            self.FEATURES
        ]

        X_scaled = (
            self.scaler.fit_transform(
                X_train
            )
        )

        self.model = IsolationForest(
            contamination=0.034,
            n_estimators=100,
            random_state=42,
        )

        self.model.fit(X_scaled)

        logger.info(
            "Isolation Forest training completed"
        )

    def predict_anomaly_score(
        self,
        sensor_reading: np.ndarray,
    ) -> float:
        """
        Predict anomaly probability.
        """

        scaled_reading = (
            self.scaler.transform(
                sensor_reading
            )
        )

        raw_score = (
            self.model
            .decision_function(
                scaled_reading
            )[0]
        )

        normalized_score = (
            1 / (1 + np.exp(raw_score))
        )

        return float(normalized_score)

    def save_model(
        self,
        model_path: str,
        scaler_path: str,
    ):
        """
        Save artifacts.
        """

        joblib.dump(
            self.model,
            model_path,
        )

        joblib.dump(
            self.scaler,
            scaler_path,
        )

        logger.info(
            "Isolation Forest artifacts saved"
        )