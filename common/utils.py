# -*- coding: utf-8 -*-

import random
import time
import hashlib
import string
from random import choice
from django.utils.encoding import smart_str
from string import ascii_letters, digits

__author__ = 'oks'


def generate_id(size=None):
    import uuid
    if size is not None:
        if size < 17:
            raise Exception(u"Size must be ≥ 17")
        tm = int(time.time()*1000)
        code = generate_code(size - len(str(tm)), digits=False, upper_case=False)
        return u"{}{}".format(tm, code)
    return uuid.uuid1().hex


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
    if first:
        return choice(first) + ''.join(choice(chars) for x in range(length - 1) if x)
    else:
        return ''.join(choice(chars) for x in range(length - 1) if x)


def get_hexdigest(algorithm, salt, raw_password):
    """
    Returns a string of the hexdigest of the given plaintext password and salt
    using the given algorithm ('md5', 'sha1' or 'crypt').
    """

    raw_password, salt = smart_str(raw_password), smart_str(salt)

    if algorithm == 'md5':
        return hashlib.md5(salt + raw_password).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(salt + raw_password).hexdigest()
    raise ValueError("Got unknown password algorithm type in password.")


def gen_hash(password, salt=None, algorithm='sha512'):
    hash_lib = hashlib.new(algorithm)
    hash_lib.update(smart_str(password))
    if salt is None:
        salt = ''.join([random.choice(ascii_letters + digits) for _ in range(8)])
    hash_lib.update(salt)
    return algorithm, salt, hash_lib.hexdigest()


def set_password(raw_password):
    algorithm = 'sha1'
    salt = get_hexdigest(algorithm, str(random.random()), str(random.random()))[:5]
    hsh = get_hexdigest(algorithm, salt, raw_password)
    return '%s$%s$%s' % (algorithm, salt, hsh)


def check_password(raw_password, enc_password):
    """
    Returns a boolean of whether the raw_password was correct. Handles
    encryption formats behind the scenes.
    """
    try:
        algo, salt, hsh = enc_password.split('$')
    except:
        raise ValueError("You've mistakenly set the password directly. Please use set_password() instead.")
    if algo == 'sha512':
        return hsh == gen_hash(raw_password, salt, algo)[-1]
    return hsh == get_hexdigest(algo, salt, raw_password)


def zip_values(iterable, dict2, empty_fields=False):
    """

    :type iterable: iter
    :type dict2: dict
    :return: list of tuples with keys in both dicts if not empty, else all keys in the left dict (left join)
    :rtype: list
    """
    zipped = []
    assert isinstance(dict2, dict)
    if not all([iterable, dict2]):
        return []

    if isinstance(iterable, dict):
        for k, v in iterable.iteritems():
            if (not empty_fields and (k not in dict2.keys())) or (not empty_fields and (dict2.get(k) is None)):
                continue
            zipped.append((v, dict2.get(k)))

    elif isinstance(iterable, list):
        for k in iterable:
            if (not empty_fields and (k not in dict2.keys())) or (not empty_fields and (dict2.get(k) is None)):
                continue
            zipped.append((k, dict2.get(k)))

    return zipped


def extended_cmp(val1, val2):
    if not isinstance(val1, list):
        return cmp(val1, val2)
    for i, v in enumerate(val1):
        if cmp(v, val2[i]):
            if isinstance(v, dict):
                cum_eq = sum([cmp(x, y) for x, y in zip_values(v, val2[i])])
                return cum_eq
            return 1
    return 0