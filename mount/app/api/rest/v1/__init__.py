from __future__ import annotations

from fastapi import APIRouter

from . import scores

router = APIRouter()

router.include_router(scores.router, tags=["scores"])
