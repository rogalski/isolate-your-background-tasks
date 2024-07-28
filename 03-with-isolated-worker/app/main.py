import json
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Callable, Never, ParamSpec

import redis.asyncio as redis
from fastapi import FastAPI
from starlette.requests import Request

from . import tasks



@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[Never]:
    # set up logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # set up connection pool
    pool = redis.ConnectionPool.from_url("redis://redis")
    _app.state.mq_pool = pool

    yield None


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index():
    """Hello world"""
    return {"Hello": "World"}


@app.get("/fast")
async def fast_operation():
    """Simulate fast API operation"""
    return {"operation": "fast"}


@app.get("/slow")
async def slow_operation(request: Request):
    """Simulate slow API operation, but moved to background tasks."""

    await submit_task(request, tasks.slow_operation_task, 10, 100)
    return {"operation": "slow"}

P = ParamSpec("P")


async def submit_task(
    request: Request, task: Callable[P, Any], *args: P.args, **kwargs: P.kwargs
) -> None:
    client = redis.Redis.from_pool(request.app.state.mq_pool)
    await client.lpush(
        tasks.TASKS_REDIS_LIST,
        json.dumps({"task": task.__name__, "args": args, "kwargs": kwargs}),
    )
