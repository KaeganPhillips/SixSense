###############################################################################
# Kaegan Phillips
# November 5, 2026
#
# username_merger.py
#
# Merges the collected R6 Tracker and SIEGRS usernames into a single CSV file
# of valid PC players with no duplicates.
#
# Usage: python -m sixsense.data_collection.username_merger
###############################################################################

import csv
import os

from sixsense.config import RAW_DIR, USERNAMES_CSV_FILE
from sixsense.data_collection.username_validation import check_valid_username

#------------------------------------------------------------------------------
R6_TRACKER_CSV_FILE = RAW_DIR / "r6_tracker_players.csv"
SIEGRS_CSV_FILE = RAW_DIR / "siegrs_players.csv"

OUTPUT_CSV_FILE = USERNAMES_CSV_FILE

# the platform name Arenyze expects for PC players
PC_PLATFORM = "uplay"

# map of R6 Tracker platform names to Arenyze expected platform names
R6_TRACKER_PLATFORM_MAP = {
    "ubi": PC_PLATFORM
}

#------------------------------------------------------------------------------
def load_r6_tracker_players(csv_path):
    '''
    Method to load the PC players from an R6 Tracker CSV file. Players from any
    other platform are skipped.

    param: csv_path: the file path of the R6 Tracker CSV file
    return: a list of player dictionaries with a username and platform
    '''
    players = []

    with open(csv_path, encoding="utf-8", newline="") as csv_file:
        for row in csv.DictReader(csv_file):
            platform = R6_TRACKER_PLATFORM_MAP.get(row["platform"])

            if platform is None:
                continue

            players.append({"username": row["handle"], "platform": platform})

    return players

#------------------------------------------------------------------------------
def load_siegrs_players(csv_path):
    '''
    Method to load the PC players from a SIEGRS CSV file. Rows from any other
    platform are skipped.

    param: csv_path: the file path of the SIEGRS CSV file
    return: a list of player dictionaries with a username and platform
    '''
    players = []

    with open(csv_path, encoding="utf-8", newline="") as csv_file:
        for row in csv.DictReader(csv_file):
            if row["platform"] != PC_PLATFORM:
                continue

            players.append(
                {"username": row["username"], "platform": row["platform"]}
            )

    return players

#------------------------------------------------------------------------------
def remove_invalid_players(players):
    '''
    Method to remove players whose usernames do not follow Ubisoft's username
    rules.

    param: players: a list of player dictionaries
    return: a list of the players with valid usernames
    '''
    return [
        player for player in players
        if check_valid_username(player["username"])
    ]

#------------------------------------------------------------------------------
def remove_duplicate_players(players):
    '''
    Method to remove duplicate players. Usernames are not case sensitive, so
    usernames that differ only by case are duplicates. The first occurrence
    of each player is kept.

    param: players: a list of player dictionaries
    return: a list of the players with duplicates removed
    '''
    seen = set()
    unique_players = []

    for player in players:
        key = (player["username"].lower(), player["platform"])

        if key in seen:
            continue

        seen.add(key)
        unique_players.append(player)

    return unique_players

#------------------------------------------------------------------------------
def save_players_to_csv(players, csv_path):
    '''
    Method to save a list of players to a CSV file, overwriting any existing
    file.

    param: players: a list of player dictionaries to save
    param: csv_path: the file path to save the CSV file to
    '''
    # create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    with open(csv_path, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["username", "platform"])
        writer.writeheader()
        writer.writerows(players)

#------------------------------------------------------------------------------
def main():
    '''
    Method to merge the R6 Tracker and SIEGRS players into one CSV file of
    valid, deduplicated PC players.
    '''
    players = load_r6_tracker_players(R6_TRACKER_CSV_FILE)
    print(f"Loaded {len(players)} PC players from R6 Tracker.")

    siegrs_players = load_siegrs_players(SIEGRS_CSV_FILE)
    print(f"Loaded {len(siegrs_players)} PC players from SIEGRS.")

    players += siegrs_players
    total_count = len(players)

    players = remove_invalid_players(players)
    print(f"Removed {total_count - len(players)} invalid usernames.")

    valid_count = len(players)
    players = remove_duplicate_players(players)
    print(f"Removed {valid_count - len(players)} duplicate usernames.")

    save_players_to_csv(players, OUTPUT_CSV_FILE)
    print(f"Saved {len(players)} players to {OUTPUT_CSV_FILE}")

#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

