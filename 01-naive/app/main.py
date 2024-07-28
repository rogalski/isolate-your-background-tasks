import asyncio
import uuid

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def index():
    """Hello world"""
    return {"Hello": "World"}


@app.get("/fast")
async def fast_operation():
    """Simulate fast API operation"""
    return {"operation": "fast"}


@app.get("/slow")
async def slow_operation():
    """Simulate slow API operation"""
    await asyncio.sleep(5.0)
    random_uuid = uuid.uuid4()
    return {"operation": "slow", "uuid": random_uuid}
