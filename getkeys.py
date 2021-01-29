# Citation: Box Of Hats (https://github.com/Box-Of-Hats )
# avail: https://raw.githubusercontent.com/Sentdex/pygta5/master/getkeys.py

import win32api as wapi
import time

keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'£$/\\":
    keyList.append(char)

def key_check():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys
 
