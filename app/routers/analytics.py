from fastapi import APIRouter
from app.schemas.analytics import TurnoverReasonOut, RadarDataOut, PredictionOut

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/turnover-reasons", response_model=list[TurnoverReasonOut])
def get_turnover_reasons():
    return [
        TurnoverReasonOut(name="Compensation", value=32, color="hsl(0, 84%, 50%)"),
        TurnoverReasonOut(name="Career Growth", value=28, color="hsl(25, 95%, 53%)"),
        TurnoverReasonOut(name="Management", value=18, color="hsl(38, 92%, 50%)"),
        TurnoverReasonOut(name="Work-Life Balance", value=12, color="hsl(217, 91%, 53%)"),
        TurnoverReasonOut(name="Culture", value=10, color="hsl(160, 84%, 39%)"),
    ]


@router.get("/org-health", response_model=list[RadarDataOut])
def get_org_health():
    return [
        RadarDataOut(factor="Compensation", current=65, benchmark=80),
        RadarDataOut(factor="Growth", current=55, benchmark=75),
        RadarDataOut(factor="Culture", current=78, benchmark=72),
        RadarDataOut(factor="Management", current=70, benchmark=74),
        RadarDataOut(factor="Benefits", current=82, benchmark=78),
        RadarDataOut(factor="Flexibility", current=60, benchmark=85),
    ]


@router.get("/predictions", response_model=list[PredictionOut])
def get_predictions():
    return [
        PredictionOut(segment="Engineering < 2yr", probability=34, count=12, trend="increasing"),
        PredictionOut(segment="Mid-level Managers", probability=28, count=8, trend="stable"),
        PredictionOut(segment="Remote Workers", probability=22, count=15, trend="decreasing"),
        PredictionOut(segment="Recent Promotions", probability=12, count=6, trend="stable"),
        PredictionOut(segment="Senior Leadership", probability=8, count=3, trend="decreasing"),
    ]
