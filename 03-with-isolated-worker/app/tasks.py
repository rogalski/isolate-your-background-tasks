import logging
import math
import random
import sys

logger = logging.getLogger()

TASKS_REDIS_LIST = "background_tasks"


def slow_operation_task(lower: int, upper: int) -> int:
    sys.set_int_max_str_digits(1 << 24)
    _ = math.factorial(500000)
    return random.randint(lower, upper)


TASK_REGISTRY = {f.__name__: f for f in [slow_operation_task]}
