###############################################################################
# Kaegan Phillips
# November 5, 2026
#
# test_username_merger.py
#
# Tests for loading, filtering, and deduplicating collected usernames.
###############################################################################

from sixsense.data_collection.username_merger import (
    load_r6_tracker_players,
    load_siegrs_players,
    remove_duplicate_players,
    remove_invalid_players,
    save_players_to_csv,
)

#------------------------------------------------------------------------------
def test_load_r6_tracker_players_keeps_only_pc(tmp_path):
    csv_path = tmp_path / "r6_tracker_players.csv"
    csv_path.write_text(
        "handle,platform,country,rankPoints,position,matchesPlayed,kd\n"
        "PcPlayer,ubi,,3500,1,158,0.88\n"
        "ConsolePlayer,psn,,3500,2,197,1.07\n"
        "XboxPlayer,xbl,,3500,3,225,1.10\n",
        encoding="utf-8",
    )

    assert load_r6_tracker_players(csv_path) == [
        {"username": "PcPlayer", "platform": "uplay"},
    ]

#------------------------------------------------------------------------------
def test_load_siegrs_players_keeps_only_pc(tmp_path):
    csv_path = tmp_path / "siegrs_players.csv"
    csv_path.write_text(
        "username,rank,platform\n"
        "PcPlayer,Gold,uplay\n"
        "ConsolePlayer,Gold,psn\n"
        "XboxPlayer,Gold,xbl\n",
        encoding="utf-8",
    )

    assert load_siegrs_players(csv_path) == [
        {"username": "PcPlayer", "platform": "uplay"},
    ]

#------------------------------------------------------------------------------
def test_remove_invalid_players():
    players = [
        {"username": "GoodPlayer", "platform": "uplay"},
        {"username": "1BadPlayer", "platform": "uplay"},
        {"username": "ab", "platform": "uplay"},
    ]

    assert remove_invalid_players(players) == [
        {"username": "GoodPlayer", "platform": "uplay"},
    ]

#------------------------------------------------------------------------------
def test_remove_duplicate_players_ignores_case_and_keeps_first():
    players = [
        {"username": "Saucy_Arrow", "platform": "uplay"},
        {"username": "saucy_arrow", "platform": "uplay"},
        {"username": "SAUCY_ARROW", "platform": "uplay"},
        {"username": "Other_Player", "platform": "uplay"},
    ]

    assert remove_duplicate_players(players) == [
        {"username": "Saucy_Arrow", "platform": "uplay"},
        {"username": "Other_Player", "platform": "uplay"},
    ]

#------------------------------------------------------------------------------
def test_save_players_to_csv_creates_directory_and_header(tmp_path):
    csv_path = tmp_path / "data" / "usernames.csv"

    players = [{"username": "Saucy_Arrow", "platform": "uplay"}]

    save_players_to_csv(players, csv_path)

    assert csv_path.read_text(encoding="utf-8").splitlines() == [
        "username,platform",
        "Saucy_Arrow,uplay",
    ]

