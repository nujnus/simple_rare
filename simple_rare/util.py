def partition(ls, size):
    return [ls[i:i + size] for i in range(0, len(ls), size)]

