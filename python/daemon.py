from __future__ import annotations

from dataclasses import asdict
import json
import subprocess
import sys
import time
from typing import Any

from alerting import AlertRouter, ParityEvent, StdoutSink
from config import Settings, load_settings


class ParityDaemon:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.alert_router = AlertRouter()
        self.alert_router.register(StdoutSink())
        self._cpp_process: subprocess.Popen[str] | None = None

    def start_cpp_backend(self) -> None:
        if self._cpp_process and self._cpp_process.poll() is None:
            return
        self._cpp_process = subprocess.Popen(
            ["./parity_daemon"],
            cwd=str(self._cpp_binary_dir()),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

    def _cpp_binary_dir(self) -> str:
        return str((self.settings.logging_path.parent / "build" / "cpp"))

    def monitor_cpp_backend(self) -> None:
        if not self._cpp_process or not self._cpp_process.stdout:
            return
        for line in self._cpp_process.stdout:
            if line.startswith("Parity violation:"):
                event = self._parse_violation(line)
                if event:
                    self.alert_router.emit(event)

    def _parse_violation(self, line: str) -> ParityEvent | None:
        parts = line.strip().split()
        if len(parts) < 11:
            return None
        try:
            return ParityEvent(
                timestamp_ns=int(time.time_ns()),
                instrument=parts[2],
                buy_venue=parts[4],
                sell_venue=parts[8],
                bid_price=float(parts[6]),
                ask_price=float(parts[10]),
                spread=float(parts[-1]),
            )
        except ValueError:
            return None

    def run(self) -> None:
        self.start_cpp_backend()
        while True:
            self.monitor_cpp_backend()
            time.sleep(0.1)

    def shutdown(self) -> None:
        if self._cpp_process and self._cpp_process.poll() is None:
            self._cpp_process.terminate()


def main() -> None:
    settings = load_settings()
    daemon = ParityDaemon(settings)
    try:
        daemon.run()
    except KeyboardInterrupt:
        daemon.shutdown()
    finally:
        payload: dict[str, Any] = asdict(settings)
        print(json.dumps({"status": "stopped", "settings": payload}))


if __name__ == "__main__":
    sys.exit(main())

