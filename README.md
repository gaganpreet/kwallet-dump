# About
A Python script to dump contents of a .kwl kwallet file for accessing passwords away from KDE desktop. Should work on wallets created on KDE 4 (written on KDE 4.10).

The output is not polished because it serves a simple utility - to get passwords when not around a KDE desktop. Pipe the output to grep to make it more usable.

If you are looking to get Chrome passwords out of this - it'll be a bit difficult because Chrome stores the passwords in a serialized blob and you'll have to decipher that format. For everything else - Firefox, Telepathy, Amarok, Wifi passwords, other apps which store passwords - it works perfectly fine.

# Output
* Fields:
    + Type of KWallet entry - there are 3 - Password, Binary Data and Map. The sample output here shows the third format
    + Folder name
    + Key name
    + Value - Value is a tuple when entry type is a Map

* Sample Output:

        [3, 'Firefox', 'admin,,DD-WRT,http://192.168.1.1', ('usernameField', '')]
        [3, 'Firefox', 'admin,,DD-WRT,http://192.168.1.1', ('username', 'user')]
        [3, 'Firefox', 'admin,,DD-WRT,http://192.168.1.1', ('passwordField', '')]
        [3, 'Firefox', 'admin,,DD-WRT,http://192.168.1.1', ('password', 'password')]
        [3, 'Firefox', 'admin,,DD-WRT,http://192.168.1.1', ('httpRealm', 'DD-WRT')]
        [3, 'Firefox', 'admin,,DD-WRT,http://192.168.1.1', ('hostname', 'http://192.168.1.1')]
        [3, 'Firefox', 'admin,,DD-WRT,http://192.168.1.1', ('formSubmitURL', '')]

# Requirements
* Python 3
* pycrypto (for decoding Blowfish)
