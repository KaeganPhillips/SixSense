###############################################################################
# Kaegan Phillips
# November 4, 2026
#
# config.py
#
# Central location for SixSense file paths and environment settings.
###############################################################################

import os
from pathlib import Path

#------------------------------------------------------------------------------
# root of all collected and processed data, relative to the working directory
# unless overridden by the SIXSENSE_DATA_DIR environment variable
DATA_DIR = Path(os.environ.get("SIXSENSE_DATA_DIR", "data"))

RAW_DIR = DATA_DIR / "raw"              # data as collected, never modified
INTERIM_DIR = DATA_DIR / "interim"      # cleaned and merged intermediate data
PROCESSED_DIR = DATA_DIR / "processed"  # model-ready feature tables

RAW_USERNAMES_DIR = RAW_DIR / "usernames"
RAW_ARENYZE_DIR = RAW_DIR / "arenyze"
