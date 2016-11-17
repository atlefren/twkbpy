# -*- coding: utf-8 -*-
def unzigzag(n_val):
    if (n_val & 1) == 0:
        return n_val >> 1
    return -(n_val >> 1) - 1


def read_varint64(ta_struct):
    #cursor = ta_struct['cursor']
    n_val = 0
    n_shift = 0
    while True:
        n_byte = next(ta_struct['stream'])
        if (n_byte & 0x80) == 0:
            #cursor += 1
            #ta_struct['cursor'] = cursor
            return n_val | (n_byte << n_shift)
        n_val = n_val | (n_byte & 0x7f) << n_shift
        #cursor += 1
        n_shift += 7


def read_varsint64(ta_struct):
    n_val = read_varint64(ta_struct)
    return unzigzag(n_val)
