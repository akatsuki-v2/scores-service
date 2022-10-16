from __future__ import annotations

from enum import Enum


class ServiceError(str, Enum):
    SCORES_CANNOT_CREATE = "scores.cannot_create"
    SCORES_CANNOT_UPDATE = "scores.cannot_update"
    SCORES_CANNOT_DELETE = "scores.cannot_delete"
    SCORES_NOT_FOUND = "scores.not_found"
