from typing import Any
from typing import Mapping

from app.common import settings
from app.common.context import Context


class ScoresRepo:
    READ_PARAMS = """\
        score_id, beatmap_id, account_id, mode, mods, score, performance,
        accuracy, max_combo, count_50s, count_100s, count_300s, count_gekis,
        count_katus, count_misses, grade, passed, perfect, seconds_elapsed,
        anticheat_flags, client_checksum, status, created_at, updated_at
    """

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def submit(self, beatmap_id: int, account_id: int, mode: str,
                     mods: int, score: int, performance: float, accuracy: float,
                     max_combo: int, count_50s: int, count_100s: int,
                     count_300s: int, count_gekis: int, count_katus: int,
                     count_misses: int, grade: str, passed: bool, perfect: bool,
                     seconds_elapsed: int, anticheat_flags: int,
                     client_checksum: str, status: str,
                     ) -> Mapping[str, Any] | None:
        query = """\
            INSERT INTO scores (
                beatmap_id, account_id, mode, mods, score, performance,
                accuracy, max_combo, count_50s, count_100s, count_300s,
                count_gekis, count_katus, count_misses, grade, passed, perfect,
                seconds_elapsed, anticheat_flags, client_checksum, status
            ) VALUES (
                :beatmap_id, :account_id, :mode, :mods, :score, :performance,
                :accuracy, :max_combo, :count_50s, :count_100s, :count_300s,
                :count_gekis, :count_katus, :count_misses, :grade, :passed,
                :perfect, :seconds_elapsed, :anticheat_flags, :client_checksum,
                :status
            )
        """
        params = {
            "beatmap_id": beatmap_id,
            "account_id": account_id,
            "mode": mode,
            "mods": mods,
            "score": score,
            "performance": performance,
            "accuracy": accuracy,
            "max_combo": max_combo,
            "count_50s": count_50s,
            "count_100s": count_100s,
            "count_300s": count_300s,
            "count_gekis": count_gekis,
            "count_katus": count_katus,
            "count_misses": count_misses,
            "grade": grade,
            "passed": passed,
            "perfect": perfect,
            "seconds_elapsed": seconds_elapsed,
            "anticheat_flags": anticheat_flags,
            "client_checksum": client_checksum,
            "status": status,
        }
        score_id = await self.ctx.db.execute(query, params)

        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM scores
             WHERE score_id = :score_id
        """
        params = {"score_id": score_id}
        _score = await self.ctx.db.fetch_one(query, params)
        return _score

    async def fetch_one(self, score_id: int) -> Mapping[str, Any] | None:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM scores
             WHERE score_id = :score_id
        """
        params = {"score_id": score_id}
        score = await self.ctx.db.fetch_one(query, params)
        return score

    async def fetch_many(self, beatmap_id: int | None = None,
                         mode: str | None = None,
                         mods: int | None = None,
                         passed: bool | None = None,
                         perfect: bool | None = None,
                         status: str | None = None,
                         page: int = 1,
                         page_size: int = settings.DEFAULT_PAGE_SIZE,
                         ) -> list[Mapping[str, Any]]:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM scores
             WHERE beatmap_id = COALESCE(:beatmap_id, beatmap_id)
               AND mode = COALESCE(:mode, mode)
               AND mods = COALESCE(:mods, mods)
               AND passed = COALESCE(:passed, passed)
               AND perfect = COALESCE(:perfect, perfect)
               AND status = COALESCE(:status, status)
             LIMIT :limit
            OFFSET :offset
        """
        params = {
            "beatmap_id": beatmap_id,
            "mode": mode,
            "mods": mods,
            "passed": passed,
            "perfect": perfect,
            "status": status,
            "limit": page_size,
            "offset": (page - 1) * page_size,
        }
        scores = await self.ctx.db.fetch_all(query, params)
        return scores

    # TODO: fetch_count for pagination metadata?

    async def partial_update(self, score_id: int, **kwargs: Any
                             ) -> Mapping[str, Any] | None:
        # TODO: use null coalescence to update fields
        query = f"""\
            UPDATE scores
               SET {", ".join(f"{k} = :{k}" for k in kwargs)}
             WHERE score_id = :score_id
        """
        params = {"score_id": score_id, **kwargs}
        await self.ctx.db.execute(query, params)

        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM scores
             WHERE score_id = :score_id
        """
        params = {"score_id": score_id}
        score = await self.ctx.db.fetch_one(query, params)
        return score

    async def delete(self, score_id: int) -> Mapping[str, Any] | None:
        query = """\
            UPDATE scores
               SET status = 'deleted',
                   updated_at = NOW()
            WHERE score_id = :score_id
        """
        params = {"score_id": score_id}
        await self.ctx.db.execute(query, params)

        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM scores
             WHERE score_id = :score_id
        """
        params = {"score_id": score_id}
        score = await self.ctx.db.fetch_one(query, params)
        return score
