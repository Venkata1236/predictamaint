from fastapi import APIRouter
from loguru import logger

from app.models.schemas import (
    AnalysisRequest,
    AnalysisResponse,
)
from app.services.inference_service import (
    InferenceService,
)

router = APIRouter()

inference_service = (
    InferenceService()
)


@router.post(
    "/analyze-batch",
    response_model=AnalysisResponse,
)
async def analyze_batch(
    request: AnalysisRequest,
):
    """
    Analyze predictive maintenance sequence.
    """

    logger.info(
        f"Received analysis request "
        f"for machine: "
        f"{request.machine_id}"
    )

    response = (
        await inference_service
        .analyze_batch(request)
    )

    return response