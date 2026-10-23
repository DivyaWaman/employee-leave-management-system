from .constants import *


# =========================================================
# FORMAT DAYS
# =========================================================

def format_days(number):

    if number == int(number):
        return str(int(number))

    return str(number)

def get_initials(name):
    """'Sunil Batade' -> 'SB' (at most two letters)."""
    initials = ""
    for word in name.split():
        initials = initials + word[0]
    return initials[:2].upper()          # [:2] = keep only the first two letters
