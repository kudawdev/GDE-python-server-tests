
def cpu_bound_task():
    result = 0
    for i in range(10 ** 6):
        result += i
    return result


def fib(size):
    a, b = 0, 1
    for _ in range(size):
        a, b = b, a + b
    return a


def io_bound_task(filename):
    content_to_write = 'a' * 10 ** 6
    with open(f'files/{filename}', 'w') as f:
        f.write(content_to_write)

    with open(f'files/{filename}', 'r') as f:
        content = f.read()

    # os.remove(LARGE_FILE)

    return len(content)