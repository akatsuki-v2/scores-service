from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from app.services import database
from app.services import redis
from shared_modules import http_client


class Context(ABC):
    @property
    @abstractmethod
    def db(self) -> database.ServiceDatabase:
        ...

    @property
    @abstractmethod
    def redis(self) -> redis.ServiceRedis:
        ...

    @property
    @abstractmethod
    def http_client(self) -> http_client.ServiceHTTPClient:
        ...
