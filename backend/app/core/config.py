from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "PredictaMaint"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    API_V1_STR: str = "/api/v1"

    OPENAI_API_KEY: str

    DATABASE_URL: str

    LANGCHAIN_API_KEY: str
    LANGCHAIN_TRACING_V2: bool = True
    LANGCHAIN_PROJECT: str = "predictamaint"

    LSTM_MODEL_PATH: str
    ISOLATION_FOREST_PATH: str
    SCALER_PATH: str

    WEBSOCKET_INTERVAL_SECONDS: int = 2

    ALERT_NORMAL_THRESHOLD: float = 0.3
    ALERT_CRITICAL_THRESHOLD: float = 0.7

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()