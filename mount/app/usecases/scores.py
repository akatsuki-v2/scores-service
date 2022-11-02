from typing import Any
from typing import Mapping

from app.common import settings
from app.common.context import Context
from app.common.errors import ServiceError
from app.repositories.scores import ScoresRepo
from shared_modules.api.rest.v1.users import UsersClient


async def submit(ctx: Context, beatmap_md5: str, account_id: int, username: str,
                 mode: str, mods: int, score: int, performance: float,
                 accuracy: float, max_combo: int, count_50s: int,
                 count_100s: int, count_300s: int, count_gekis: int,
                 count_katus: int, count_misses: int, grade: str, passed: bool,
                 perfect: bool, seconds_elapsed: int, anticheat_flags: int,
                 client_checksum: str, status: str
                 ) -> Mapping[str, Any] | ServiceError:
    repo = ScoresRepo(ctx)

    _score = await repo.submit(beatmap_md5=beatmap_md5,
                               account_id=account_id,
                               username=username,
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


async def filter_by_country(ctx: Context, scores: list[Mapping[str, Any]], country: str) -> list[Mapping[str, Any]]:
    client = UsersClient(ctx.http_client)

    filtered_scores: list[Mapping[str, Any]] = []

    for score in scores:
        account = await client.get_account(score["account_id"])
        if account is None:
            continue

        if account.country == country:
            filtered_scores.append(score)

    return filtered_scores


async def fetch_many(ctx: Context, beatmap_md5: str | None = None,
                     account_id: int | None = None,
                     mode: str | None = None,
                     mods: int | None = None,
                     passed: bool | None = None,
                     perfect: bool | None = None,
                     status: str | None = None,
                     country: str | None = None,
                     page: int = 1,
                     page_size: int = settings.DEFAULT_PAGE_SIZE,
                     ) -> list[Mapping[str, Any]] | ServiceError:
    repo = ScoresRepo(ctx)

    scores = await repo.fetch_many(beatmap_md5=beatmap_md5,
                                   account_id=account_id,
                                   mode=mode,
                                   mods=mods,
                                   passed=passed,
                                   perfect=perfect,
                                   status=status,
                                   page=page,
                                   page_size=page_size)

    if country is not None:
        scores = await filter_by_country(ctx, scores, country)

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
