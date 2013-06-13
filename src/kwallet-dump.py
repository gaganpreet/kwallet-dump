#!/usr/bin/env python3
import argparse
import getpass
import sys
import reader

def parse_filename(args):
    parser = argparse.ArgumentParser(description='Dump a .kwl kwallet file')
    parser.add_argument('filename', help='Location of kwallet file')

    args = parser.parse_args()
    return args.filename

def main():
    filename = parse_filename(sys.argv)
    try:
        wallet = reader.KWalletReader(filename)
    except reader.InvalidKWallet as e:
        print('Invalid file error: ' + str(e))
        sys.exit(1)

    password = getpass.getpass('Wallet Password: ')
    wallet.set_password(password)
    print(wallet.decrypt())

if __name__ == '__main__':
    main()

