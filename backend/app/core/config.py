from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    APP_NAME: str = "PredictaMaint API"

    API_V1_STR: str = "/api/v1"

    OPENAI_API_KEY: str = "demo"

    DATABASE_URL: str = (
        "sqlite:///./predictamaint.db"
    )

    LANGCHAIN_API_KEY: str = "demo"

    LSTM_MODEL_PATH: str = (
        "saved_models/lstm_model.h5"
    )

    ISOLATION_FOREST_PATH: str = (
        "saved_models/isolation_forest.pkl"
    )

    SCALER_PATH: str = (
        "saved_models/scaler.pkl"
    )

    model_config = (
        SettingsConfigDict(
            env_file=".env",
            extra="ignore",
        )
    )


settings = Settings()