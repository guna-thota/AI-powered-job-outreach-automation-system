"""Resilience utilities such as retry and rate limiting."""

from __future__ import annotations

import threading
import time
from collections import deque
from typing import Callable, TypeVar

T = TypeVar("T")


class RateLimiter:
    """Simple in-memory sliding-window rate limiter."""

    def __init__(self, max_calls: int, period_seconds: int = 60) -> None:
        self.max_calls = max_calls
        self.period_seconds = period_seconds
        self._calls = deque()
        self._lock = threading.Lock()

    def wait_for_slot(self) -> None:
        """Block until a new request slot is available."""
        while True:
            with self._lock:
                now = time.monotonic()
                while self._calls and now - self._calls[0] >= self.period_seconds:
                    self._calls.popleft()
                if len(self._calls) < self.max_calls:
                    self._calls.append(now)
                    return
                sleep_for = self.period_seconds - (now - self._calls[0])
            time.sleep(max(sleep_for, 0.05))


def retry(operation: Callable[[], T], max_attempts: int, backoff_seconds: float) -> T:
    """Retry an operation with linear backoff."""
    last_error = None
    for attempt in range(1, max_attempts + 1):
        try:
            return operation()
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt == max_attempts:
                break
            time.sleep(backoff_seconds * attempt)
    raise RuntimeError(f"Operation failed after {max_attempts} attempts") from last_error
