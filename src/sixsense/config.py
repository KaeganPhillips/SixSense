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
# root of all collected data, relative to the working directory unless
# overridden by the SIXSENSE_DATA_DIR environment variable
DATA_DIR = Path(os.environ.get("SIXSENSE_DATA_DIR", "data"))

# usernames exactly as collected from each source, one CSV file per source
RAW_DIR = DATA_DIR / "raw"

# data cleaned, merged, or built from the raw data
PROCESSED_DIR = DATA_DIR / "processed"

# every valid, unique username collected, merged from all sources
USERNAMES_CSV_FILE = PROCESSED_DIR / "usernames.csv"

# detailed player data collected from Arenyze, one file per player
PLAYERS_DIR = PROCESSED_DIR / "players"

