#!/usr/bin/env python3

from intermediate_number import IncrementalBasedNumber, DecrementalBasedNumber
from permutation_mapping import *

mapping_list = [
    (LexicographicalMapping, IncrementalBasedNumber),
    (IncrementalBasedMapping, IncrementalBasedNumber),
    (DecrementalBasedMapping, DecrementalBasedNumber),
    (SJTMapping, DecrementalBasedNumber)
]

if __name__ == '__main__':

    for mapping, number in mapping_list:
        print(mapping.__name__, number.__name__)
        orig = 83674521
        a = mapping.from_permutation(orig)
        print(orig, a)

        sub = 2020
        b = number(sub, 8, True)
        print(sub, b)

        c = a - b
        perm = (mapping.to_permutation(c))
        print(perm, c)
        print()
