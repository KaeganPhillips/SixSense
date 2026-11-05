###############################################################################
# Kaegan Phillips
# November 5, 2026
#
# test_username_validation.py
#
# Tests for Ubisoft username validation.
###############################################################################

import pytest

from sixsense.data_collection.username_validation import check_valid_username

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

