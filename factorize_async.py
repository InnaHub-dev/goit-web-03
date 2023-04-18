import functools
import math
import time
from typing import Callable
from multiprocessing import Pool, cpu_count


def run_time_decorator(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args):
        start_time = time.time()
        result = func(*args)
        print(f"My function {func.__name__} took", time.time() - start_time, "to run")
        return result

    return wrapper


def factorize_number(number: int) -> list:
    factors = []
    for i in range(1, int(math.sqrt(number)) + 1):
        if number % i == 0:
            factors.append(i)
            if number // i != i:
                factors.append(number // i)
    return sorted(factors)


@run_time_decorator
def factorize(numbers: list) -> list[list]:
    lists = []
    for i in numbers:
        lists.append(factorize_number(i))
    return lists


@run_time_decorator
def factorize_async(task):
    with Pool(cpu_count()) as p:
        result = p.map(factorize_number, task)
        return result


if __name__ == "__main__":
    task = [
        128,
        255,
        99999,
        10651060,
        123456,
        12345678,
        234567,
        2345678,
        234567,
        234567,
        234567,
        23456789,
        45678,
        3456789,
        345678,
        3456789,
        45678,
        3456789,
        234567890,
        34567890,
        34567890,
        34567,
        128,
        255,
        99999,
        10651060,
        123456,
        12345678,
        234567,
        2345678,
        234567,
        234567,
        234567,
        23456789,
        45678,
        3456789,
        345678,
        3456789,
        45678,
        3456789,
        234567890,
        34567890,
        34567890,
        34567,
        99999,
        10651060,
        123456,
        12345678,
        234567,
        2345678,
        234567,
        234567,
        234567,
        23456789,
        45678,
        3456789,
        345678,
        3456789,
        45678,
        3456789,
        234567890,
        34567890,
        34567890,
        34567,
        128,
        255,
        99999,
        10651060,
        123456,
        3456789,
        345678,
        3456789,
        45678,
        3456789,
        234567890,
        34567890,
        34567890,
        34567,
        128,
        255,
        99999,
        10651060,
        123456,
        12345678,
        234567,
        2345678,
        234567,
        234567,
        234567,
        23456789,
        45678,
        3456789,
        345678,
        3456789,
        45678,
        3456789,
        234567890,
        34567890,
        34567890,
        34567,
        99999,
        10651060,
        123456,
        12345678,
        234567,
        2345678,
        234567,
        234567,
        234567,
        23456789,
        45678,
        3456789,
        345678,
        3456789,
        45678,
        3456789,
        234567890,
        34567890,
        34567890,
        34567,
        128,
        255,
        99999,
        10651060,
        123456,
        3456789,
        345678,
        3456789,
        45678,
        3456789,
        234567890,
        34567890,
        34567890,
        34567,
        128,
        255,
        99999,
        10651060,
        123456,
        12345678,
        234567,
        2345678,
        234567,
        234567,
        234567,
        23456789,
        45678,
        3456789,
        345678,
        3456789,
        45678,
        3456789,
        234567890,
        34567890,
        34567890,
        34567,
        99999,
        10651060,
        123456,
        12345678,
        234567,
        2345678,
        234567,
        234567,
        234567,
        23456789,
        45678,
        3456789,
        345678,
        3456789,
        45678,
        3456789,
        234567890,
        34567890,
        34567890,
        34567,
        128,
        255,
        99999,
        10651060,
        123456,
        3456789,
        345678,
        3456789,
        45678,
        3456789,
        234567890,
        34567890,
        34567890,
        34567,
        128,
        255,
        99999,
        10651060,
        123456,
        12345678,
        234567,
        2345678,
        234567,
        234567,
        234567,
        23456789,
        45678,
        3456789,
        345678,
        3456789,
        45678,
        3456789,
        234567890,
        34567890,
        34567890,
        34567,
        99999,
        10651060,
        123456,
        12345678,
        234567,
        2345678,
        234567,
        234567,
        234567,
        23456789,
        45678,
        3456789,
        345678,
        3456789,
        45678,
        3456789,
        234567890,
        34567890,
        34567890,
        34567,
        128,
        255,
        99999,
        10651060,
        123456456789034567,
        23456789045678,
        234567893456789,
        3456789345678,
        345678934567,
        34567893456789456,
        345678345678456,
        23456,
        4567,
        45678,
    ]
    a = factorize(task)
    print(len(a))
    b = factorize_async(task)
    print(len(b))

# Results:
# My function factorize took 23.659733057022095 to run
# My function factorize_async took 14.631557941436768 to run
