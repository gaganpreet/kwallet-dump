#!/usr/bin/env python3 

import hashlib
import struct

def block2hash(block):
    s = hashlib.sha1()
    s.update(block)
    r = ''
    for i in range(2000):
        r = s.digest()
        s = hashlib.sha1()
        s.update(r)
    return r

def password2hash(password):
    blocks = get_blocks(password, 16)
    hashed_blocks = [block2hash(block.encode('utf-8')) for block in blocks]

    if len(password) <= 16:
        # Key size of 20
        return b''.join(hashed_blocks)
    elif len(password) <= 32:
        # Key size of 40 (20/20)
        return b''.join(hashed_blocks)
    elif len(password) <= 48:
        # Key size of 56 (20/20/16 split)
        return hashed_blocks[0] + hashed_blocks[1] + hashed_blocks[2][:16]
    else:
        # Key size of 56 (14/14/14/14 split)
        return b''.join([block[:14] for block in hashed_blocks])

def get_blocks(text, block_size):
    ''' Divide a string into equal sized blocks '''
    return [text[start:start+block_size] for start in range(0, len(text), block_size)] or ['']

def switch_endianness(s):
    ''' Switch the endianness of byte string '''
    if len(s) % 4:
        raise IndexError('String should be a multiple of 4')

    return b''.join([i[::-1] for i in get_blocks(s, 4)])

def to_int(s):
    return struct.unpack('>I', s)[0]
