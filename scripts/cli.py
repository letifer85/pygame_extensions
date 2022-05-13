from __future__ import annotations

import time
from logging.basic_logger import basic_logger


def log_run(function):
    # decorator used for timing `function` run time
    def timed(*args, **kwargs):
        start = time.perf_counter()
        return_value = function(*args, **kwargs)
        elapsed = time.perf_counter() - start
        basic_logger.info(f'`{function.__name__}` executed in: {elapsed:.5f}s')
        return return_value

    return timed


def parse_args():
    ...


@log_run
def main() -> None:
    ...


if __name__ == '__main__':
    main()
