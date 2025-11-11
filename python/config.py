from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class InstrumentConfig:
    symbol: str
    venues: List[str]
    threshold: float


@dataclass
class Settings:
    instruments: Dict[str, InstrumentConfig] = field(default_factory=dict)
    zerodha_api_key: str = ""
    zerodha_access_token: str = ""
    parity_threshold_default: float = 0.01
    logging_path: Path = Path("/tmp/parity_arb.log")


def load_settings() -> Settings:
    # TODO: Parse configs/instruments.yml and thresholds.yml once format is finalized.
    return Settings()

