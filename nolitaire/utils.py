import random

def take_choices(items, k):
    taken_indexes = random.sample(range(len(items)), k=k)
    taken = [item for i, item in enumerate(items) if i in taken_indexes]
    kept = [item for i, item in enumerate(items) if i not in taken_indexes]
    return taken, kept
