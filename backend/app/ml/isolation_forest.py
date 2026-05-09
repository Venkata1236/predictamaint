import joblib
import numpy as np
import pandas as pd

from loguru import logger

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler

from app.ml.preprocessor import FEATURE_COLUMNS


class IsolationForestDetector:
    def __init__(
        self,
        contamination: float = 0.034,
        n_estimators: int = 100,
        random_state: int = 42,
    ):

        self.contamination = contamination

        self.model = IsolationForest(
            contamination=contamination,
            n_estimators=n_estimators,
            random_state=random_state,
        )

        self.score_scaler = MinMaxScaler()

    def train(
        self,
        df: pd.DataFrame,
    ):

        logger.info(
            "Training Isolation Forest on healthy samples only"
        )

        normal_df = df[
            df["Machine failure"] == 0
        ]

        X_normal = normal_df[
            FEATURE_COLUMNS
        ]

        self.model.fit(X_normal)

        raw_scores = self.model.decision_function(
            X_normal
        ).reshape(-1, 1)

        self.score_scaler.fit(raw_scores)

        logger.info(
            "Isolation Forest training completed"
        )

    def predict_raw_score(
        self,
        sensor_reading: np.ndarray,
    ) -> float:

        raw_score = self.model.decision_function(
            sensor_reading
        )[0]

        return float(raw_score)

    def predict_anomaly_score(
        self,
        sensor_reading: np.ndarray,
    ) -> float:

        raw_score = self.predict_raw_score(
            sensor_reading
        )

        normalized_score = self.score_scaler.transform(
            [[raw_score]]
        )[0][0]

        anomaly_score = 1 - normalized_score

        anomaly_score = np.clip(
            anomaly_score,
            0,
            1,
        )

        return float(anomaly_score)

    def detect_anomalous_features(
        self,
        sensor_reading: dict,
        baseline_means: dict,
        threshold: float = 0.15,
    ):

        anomalous_features = []

        for feature, value in sensor_reading.items():

            if feature not in baseline_means:
                continue

            baseline = baseline_means[feature]

            if baseline == 0:
                continue

            deviation_ratio = abs(
                value - baseline
            ) / baseline

            if deviation_ratio > threshold:
                anomalous_features.append(feature)

        return anomalous_features

    def save_model(
        self,
        model_path: str,
        scaler_path: str,
    ):

        joblib.dump(
            self.model,
            model_path,
        )

        joblib.dump(
            self.score_scaler,
            scaler_path,
        )

        logger.info(
            "Isolation Forest artifacts saved successfully"
        )

    def load_model(
        self,
        model_path: str,
        scaler_path: str,
    ):

        self.model = joblib.load(
            model_path
        )

        self.score_scaler = joblib.load(
            scaler_path
        )

        logger.info(
            "Isolation Forest artifacts loaded successfully"
        )