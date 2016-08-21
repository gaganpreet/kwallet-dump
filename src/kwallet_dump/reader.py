#!/usr/bin/env python3
from . import util
from Crypto.Cipher import Blowfish
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512, HMAC

import struct

class InvalidKWallet(Exception): pass
class PasswordMissing(Exception): pass

class KWalletReader:
    '''
        Class to read a kwallet file, verify it's valid, 
        use password to decrypt and keep the encrypted part
    '''
    def __init__(self, filename, salt_filename=None, password=None):
        ''' Initialize a KWallet.

            Arguments:
                filename: Path to KWallet file
                password: Password for the wallet
        '''
        self.salt_filename = salt_filename
        with open(filename, "rb") as kwallet_file:
            self.encrypted = self.parse_and_verify_kwallet(kwallet_file)

            self.key = None
            if password:
                self.key = self.set_password(self, password)

    def set_password(self, password):
        ''' Set a password for the KWallet
            
            Arguments:
                password: Password for the wallet
            Return:
                None
        '''
        if self.sha512pbkdf2:
            if not self.salt_filename:
                raise InvalidKWallet('A salt file is required for this format, typically located in the same directory as the .kwl')
            with open(self.salt_filename, 'rb') as salt_file:
                salt = salt_file.read()

            # PBKDF2 parameters are constants in
            # kwallet/src/runtime/kwalletd/backend/kwalletbackend.h
            self.key = PBKDF2(password, salt, dkLen=56, count=50000, prf=lambda p,s: HMAC.new(p,s,SHA512).digest())
        else:
            self.key = util.password2hash(password)

    def decrypt(self):
        ''' Decrypt a kwallet '''
        if not self.key:
            raise PasswordMissing('Set the password first')

        # Unfortunately, KWallet's Blowfish implementation is a little wrong
        # It seems to have the wrong endianness than of native systems, 
        # this following line fixes that
        self.encrypted = util.switch_endianness(self.encrypted)

        bf = Blowfish.new(self.key)
        decrypted = bf.decrypt(self.encrypted)

        # And switch the endianness again
        return util.switch_endianness(decrypted)

    def parse_and_verify_kwallet(self, kwallet_file):
        ''' Open a kwallet file and do some sanity checks:
                1 Verify magic header
                2 Verify kwallet compatibility
                3 Do some for loops I have no idea about
                4 Get the actual encrypted text, verify it's divisible by block_size and return it
        '''
        self._verify_magic(kwallet_file)
        self._parse_format_header(kwallet_file)
        self._weird_loop(kwallet_file)

        remaining = kwallet_file.read()
        if self._verify_length(remaining) == True:
            return remaining
    
    @staticmethod
    def _verify_magic(kwallet_file):
        ''' Verify magic header of kwallet file '''
        kwallet_magic = b'KWALLET\n\r\0\r\n'
        magic_len = len(kwallet_magic)
        if kwallet_file.read(magic_len) != kwallet_magic:
            raise InvalidKWallet('Magic header doesn\'t match')

    def _parse_format_header(self, kwallet_file):
        ''' Verify kwallet compatibility and parse the cipher specified in the
            file header.

            Details of kwallet_info:
                # First byte - major version - should be 0
                # Second byte - minor version - should be 0
                # Third byte - cipher used - CBC == 0
                # Fourth byte - hash used - SHA1 == 0
        '''
        (major, minor, cipher, hashtype) = struct.unpack("bbbb", kwallet_file.read(4))
        if major == 0 and minor == 0 and cipher == 0 and hashtype == 0:
            self.sha512pbkdf2 = False
            return
        if major == 0 and minor == 1 and cipher == 0 and hashtype == 2:
            self.sha512pbkdf2 = True
            return # hashing is PBKDF2
        raise InvalidKWallet('Filetype not supported')

    @staticmethod
    def _weird_loop(kwallet_file):
        ''' 
            I have no idea wtf this block of code does. 
            It's a copy from C++ code to Python - the original
            C++ code is not commented
        '''
        hash_count = util.to_int(kwallet_file.read(4))
        for _ in range(hash_count):
            kwallet_file.read(16)
            fsz = util.to_int(kwallet_file.read(4))
            kwallet_file.read(16 * fsz)
          
    @staticmethod
    def _verify_length(encrypted):
        ''' Verify that the length of encrypted content is 
            divisible by block size (8) 
        '''
        if len(encrypted) % 8:
            raise InvalidKWallet("File contents are not valid")
        return True
