from typing import Tuple

import joblib
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler


FEATURE_COLUMNS = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
]


TARGET_COLUMN = "Machine failure"


class TimeSeriesPreprocessor:
    def __init__(self, window_size: int = 50):
        self.window_size = window_size
        self.scaler = StandardScaler()

    def load_dataset(self, file_path: str) -> pd.DataFrame:
        df = pd.read_csv(file_path)

        return df

    def temporal_train_val_test_split(
        self,
        df: pd.DataFrame,
        train_ratio: float = 0.7,
        val_ratio: float = 0.15,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

        total_size = len(df)

        train_end = int(total_size * train_ratio)
        val_end = int(total_size * (train_ratio + val_ratio))

        train_df = df.iloc[:train_end]
        val_df = df.iloc[train_end:val_end]
        test_df = df.iloc[val_end:]

        return train_df, val_df, test_df

    def fit_scaler(self, train_df: pd.DataFrame):
        self.scaler.fit(train_df[FEATURE_COLUMNS])

    def transform_features(
        self,
        df: pd.DataFrame,
    ) -> np.ndarray:

        return self.scaler.transform(df[FEATURE_COLUMNS])

    def create_sliding_windows(
        self,
        features: np.ndarray,
        labels: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray]:

        X = []
        y = []

        for i in range(len(features) - self.window_size):

            X_window = features[i:i + self.window_size]

            y_target = labels[i + self.window_size]

            X.append(X_window)
            y.append(y_target)

        return np.array(X), np.array(y)

    def preprocess_training_data(
        self,
        df: pd.DataFrame,
    ):

        train_df, val_df, test_df = (
            self.temporal_train_val_test_split(df)
        )

        self.fit_scaler(train_df)

        train_features = self.transform_features(train_df)
        val_features = self.transform_features(val_df)
        test_features = self.transform_features(test_df)

        train_labels = train_df[TARGET_COLUMN].values
        val_labels = val_df[TARGET_COLUMN].values
        test_labels = test_df[TARGET_COLUMN].values

        X_train, y_train = self.create_sliding_windows(
            train_features,
            train_labels,
        )

        X_val, y_val = self.create_sliding_windows(
            val_features,
            val_labels,
        )

        X_test, y_test = self.create_sliding_windows(
            test_features,
            test_labels,
        )

        return (
            X_train,
            y_train,
            X_val,
            y_val,
            X_test,
            y_test,
        )

    def preprocess_inference_window(
        self,
        readings: list,
    ) -> np.ndarray:

        df = pd.DataFrame(readings)

        feature_mapping = {
            "air_temp": "Air temperature [K]",
            "process_temp": "Process temperature [K]",
            "rotational_speed": "Rotational speed [rpm]",
            "torque": "Torque [Nm]",
            "tool_wear": "Tool wear [min]",
        }

        df.rename(columns=feature_mapping, inplace=True)

        scaled_features = self.scaler.transform(
            df[FEATURE_COLUMNS]
        )

        return np.expand_dims(scaled_features, axis=0)

    def save_scaler(
        self,
        file_path: str,
    ):
        joblib.dump(self.scaler, file_path)

    def load_scaler(
        self,
        file_path: str,
    ):
        self.scaler = joblib.load(file_path)