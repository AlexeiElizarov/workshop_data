import os
import string
import hashlib

def generate_random_string(length,
                           stringset="".join(
                               [string.ascii_uppercase+string.digits]
                           )):

    return "".join([stringset[i%len(stringset)] for i in [x for x in os.urandom(length)]]).encode()

solt = "dskljfwqj".encode()

def salted_hash(string):
    return hashlib.sha1(b" ".join([
        string,
        solt,
    ])).hexdigest()






