import numpy as np

from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.metrics import AUC
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.optimizers import Adam

from loguru import logger


class PredictiveLSTM:
    def __init__(
        self,
        input_shape=(50, 5),
    ):
        self.input_shape = input_shape
        self.model = self._build_model()

    def _build_model(self) -> Sequential:

        model = Sequential([
            LSTM(
                64,
                return_sequences=True,
                input_shape=self.input_shape,
            ),

            Dropout(0.2),

            LSTM(
                32,
                return_sequences=False,
            ),

            Dropout(0.2),

            Dense(
                16,
                activation="relu",
            ),

            Dense(
                1,
                activation="sigmoid",
            ),
        ])

        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss="binary_crossentropy",
            metrics=[
                AUC(name="auc"),
            ],
        )

        logger.info("LSTM model compiled successfully")

        return model

    def train(
        self,
        X_train,
        y_train,
        X_val,
        y_val,
        epochs: int = 50,
        batch_size: int = 32,
    ):

        logger.info("Starting LSTM training")

        early_stopping = EarlyStopping(
            monitor="val_auc",
            patience=10,
            mode="max",
            restore_best_weights=True,
        )

        class_weights = {
            0: 1,
            1: 30,
        }

        history = self.model.fit(
            X_train,
            y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            class_weight=class_weights,
            callbacks=[early_stopping],
            verbose=1,
        )

        logger.info("LSTM training completed")

        return history

    def evaluate(
        self,
        X_test,
        y_test,
    ):

        logger.info("Evaluating LSTM model")

        results = self.model.evaluate(
            X_test,
            y_test,
            verbose=0,
        )

        metrics = dict(
            zip(
                self.model.metrics_names,
                results,
            )
        )

        logger.info(f"Evaluation metrics: {metrics}")

        return metrics

    def predict_probability(
        self,
        window: np.ndarray,
    ) -> float:

        prediction = self.model.predict(
            window,
            verbose=0,
        )[0][0]

        return float(prediction)

    def predict_batch(
        self,
        X_batch,
    ) -> np.ndarray:

        predictions = self.model.predict(
            X_batch,
            verbose=0,
        )

        return predictions.flatten()

    def save_model(
        self,
        file_path: str,
    ):

        self.model.save(file_path)

        logger.info(f"LSTM model saved to {file_path}")

    def load_existing_model(
        self,
        file_path: str,
    ):

        self.model = load_model(file_path)

        logger.info(f"LSTM model loaded from {file_path}")
        
    @classmethod
    def load_model(
        cls,
        model_path: str,
    ):
        """
        Load trained LSTM model.
        """

        from tensorflow.keras.models import (
            load_model,
        )

        logger.info(
            f"Loading LSTM model from "
            f"{model_path}"
        )

        instance = cls.__new__(cls)

        instance.model = load_model(
            model_path
        )

        logger.info(
            "LSTM model loaded successfully"
        )

        return instance