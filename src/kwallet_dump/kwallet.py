#!/usr/bin/env python3
from . import util
from io import BytesIO

class KWallet:
    def __init__(self, contents):
        ''' Initialize a KWallet.

            Caveats:
            1. KWallet is stored in a QDataStream, which is a form of serializing data
            for cross platform usage. This class works on my machine, which is Intel-based x86_64
            little-endian. I haven't tested with any other architectures or endianness, but it should
            hopefully work.

            2. Because KWallet format doesn't have any documentation (that I could find), this is a reverse engineered
            one based on reading the KWallet code and looking at the stream myself. It's not perfect,
            but it works for my wallet files.

            TL;DR: KWallet data is stored in a complex format, and this class can fail while parsing it.

            Arguments:
                contents: QDataStream binary encoded string
        '''
        self.entries = []
        self.initialize(contents)
        
    def initialize(self, contents):
        '''
            Initializes the KWallet encrypted stream into a flattened list
            Arguments:
                contents

            List format:
                [entry_type, folder, key, value]
                    folder - Folder name

                    Then each folder in the stream has multiple entries (the list is flattened):
                        entry_type - Binary Data, Maps, Passwords etc
                        key - Name of key in entry
                        value - Can be binary data, a map (stored as a tuple), password
                    
        '''
        # First 8 bytes are skippable, next 4 bytes store the size of contents
        size = util.to_int(contents[8:12])

        # Reading the string as a file is convenient because it's a stream
        f = BytesIO(contents[12:12+size])

        while f.tell() < size:
            folder = self._read_str(f)

            folder_size = self._read_int(f)

            for _ in range(folder_size):
                key = self._read_str(f)

                ''' Note about entry types:
                    1 -> Password
                    2 -> Binary data
                    3 -> Map
                '''
                entry_type = self._read_int(f)

                if entry_type > 3 or entry_type < 1:
                    raise ValueError('Unsupported entry type, %s'%(entry_type))

                if entry_type == 1:
                    self._read_int(f)

                if entry_type == 3:
                    self._read_int(f)
                    value_count = self._read_int(f)
                    for _ in range(value_count):
                        map_key = self._read_str(f, entry_type)
                        map_value = self._read_str(f, entry_type)
                        self.entries.append([entry_type, folder, key, 
                                            (map_key, map_value)])

                if entry_type == 1 or entry_type == 2:
                    value = self._read_str(f, entry_type)
                    self.entries.append([entry_type, folder, key, value])

    def get_entries(self):
        '''
            Return flattened list of entries
        '''
        return self.entries

    def _read_int(self, f):
        '''
            Read an integer from file from the current location
        '''
        return util.to_int(f.read(4))

    def _read_str(self, f, entry_type=1):
        '''
            Read a QString from file from the current location

            Depending on the entry type (binary vs rest), the string may be stored as it is
            or UTF-16

        '''
        nbytes = self._read_int(f)
        # Null strings are stored as UINT_MAX
        if nbytes == (1 << 32) - 1:
            return ''

        s = f.read(nbytes)
        if entry_type != 2:
            s = s.decode('utf-16-be')
        return s

