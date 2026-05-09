import time

from fastapi import APIRouter, HTTPException

from loguru import logger

from app.ml.inference import (
    PredictiveMaintenanceInference,
)

from app.models.schemas import (
    AnalysisRequest,
    AnalysisResponse,
)


router = APIRouter()

inference_engine = (
    PredictiveMaintenanceInference()
)


@router.post(
    "/analyze-batch",
    response_model=AnalysisResponse,
)
async def analyze_batch(
    request: AnalysisRequest,
):

    logger.info(
        f"Received analysis request for "
        f"machine_id={request.machine_id}"
    )

    start_time = time.time()

    try:

        readings = [
            reading.model_dump()
            for reading in request.readings
        ]

        inference_result = (
            inference_engine.run_inference(
                readings=readings,
                dataset_path="app/data/ai4i2020.csv",
            )
        )

        processing_time_ms = (
            time.time() - start_time
        ) * 1000

        response = AnalysisResponse(
            machine_id=request.machine_id,

            alert_tier=
                inference_result["alert_tier"],

            ensemble_score=
                inference_result["ensemble_score"],

            lstm_failure_probability=
                inference_result[
                    "lstm_failure_probability"
                ],

            isolation_forest_score=
                inference_result[
                    "isolation_forest_score"
                ],

            anomalous_features=
                inference_result[
                    "anomalous_features"
                ],

            recommended_action=
                inference_result[
                    "recommended_action"
                ],

            processing_time_ms=
                round(processing_time_ms, 2),
        )

        logger.info(
            f"Analysis completed for "
            f"machine_id={request.machine_id}"
        )

        return response

    except Exception as e:

        logger.exception(
            "Error during batch analysis"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )