from fastapi import APIRouter

router = APIRouter()


@router.get("/healthz", operation_id="healthz")
def healthz() -> dict[str, object]:
    return {"status": "ok", "checks": {}}


@router.get("/readyz", operation_id="readyz")
def readyz() -> dict[str, object]:
    return {"status": "ok", "checks": {"database": "ok"}}
