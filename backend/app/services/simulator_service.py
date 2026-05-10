import asyncio
from typing import AsyncGenerator, Dict

import pandas as pd
from loguru import logger


class SensorSimulator:
    """
    Replay AI4I dataset as live stream.
    """

    def __init__(
        self,
        dataset_path: str,
    ):
        logger.info(
            "Loading sensor simulation dataset"
        )

        self.df = pd.read_csv(
            dataset_path
        )

    async def stream_readings(
        self,
    ) -> AsyncGenerator[Dict, None]:
        """
        Stream sensor readings continuously.
        """

        logger.info(
            "Starting live sensor stream"
        )

        for _, row in (
            self.df.iterrows()
        ):

            payload = {
                "machine_id": "CNC_001",

                "timestamp":
                    pd.Timestamp.utcnow()
                    .isoformat(),

                "air_temp":
                    float(
                        row[
                            "Air temperature [K]"
                        ]
                    ),

                "process_temp":
                    float(
                        row[
                            "Process temperature [K]"
                        ]
                    ),

                "rotational_speed":
                    float(
                        row[
                            "Rotational speed [rpm]"
                        ]
                    ),

                "torque":
                    float(
                        row[
                            "Torque [Nm]"
                        ]
                    ),

                "tool_wear":
                    float(
                        row[
                            "Tool wear [min]"
                        ]
                    ),
            }

            yield payload

            await asyncio.sleep(2)