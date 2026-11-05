###############################################################################
# Kaegan Phillips
# November 5, 2026
#
# username_validation.py
#
# Checks whether a username follows Ubisoft's official username rules.
###############################################################################

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

