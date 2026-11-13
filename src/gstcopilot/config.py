"""Central settings: paths, GST thresholds and model name.

Values come from environment variables (loaded from a local .env file if present),
with safe defaults so tests run without any setup.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ---- Paths ----
REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = Path(os.getenv("GSTCOPILOT_DATA_DIR", REPO_ROOT / "data"))
DB_PATH = Path(os.getenv("GSTCOPILOT_DB", DATA_DIR / "gst.db"))

# ---- Synthetic data ----
DEFAULT_SEED = 42

# ---- DRC-01C threshold (Rule 88D) ----
# Intimation when GSTR-3B ITC exceeds GSTR-2B ITC by MORE than both limits.
# The portal limit is configurable by the GST Council, so keep it as a setting.
DRC01C_PCT_THRESHOLD = float(os.getenv("DRC01C_PCT_THRESHOLD", "20"))  # percent
DRC01C_AMOUNT_THRESHOLD = float(os.getenv("DRC01C_AMOUNT_THRESHOLD", "2500000"))  # rupees (Rs 25 lakh)

# ---- LLM ----
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or None
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

# ---- Agent SQL limits ----
SQL_ROW_LIMIT = 200
SQL_TIMEOUT_SECONDS = 5
