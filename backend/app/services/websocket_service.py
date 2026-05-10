from collections import deque

import numpy as np
from fastapi import APIRouter, WebSocket
from loguru import logger

from app.services.inference_service import (
    InferenceService,
)

from app.services.simulator_service import (
    SensorSimulator,
)

router = APIRouter()

simulator = SensorSimulator(
    dataset_path=(
        "app/data/ai4i2020.csv"
    )
)

inference_service = (
    InferenceService()
)

sensor_buffer = deque(
    maxlen=50
)


@router.websocket(
    "/ws/sensor-stream"
)
async def sensor_stream(
    websocket: WebSocket,
):
    """
    Real-time predictive maintenance stream.
    """

    await websocket.accept()

    logger.info(
        "WebSocket client connected"
    )

    try:

        async for reading in (
            simulator.stream_readings()
        ):

            sensor_buffer.append([
                reading["air_temp"],
                reading["process_temp"],
                reading[
                    "rotational_speed"
                ],
                reading["torque"],
                reading["tool_wear"],
            ])

            if len(sensor_buffer) < 50:
                continue

            sensor_window = np.array(
                sensor_buffer
            ).reshape(1, 50, 5)

            latest_reading = np.array([
                sensor_buffer[-1]
            ])

            result = (
                inference_service
                .ensemble
                .analyze_machine_state(
                    sensor_reading=
                        latest_reading,

                    sensor_window=
                        sensor_window,
                )
            )

            payload = {
                "machine_id":
                    reading["machine_id"],

                "timestamp":
                    reading["timestamp"],

                "readings": {
                    "air_temp":
                        reading["air_temp"],

                    "process_temp":
                        reading[
                            "process_temp"
                        ],

                    "rotational_speed":
                        reading[
                            "rotational_speed"
                        ],

                    "torque":
                        reading["torque"],

                    "tool_wear":
                        reading[
                            "tool_wear"
                        ],
                },

                "alert_tier":
                    result["alert_tier"],

                "ensemble_score":
                    result[
                        "ensemble_score"
                    ],

                "anomalous_features":
                    result[
                        "anomalous_features"
                    ],
            }

            await websocket.send_json(
                payload
            )

    except Exception as error:

        logger.error(
            f"WebSocket error: {error}"
        )

    finally:

        await websocket.close()

        logger.info(
            "WebSocket client disconnected"
        )