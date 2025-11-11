from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class ParityEvent:
    timestamp_ns: int
    instrument: str
    buy_venue: str
    sell_venue: str
    bid_price: float
    ask_price: float
    spread: float


class AlertSink(Protocol):
    def publish(self, event: ParityEvent) -> None:
        ...


class StdoutSink:
    def publish(self, event: ParityEvent) -> None:
        print(
            "[ALERT]",
            event.instrument,
            event.buy_venue,
            event.sell_venue,
            event.spread,
        )


class AlertRouter:
    def __init__(self) -> None:
        self._sinks: list[AlertSink] = []

    def register(self, sink: AlertSink) -> None:
        self._sinks.append(sink)

    def emit(self, event: ParityEvent) -> None:
        for sink in self._sinks:
            sink.publish(event)

