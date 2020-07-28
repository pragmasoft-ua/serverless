import random
import numpy as np

def submit(state: dict) -> list:
    """
    submits mapreduce job
    """
    state = state if state is not None else {}
    size = state.get('size', 1000)
    partitions = state.get('partitions', 100)
    seed = state.get('seed', None)
    if seed is not None:
        np.random.seed(seed)
    arr = np.random.randint(0,size,size)
    arr = np.reshape(arr, (partitions, -1))
    # must convert to list, because numpy arrays are not json serializable
    return  arr.tolist()

def step(items: list) -> int:
    return sum(items)

def calculate(**kwargs) -> int:
    items = submit(kwargs)
    items = [step(i) for i in items]
    result = step(items)
    return result
