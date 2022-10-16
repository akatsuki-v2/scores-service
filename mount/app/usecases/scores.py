from typing import Any
from typing import Mapping

from app.common import settings
from app.common.context import Context
from app.common.errors import ServiceError
from app.repositories.scores import ScoresRepo


async def submit(ctx: Context, beatmap_id: int, account_id: int, mode: str,
                 mods: int, score: int, performance: float, accuracy: float,
                 max_combo: int, count_50s: int, count_100s: int,
                 count_300s: int, count_gekis: int, count_katus: int,
                 count_misses: int, grade: str, passed: bool, perfect: bool,
                 seconds_elapsed: int, anticheat_flags: int,
                 client_checksum: str, status: str
                 ) -> Mapping[str, Any] | ServiceError:
    repo = ScoresRepo(ctx)

    _score = await repo.submit(beatmap_id=beatmap_id,
                               account_id=account_id,
                               mode=mode,
                               mods=mods,
                               score=score,
                               performance=performance,
                               accuracy=accuracy,
                               max_combo=max_combo,
                               count_50s=count_50s,
                               count_100s=count_100s,
                               count_300s=count_300s,
                               count_gekis=count_gekis,
                               count_katus=count_katus,
                               count_misses=count_misses,
                               grade=grade,
                               passed=passed,
                               perfect=perfect,
                               seconds_elapsed=seconds_elapsed,
                               anticheat_flags=anticheat_flags,
                               client_checksum=client_checksum,
                               status=status)
    if _score is None:
        return ServiceError.SCORES_CANNOT_CREATE

    return _score


async def fetch_one(ctx: Context, score_id: int) -> Mapping[str, Any] | ServiceError:
    repo = ScoresRepo(ctx)

    score = await repo.fetch_one(score_id=score_id)

    if score is None:
        return ServiceError.SCORES_NOT_FOUND

    return score


async def fetch_many(ctx: Context, beatmap_id: int | None = None,
                     mode: str | None = None,
                     mods: int | None = None,
                     passed: bool | None = None,
                     perfect: bool | None = None,
                     status: str | None = None,
                     page: int = 1,
                     page_size: int = settings.DEFAULT_PAGE_SIZE,
                     ) -> list[Mapping[str, Any]] | ServiceError:
    repo = ScoresRepo(ctx)

    scores = await repo.fetch_many(beatmap_id=beatmap_id,
                                   mode=mode,
                                   mods=mods,
                                   passed=passed,
                                   perfect=perfect,
                                   status=status,
                                   page=page,
                                   page_size=page_size)

    return scores


# TODO
# async def partial_update(ctx: Context) -> Mapping[str, Any] | ServiceError:
#     repo = ScoresRepo(ctx)


async def delete(ctx: Context, score_id: int) -> Mapping[str, Any] | ServiceError:
    repo = ScoresRepo(ctx)

    score = await repo.delete(score_id=score_id)
    if score is None:
        return ServiceError.SCORES_NOT_FOUND

    return score
