import asyncio
import json
import logging

import app.tasks
import redis.asyncio as redis

log = logging.getLogger(__package__)


async def consumer() -> None:
    client = redis.Redis.from_url("redis://redis")
    log.info(f"Ping successful: {await client.ping()}")
    while True:
        _, msg = await client.brpop(app.tasks.TASKS_REDIS_LIST)
        log.debug(msg)
        msg_spec = json.loads(msg)
        if msg_spec["task"] not in app.tasks.TASK_REGISTRY:
            log.warning("Unknown task: %s", msg_spec["task"])
            continue
        func = app.tasks.TASK_REGISTRY[msg_spec["task"]]
        args = msg_spec["args"]
        kwargs = msg_spec["kwargs"]
        log.info("Execute %s %s %s", func, args, kwargs)
        try:
            retval = func(*args, **kwargs)
        except Exception:
            log.exception("Failed to execute %s %s %s", func, args, kwargs)
        else:
            log.info("Retval: %s", retval)


def main():
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(consumer())
    finally:
        loop.close()


if __name__ == "__main__":
    main()
