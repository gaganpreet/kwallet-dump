#!/usr/bin/env python3
import argparse
import getpass
import sys
from kwallet_dump import kwallet, reader

def parse_filename():
    parser = argparse.ArgumentParser(description='Dump a .kwl kwallet file')
    parser.add_argument('filename', help='Location of kwallet file')

    args = parser.parse_args()
    return args.filename

def main():
    filename = parse_filename()
    try:
        wallet = reader.KWalletReader(filename)
    except reader.InvalidKWallet as e:
        print('Invalid file error: ' + str(e))
        sys.exit(1)

    password = getpass.getpass('Wallet Password: ')
    wallet.set_password(password)

    decrypted = wallet.decrypt()

    wallet = kwallet.KWallet(decrypted)
    for entry in wallet.get_entries():
        print(entry)


if __name__ == '__main__':
    main()
