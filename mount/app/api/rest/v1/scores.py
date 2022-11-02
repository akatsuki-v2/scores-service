from typing import Literal

from app.api.rest.context import RequestContext
from app.common import responses
from app.common import settings
from app.common.errors import ServiceError
from app.common.responses import Success
from app.models import Status
from app.models.scores import Score
from app.models.scores import ScoreInput
from app.usecases import scores
from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()


@router.post("/v1/scores", response_model=Success[Score])
async def submit(args: ScoreInput, ctx: RequestContext = Depends()):
    data = await scores.submit(ctx, beatmap_md5=args.beatmap_md5,
                               account_id=args.account_id,
                               username=args.username, mode=args.mode,
                               mods=args.mods, score=args.score,
                               performance=0.0, accuracy=args.accuracy,
                               max_combo=args.max_combo, count_50s=args.count_50s,
                               count_100s=args.count_100s,
                               count_300s=args.count_300s,
                               count_gekis=args.count_gekis,
                               count_katus=args.count_katus,
                               count_misses=args.count_misses,
                               grade=args.grade, passed=args.passed,
                               perfect=args.perfect,
                               seconds_elapsed=args.seconds_elapsed,
                               anticheat_flags=args.anticheat_flags,
                               client_checksum=args.client_checksum,
                               status=Status.ACTIVE)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to create score")

    resp = Score.from_mapping(data)
    return responses.success(resp)


@router.get("/v1/scores/{score_id}", response_model=Success[Score])
async def fetch_one(score_id: int, ctx: RequestContext = Depends()):
    data = await scores.fetch_one(ctx, score_id=score_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to fetch score")

    resp = Score.from_mapping(data)
    return responses.success(resp)


@router.get("/v1/scores", response_model=Success[list[Score]])
async def fetch_many(beatmap_md5: str | None = None,
                     account_id: int | None = None,
                     mode: Literal['osu', 'taiko',
                                   'fruits', 'mania'] | None = None,
                     mods: int | None = None,
                     passed: bool | None = None,
                     perfect: bool | None = None,
                     status: str | None = None,
                     country: str | None = None,
                     page: int = 1,
                     page_size: int = settings.DEFAULT_PAGE_SIZE,
                     ctx: RequestContext = Depends()):
    data = await scores.fetch_many(ctx, beatmap_md5=beatmap_md5,
                                   account_id=account_id,
                                   mode=mode, mods=mods,
                                   passed=passed, perfect=perfect,
                                   status=status, country=country,
                                   page=page, page_size=page_size)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to fetch scores")

    resp = [Score.from_mapping(rec) for rec in data]
    return responses.success(resp)


# TODO: partial_update


@router.delete("/v1/scores/{score_id}", response_model=Success[Score])
async def delete(score_id: int, ctx: RequestContext = Depends()):
    data = await scores.delete(ctx, score_id=score_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to delete score")

    resp = Score.from_mapping(data)
    return responses.success(resp)
