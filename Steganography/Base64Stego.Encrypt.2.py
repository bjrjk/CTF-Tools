# -*- coding: utf8 -*-
# https://www.tr0y.wang/2017/06/14/Base64steg/

import base64
flag = 'Tr0y{Base64isF4n}'
bin_str = ''.join([bin(ord(c)).replace('0b', '').zfill(8) for c in flag])
base64chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
with open('Encrypt.txt', 'rb') as f0, open('Decrypt.txt', 'wb') as f1:
    for line in f0.readlines():
        rowstr = base64.b64encode(line.replace('\n', ''))
        equalnum = rowstr.count('=')
        if equalnum and len(bin_str):
            offset = int('0b'+bin_str[:equalnum * 2], 2)
            char = rowstr[len(rowstr) - equalnum - 1]
            rowstr = rowstr.replace(char, base64chars[base64chars.index(char) + offset])
            bin_str = bin_str[equalnum*2:]
        f1.write(rowstr + '\n')

