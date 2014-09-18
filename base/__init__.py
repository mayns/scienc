# -*- coding: utf-8 -*-

import pytz
import operator
from babel import Locale
from babel.dates import get_timezone_location, get_timezone_gmt
from dateutil import rrule
from datetime import datetime, timedelta
import hashlib
import string
from random import choice
from importlib import import_module

from tornado import gen


__author__ = 'oks'


# ------------------------------- ID, HASH GENERATORS -------------------------------

def generate_id(size=64):
    import uuid
    return uuid.uuid1().int >> size


def generate_code(length, digits=True, low_case=True, upper_case=True):
    chars = ''
    first = ''
    if digits:
        chars += string.digits
    if low_case:
        chars += string.lowercase
        first += string.lowercase
    if upper_case:
        chars += string.uppercase
        first += string.uppercase
    return choice(first) + ''.join(choice(chars) for x in range(length - 1) if x)


def get_hash(string_val):
    return hashlib.md5(string_val).hexdigest()

# ------------------------------- END of ID, HASH GENERATORS --------------------------

