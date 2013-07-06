#!/usr/bin/env python3
import util
from Crypto.Cipher import Blowfish

class InvalidKWallet(Exception): pass
class PasswordMissing(Exception): pass

class KWalletReader:
    def __init__(self, filename, password=None):
        ''' Initialize a KWallet.

            Arguments:
                filename: Path to KWallet file
                password: Password for the wallet
        '''
        with open(filename, "rb") as f:
            self.contents = f.read()
            self.encrypted = self.parse_and_verify_kwallet(self.contents)

            self.key = None
            if password:
                self.key = util.password2hash(password)

    def set_password(self, password):
        ''' Set a password for the KWallet
            
            Arguments:
                password: Password for the wallet
            Return:
                None
        '''
        self.key = util.password2hash(password)

    def decrypt(self):
        ''' Decrypt a kwallet '''
        if not self.key:
            raise PasswordMissing('Set the password first')

            
        # Unfortunately, KWallet's Blowfish implementation is a little wrong
        # It seems to have the wrong endianness than of native systems, this following
        # line fixes that
        self.encrypted = util.switch_endianness(self.encrypted)

        bf = Blowfish.new(self.key)
        decrypted = bf.decrypt(self.encrypted)

        # And switch the endianness again
        return util.switch_endianness(decrypted)

    def parse_and_verify_kwallet(self, contents):
        ''' Open a kwallet file and do some sanity checks:
                1 Verify magic header
                2 Verify kwallet compatibility
                3 Do some for loops I have no idea about
                4 Get the actual encrypted text, verify it's divisible by block_size and return it
        '''
        offset = 0

        # This might have been better handled with StringIO
        offset = self._verify_magic(offset)
        offset = self._verify_compatibility(offset)
        offset = self._weird_loop(offset)
        self._verify_length(offset)
        return self.contents[offset:]
    
    def _verify_magic(self, offset):
        ''' Verify magic header of kwallet file '''
        kwallet_magic = b'KWALLET\n\r\0\r\n'
        magic_len = len(kwallet_magic)
        if self.contents[:magic_len] != kwallet_magic:
            raise InvalidKWallet('Magic header doesn\'t match')
        offset += magic_len
        return offset

    def _verify_compatibility(self, offset):
        ''' Verify kwallet compatibility
            # Details of kwallet_info
            # First byte - major version - should be 0
            # Second byte - minor version - should be 0
            # Third byte - cipher used - CBC == 0
            # Fourth byte - hash used - SHA1 == 0
        '''
        kwallet_info = self.contents[offset:offset+4]
        if kwallet_info != b'\0'*4:
            raise InvalidKWallet('Filetype not supported')
        offset += 4
        return offset

    def _weird_loop(self, offset):
        ''' 
            I have no idea wtf this block of code does. 
            It's a copy from C++ code to Python - the original
            C++ code is not commented
        '''
        hash_count = util.to_int(self.contents[offset:offset+4])
        offset += 4
        for i in range(hash_count):
            offset += 16
            fsz = util.to_int(self.contents[offset:offset+4])
            offset += 4
            for j in range(fsz):
                offset += 16
        return offset

          
    def _verify_length(self, offset):
        ''' Verify that the length of encrypted content is divisible by block size (8) '''
        enc_length = len(self.contents) - offset
        if enc_length % 8:
            raise InvalidKWallet("File contents are not valid")
