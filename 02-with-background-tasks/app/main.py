import logging
import math
import sys
import uuid

from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)


def slow_operation_task():
    sys.set_int_max_str_digits(1 << 24)
    _ = math.factorial(500000)
    random_uuid = uuid.uuid4()
    logger.info("Background task completed: %s", random_uuid)


@app.get("/")
async def index():
    """Hello world"""
    return {"Hello": "World"}


@app.get("/fast")
async def fast_operation():
    """Simulate fast API operation"""
    return {"operation": "fast"}


@app.get("/slow")
async def slow_operation(background_tasks: BackgroundTasks):
    """Simulate slow API operation, but moved to background tasks."""

    # Simple in-memory queue is used for each uvicorn worker.
    background_tasks.add_task(slow_operation_task)
    return {"operation": "slow"}
