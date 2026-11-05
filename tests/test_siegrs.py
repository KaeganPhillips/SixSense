###############################################################################
# Kaegan Phillips
# November 4, 2026
#
# test_siegrs.py
#
# Tests for the SIEGRS collector's username validation and rank parsing.
###############################################################################

import pytest

from sixsense.data_collection.siegrs import (
    check_valid_username,
    collect_players,
    parse_rank,
)

#------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "username", ["abc", "Saucy_Arrow", "a.b-c_d", "x" * 15]
)
def test_valid_usernames(username):
    assert check_valid_username(username)

#------------------------------------------------------------------------------
@pytest.mark.parametrize("username", [
    "ab",           # too short
    "x" * 16,       # too long
    "1player",      # starts with a number
    "_player",      # starts with punctuation
    "bad name",     # contains a space
    "bad@name",     # contains invalid punctuation
])
def test_invalid_usernames(username):
    assert not check_valid_username(username)

#------------------------------------------------------------------------------
@pytest.mark.parametrize("rank_name, expected", [
    ("Bronze II", "Bronze"),
    ("Champions", "Champion"),
    ("Platinum V", "Platinum"),
    ("None", None),
    ("", None),
    (None, None),
    ("Unranked", None),
])
def test_parse_rank(rank_name, expected):
    assert parse_rank(rank_name) == expected

#------------------------------------------------------------------------------
def make_player(username, rank_name, platform_abbr):
    '''Builds a player entry shaped like the SIEGRS API response.'''
    return {
        "platform_username": username,
        "rank": {"name": rank_name},
        "platform": {"abbr": platform_abbr},
    }

#------------------------------------------------------------------------------
def test_collect_players_skips_invalid_entries():
    page = {"data": [
        make_player("GoodPlayer", "Gold III", "PC"),
        make_player("1BadName", "Gold III", "PC"),
        make_player("Unranked", "None", "PC"),
        make_player("Switcher", "Gold III", "NS"),
        {"platform_username": "Malformed"},
    ]}

    assert collect_players(page) == [
        {"username": "GoodPlayer", "rank": "Gold", "platform": "uplay"},
    ]
