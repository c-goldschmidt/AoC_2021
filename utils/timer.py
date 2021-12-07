from time import time


class Timer:

    def __init__(self):
        self.start = time()

    def __enter__(self):
        self.start = time()

    def next(self, message):
        elapsed = time() - self.start
        self.start = time()
        print(f'{message}: {elapsed}s')

    def __exit__(self, *_):
        elapsed = time() - self.start
        print(f'Completed in {elapsed}s')
