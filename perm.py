#!/usr/bin/env python3

from intermediate_number import *
from permutation_mapping import *

mapping_list = [
    (LexicographicalMapping, IncrementalBasedNumber),
    (IncrementalBasedMapping, IncrementalBasedNumber),
    (DecrementalBasedMapping, DecrementalBasedNumber),
    (SJTMapping, DecrementalBasedNumber)
]

if __name__ == '__main__':

    for mapping, number in mapping_list:
        print(f'Use {mapping.__name__} with {number.__name__}')

        # the original permutation
        orig = 83674521
        a = mapping.from_permutation(orig)
        print(f'Original:\t{orig}\t{a}')

        # the delta from intermediate number of the original permutation
        sub = 2020
        b = number(sub, len(str(orig)), True)
        print(f'Delta:\t\t{sub}\t\t{b}')

        # the calculated permutation from original +/- delta
        try:
            c = a - b
            perm = mapping.to_permutation(c)
        except:
            c = 'underflow'
            perm = 'underflow'
        print(f'Sub:\t\t{perm}\t{c}')
        try:
            d = a + b
            perm = mapping.to_permutation(d)
        except:
            d = 'overflow'
            perm = 'overflow'
        print(f'Add:\t\t{perm}\t{d}')
        print()
