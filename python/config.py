from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class InstrumentConfig:
    symbol: str
    venues: List[str]
    threshold: float


def _default_log_path() -> Path:
    project_root = Path(__file__).resolve().parent.parent
    return project_root / "logs" / "parity_arb.log"


@dataclass
class Settings:
    instruments: Dict[str, InstrumentConfig] = field(default_factory=dict)
    zerodha_api_key: str = ""
    zerodha_api_secret: str = ""
    zerodha_access_token: str = ""
    parity_threshold_default: float = 0.01
    logging_path: Path = field(default_factory=_default_log_path)


def load_settings() -> Settings:
    # TODO: Parse configs/instruments.yml and thresholds.yml once format is finalized.
    return Settings(
        zerodha_api_key=os.getenv("ZERODHA_API_KEY", ""),
        zerodha_api_secret=os.getenv("ZERODHA_API_SECRET", ""),
        zerodha_access_token=os.getenv("ZERODHA_ACCESS_TOKEN", ""),
    )

