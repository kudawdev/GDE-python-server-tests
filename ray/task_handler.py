import os
import sys

import ray

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from test.config.config import Config

config_file_path = os.path.join(os.getcwd(), '../config/config.cfg')
config = Config(config_file_path)


@ray.remote
def handle_request(task_name):
    if task_name == "cpu":
        result = cpu_bound_task()
    elif task_name == "io":
        result = io_bound_task()
    elif task_name == "fib":
        result = fib()
    else:
        result = "Task no found"

    return str(result)


def cpu_bound_task():
    result = 0
    for i in range(10 ** 6):
        result += i
    return result


def fib():
    a, b = 0, 1
    for _ in range(config.task_setting_fibonacci_limit):
        a, b = b, a + b
    return a


def io_bound_task():
    content_to_write = 'a' * 10 ** 6
    with open(f'files/{config.task_setting_large_file_name}', 'w') as f:
        f.write(content_to_write)

    with open(f'files/{config.task_setting_large_file_name}', 'r') as f:
        content = f.read()
    # os.remove(LARGE_FILE)
    return len(content)
