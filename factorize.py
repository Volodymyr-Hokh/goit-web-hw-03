from datetime import datetime
from functools import wraps
from multiprocessing import Process, Queue


def measure_speed(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start = datetime.now()
        res = func(*args, **kwargs)
        finish = datetime.now()
        exec_time = finish - start
        print(f"Function {func.__name__} executed in {exec_time}")
        return res
    return inner


@measure_speed
def factorize_single_process(*numbers):
    result = []
    for number in numbers:
        res = []
        result.append(res)
        for i in range(1, number + 1):
            if number % i == 0:
                res.append(i)
    return result


@measure_speed
def factorize_multi_process(queue: Queue, *numbers):
    result = []
    for number in numbers:
        res = []
        result.append(res)
        for i in range(1, number + 1):
            if number % i == 0:
                res.append(i)
    queue.put(res)
    return result


def create_queue(*numbers):
    processes = []
    queue = Queue()

    for number in numbers:
        process = Process(target=factorize_multi_process, args=(queue, number))
        processes.append(process)
        process.start()

    results = []

    for process in processes:
        process.join()

    while not queue.empty():
        results.append(queue.get())
    return results


def test_func(func):
    a, b, c, d = func(128, 255, 99999, 10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]


if __name__ == "__main__":
    test_func(create_queue)
    test_func(factorize_single_process)
