###############################################################################
# Kaegan Phillips
# September 18, 2026
#
# siegrs.py
#
# Collects player data from the SIEGRS API and saves players with Ubisoft-valid
# usernames to an output CSV file.
#
# Usage: python -m sixsense.data_collection.siegrs [--start-page N]
###############################################################################

import argparse
import csv
import os
import time

import requests

from sixsense.config import RAW_USERNAMES_DIR

#------------------------------------------------------------------------------
PLAYERS_ENDPOINT = "https://siegrs.gg/api/players"
DEFAULT_PARAMS = {"availability": "all"}

OUTPUT_CSV_FILE = RAW_USERNAMES_DIR / "siegrs_players.csv"

# rank tiers in order of increasing skill level
RANK_TIERS = [
    "Copper", "Bronze", "Silver", "Gold",
    "Platinum", "Emerald", "Diamond", "Champion"
]

# map of SIEGRS platform names to Arenyze expected platform names
PLATFORM_MAP = {
    "PC": "uplay",
    "PS4": "psn",
    "X1": "xbl"
}

MAX_CONSECUTIVE_FAILURES = 3
COOLDOWN_SECONDS = 60
REQUEST_DELAY_SECONDS = 0.2

#------------------------------------------------------------------------------
class TooManyFailuresError(Exception):
    '''Raised when consecutive page failures exceed the maximum allowed.'''
    pass

#------------------------------------------------------------------------------
def fetch_page(page_number):
    '''
    Method to fetch a page of players from the SIEGRS API.

    param: page_number: the page number to fetch
    return: page_data: the JSON data from the fetched page
    '''
    params = {**DEFAULT_PARAMS, "page": page_number}
    response = requests.get(PLAYERS_ENDPOINT, params=params)
    response.raise_for_status()

    return response.json()

#------------------------------------------------------------------------------
def get_page_count():
    '''
    Method to get the last page number from the SIEGRS API metadata.

    return: page_count: the last page number from the SIEGRS API metadata
    '''
    page_data = fetch_page(1)  # fetch the first page to get the metadata

    # page count is the same as the last page number in the metadata
    page_count = page_data["meta"]["last_page"]

    return page_count

#------------------------------------------------------------------------------
def collect_players(page):
    '''
    Method to collect players from a given page. Collects username, rank, and
    platform.

    Only collects players with a valid username and a parseable rank and
    platform.

    param: page: the JSON data from a SIEGRS page
    return: a list of valid players from the page
    '''
    valid_players = []

    for player_data in page["data"]:
        try:
            # extract the username and check if it's valid
            username = player_data["platform_username"]

            if not check_valid_username(username):
                continue

            # extract rank, skip unranked or unparseable ranks
            # e.g. "Bronze II", "Champions", "None"
            rank_name = player_data["rank"]["name"]
            rank = parse_rank(rank_name)

            if rank is None:
                continue

            # extract and map platform, skip unknown platforms
            platform_abbr = player_data["platform"]["abbr"]
            platform = PLATFORM_MAP.get(platform_abbr)

            if platform is None:
                continue

            print(f"\tFound Valid Player: {username} ({rank}, {platform})")

            # create a player dictionary and append it to the valid players
            valid_player = {
                "username": username,
                "rank": rank,
                "platform": platform,
            }

            valid_players.append(valid_player)

        # catch malformed player data and skip to the next player
        except (KeyError, TypeError):
            continue

    return valid_players

#------------------------------------------------------------------------------
def check_valid_username(username):
    '''
    Method to check if a username is valid according to Ubisoft's criteria:

    1. Be 3 to 15 characters long.
    2. Start with a letter.
    3. Only contain letters, numbers, and the following punctuation:
       underscore (_), dash (-), and period (.).

    username: a username to validate
    return: True if the username is valid, False otherwise
    '''
    # ensure length is valid
    if not (3 <= len(username) <= 15):
        return False

    # ensure first character is a letter
    if not username[0].isalpha():
        return False

    # ensure all characters are valid
    for char in username:
        if not (char.isalnum() or char in {'_', '-', '.'}):
            return False

    return True

#------------------------------------------------------------------------------
def parse_rank(rank_name):
    '''
    Method to validate a rank name and parse it into a rank tier e.g "Bronze".

    param: rank_name: the "name" field from a player's rank object, e.g.
           "Bronze II", "Champions", "None".
    return: rank (str) or None
    '''
    if not rank_name or rank_name == "None":
        return None

    # extract the rank tier from the rank name
    for tier in RANK_TIERS:
        if rank_name.startswith(tier):
            return tier

    return None  # return None if the rank name doesn't match any known tier

#------------------------------------------------------------------------------
def save_players_to_csv(players, csv_path):
    '''
    Method to append a list of players to a CSV file. Repeated runs build up
    one continuous file instead of overwriting.

    param: players: a list of player dictionaries to save
    param: csv_path: the file path to save the CSV file to
    '''
    # create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    file_has_content = (
        os.path.exists(csv_path) and os.path.getsize(csv_path) > 0
    )

    with open(csv_path, "a", encoding="utf-8", newline="") as csv_file:
        fieldnames = ["username", "rank", "platform"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if not file_has_content:
            writer.writeheader()

        writer.writerows(players)

#------------------------------------------------------------------------------
def main():
    '''
    Method to collect players from every SIEGRS page, starting at --start-page,
    and append the valid ones to OUTPUT_CSV_FILE.
    '''
    parser = argparse.ArgumentParser(
        description="Collect player data from the SIEGRS API."
    )
    parser.add_argument(
        "--start-page",
        type=int,
        default=1,
        help="Page number to start collecting from (default = 1)."
    )
    args = parser.parse_args()

    # ensure start page is valid
    start_page = args.start_page
    if start_page < 1:
        raise ValueError("Start page must be 1 or greater.")

    players = []
    consecutive_failures = 0
    last_completed_page = start_page - 1  # no pages processed yet
    page_count = "?"  # unknown until the first page is fetched

    try:
        page_count = get_page_count()

        if start_page > page_count:
            print(
                f"Start page ({start_page}) is beyond the last page "
                f"({page_count}). Nothing to do."
            )

        for page_number in range(start_page, page_count + 1):

            try:
                page = fetch_page(page_number)
                players += collect_players(page)

                consecutive_failures = 0  # reset on success
                last_completed_page = page_number

            except requests.exceptions.RequestException as e:
                print(f"\tPage {page_number} Failed: {e}")
                consecutive_failures += 1

                # attempt to cooldown if too many failures in a row
                if consecutive_failures == MAX_CONSECUTIVE_FAILURES:
                    print(
                        f"{consecutive_failures} failures in a row. "
                        f"{COOLDOWN_SECONDS}s cooldown..."
                    )
                    time.sleep(COOLDOWN_SECONDS)

                # halt execution if failures exceed the maximum allowed
                elif consecutive_failures > MAX_CONSECUTIVE_FAILURES:
                    raise TooManyFailuresError(
                        f"{consecutive_failures} failures in a row."
                    ) from e

            # pace every request to avoid rate limiting
            time.sleep(REQUEST_DELAY_SECONDS)

    except TooManyFailuresError as e:
        print(f"\n\nHalting Execution: {e}")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")

    except Exception as e:
        print(f"\n\nUnexpected Error: {e}")

    finally:
        if players:
            save_players_to_csv(players, OUTPUT_CSV_FILE)
            print(
                f"\n\nSaved {len(players)} valid players to "
                f"{OUTPUT_CSV_FILE}"
            )
        else:
            print("\n\nNo players collected -- nothing appended.")

        print(f"Parsed {last_completed_page} / {page_count} available pages.")

#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
