from app.common.context import Context
from app.services import database
from app.services import redis
from fastapi import Request
from shared_modules import http_client


class RequestContext(Context):
    def __init__(self, request: Request) -> None:
        self.request = request

    @property
    def db(self) -> database.ServiceDatabase:
        return self.request.state.db

    @property
    def redis(self) -> redis.ServiceRedis:
        return self.request.state.redis

    @property
    def http_client(self) -> http_client.ServiceHTTPClient:
        return self.request.state.http_client
