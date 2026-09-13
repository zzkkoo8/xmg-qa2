from typing import Annotated

from fastapi import APIRouter, Depends

from xmg_qa2.api.deps import Principal, require_admin

router = APIRouter()


@router.get("/admin/ping", operation_id="adminPing")
def admin_ping(_: Annotated[Principal, Depends(require_admin)]) -> dict[str, bool]:
    return {"ok": True}
