import contextlib
import time
from dataclasses import dataclass, field
from typing import Any, Iterator

JsonType = dict[str, Any]


def url_join(*urls: str):
    return "/".join([url.strip("/") for url in urls])


@dataclass
class TimeCounter:
    _start: float = field(default_factory=time.time)
    _end: float | None = None

    @classmethod
    @contextlib.contextmanager
    def start(cls) -> Iterator["TimeCounter"]:
        time_counter = TimeCounter()
        yield time_counter
        time_counter._end = time.time()

    def milliseconds_passed(self) -> float:
        return 1000 * ((self._end or time.time()) - self._start)
