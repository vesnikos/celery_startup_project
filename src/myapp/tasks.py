from .capp import capp
import random


@capp.task
def my_super_task(x, y):
    return x + y


@capp.task(bind=True)
def long_running_task(self) -> float:
    n = 100000
    total = 0
    for i in range(0, n):
        total += random.randint(1, 1000)
    return total / n
