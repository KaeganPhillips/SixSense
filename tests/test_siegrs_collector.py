###############################################################################
# Kaegan Phillips
# November 4, 2026
#
# test_siegrs_collector.py
#
# Tests for the SIEGRS collector's rank parsing and page filtering.
###############################################################################

import pytest

from sixsense.data_collection.siegrs_collector import (
    collect_players,
    parse_rank,
)

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

