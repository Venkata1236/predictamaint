import pandas as pd
import numpy as np

from loguru import logger

from app.core.config import settings

from app.ml.preprocessor import (
    TimeSeriesPreprocessor,
)

from app.ml.lstm_model import (
    PredictiveLSTM,
)

from app.ml.isolation_forest import (
    IsolationForestDetector,
)

from app.ml.ensemble import (
    PredictiveMaintenanceEnsemble,
)


class PredictiveMaintenanceInference:
    def __init__(self):

        logger.info(
            "Initializing PredictiveMaintenanceInference"
        )

        self.preprocessor = (
            TimeSeriesPreprocessor()
        )

        self.preprocessor.load_scaler(
            settings.SCALER_PATH
        )

        self.lstm_model = (
            PredictiveLSTM()
        )

        self.lstm_model.load_existing_model(
            settings.LSTM_MODEL_PATH
        )

        self.isolation_detector = (
            IsolationForestDetector()
        )

        self.isolation_detector.load_model(
            settings.ISOLATION_FOREST_PATH,
            "saved_models/if_scaler.pkl",
        )

        self.ensemble = (
            PredictiveMaintenanceEnsemble(
                lstm_model=self.lstm_model,
                isolation_detector=self.isolation_detector,
            )
        )

        logger.info(
            "Inference pipeline initialized successfully"
        )

    def calculate_baseline_means(
        self,
        dataset_path: str,
    ):

        df = pd.read_csv(dataset_path)

        return {
            "air_temp":
                df["Air temperature [K]"].mean(),

            "process_temp":
                df["Process temperature [K]"].mean(),

            "rotational_speed":
                df["Rotational speed [rpm]"].mean(),

            "torque":
                df["Torque [Nm]"].mean(),

            "tool_wear":
                df["Tool wear [min]"].mean(),
        }

    def prepare_latest_sensor_array(
        self,
        latest_reading: dict,
    ):

        return np.array([
            [
                latest_reading["air_temp"],
                latest_reading["process_temp"],
                latest_reading["rotational_speed"],
                latest_reading["torque"],
                latest_reading["tool_wear"],
            ]
        ])

    def run_inference(
        self,
        readings: list,
        dataset_path: str,
    ):

        logger.info(
            "Running production inference pipeline"
        )

        window_data = (
            self.preprocessor.preprocess_inference_window(
                readings
            )
        )

        latest_reading = readings[-1]

        latest_sensor_array = (
            self.prepare_latest_sensor_array(
                latest_reading
            )
        )

        baseline_means = (
            self.calculate_baseline_means(
                dataset_path
            )
        )

        result = (
            self.ensemble.analyze_machine_state(
                window_data=window_data,
                latest_sensor_array=latest_sensor_array,
                latest_sensor_dict=latest_reading,
                baseline_means=baseline_means,
            )
        )

        logger.info(
            "Inference completed successfully"
        )

        return result