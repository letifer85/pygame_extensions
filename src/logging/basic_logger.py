from __future__ import annotations

import sys

import loguru

basic_logger = loguru.logger
basic_logger.configure(
    handlers=[
        {
            'sink': sys.stdout,
            'format': '<level>{level}</level> {time:HH:mm:ss:SSSS}: <yellow>{message}</yellow>',  # noqa
        }
    ]
)
