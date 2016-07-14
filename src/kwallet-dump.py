#!/usr/bin/env python3
import argparse
import getpass
import sys
from kwallet_dump import kwallet, reader

def parse_args():
    parser = argparse.ArgumentParser(description='Dump a .kwl kwallet file')
    parser.add_argument('filename', help='Location of kwallet file')
    parser.add_argument(
        'salt_filename',
        help='Location of salt file for PBKDF2-derived files (since KDE 4.13)',
        nargs='?',
    )

    return parser.parse_args()

def main():
    args = parse_args()
    try:
        wallet = reader.KWalletReader(args.filename, args.salt_filename)
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
