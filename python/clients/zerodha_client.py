from __future__ import annotations

import threading
from typing import Callable

try:
    from kiteconnect import KiteTicker
except ImportError:  # pragma: no cover - optional dependency until installed
    KiteTicker = None  # type: ignore


class ZerodhaStream:
    def __init__(
        self,
        api_key: str,
        access_token: str,
        instruments: list[int],
        on_tick: Callable[[dict], None],
    ) -> None:
        if KiteTicker is None:
            raise RuntimeError("kiteconnect is not installed; install kiteconnect>=3.9.0")
        self._ticker = KiteTicker(api_key, access_token)
        self._on_tick = on_tick
        self._instruments = instruments
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        self._ticker.on_ticks = self._wrap_on_ticks
        self._ticker.on_connect = self._subscribe
        self._thread = threading.Thread(target=self._ticker.connect, kwargs={"threaded": True}, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if self._ticker is not None:
            self._ticker.close()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)

    def _subscribe(self, _: KiteTicker) -> None:
        self._ticker.subscribe(self._instruments)
        self._ticker.set_mode(self._instruments, KiteTicker.MODE_FULL)

    def _wrap_on_ticks(self, _: KiteTicker, ticks: list[dict]) -> None:
        for tick in ticks:
            self._on_tick(tick)

