# Parity Arbitrage Monitor

Low-latency monitoring stack that detects parity violations between Zerodha instruments and secondary venues. C++ handles the microsecond-sensitive comparison. Python supervises the daemon, handles alert fan-out, and powers analytics.

## Layout

- `cpp/` – Core parity detection engine (CMake project).
- `python/` – Supervisor, alerting, and dashboards.
- `configs/` – Instrument + threshold configuration stubs.
- `scripts/` – Build and run helpers.

## Getting Started

1. **Build the C++ binary**
   ```bash
   ./scripts/build.sh
   ```
2. **Run the supervisor**
   ```bash
   ./scripts/run_daemon.sh
   ```

## Next Steps

- Implement Zerodha WebSocket feed inside `FeedHandler` or through `python/clients/zerodha_client.py` with `pybind11` bindings.
- Replace console logging with shared-memory alert fan-out and Prometheus exporters.
- Fill out `configs/` YAML with real instrument metadata and thresholds.
- Add vectorbt-based notebooks under `python/notebooks/` for replay analysis.

