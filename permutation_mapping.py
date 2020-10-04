#!/usr/bin/env python3

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from intermediate_number import *

class PermutationMapping(ABC):

    @classmethod
    def from_permutation(cls, permutation: int) -> IntermediateNumber:
        s = str(permutation)
        assert set(map(int, s)) == set([i + 1 for i in range(len(s))]), 'must be a valid permutation of 1 to n'
        numbers = [int(c) for c in str(permutation)]
        return cls._from_perm(numbers)

    @classmethod
    def to_permutation(cls, intermediate: IntermediateNumber) -> int:
        numbers = cls._to_perm(intermediate)
        return ''.join(map(str, numbers))

    @staticmethod
    @abstractmethod
    def _from_perm(permutation: List[int]) -> IntermediateNumber:
        pass

    @staticmethod
    @abstractmethod
    def _to_perm(intermediate: IntermediateNumber) -> List[int]:
        pass


class LexicographicalMapping(PermutationMapping):

    @staticmethod
    def _from_perm(numbers: List[int]) -> IntermediateNumber:
        intermediate = []
        for i, num in enumerate(numbers[:-1]):
            intermediate.append(len([i for i in numbers[i + 1:] if i < num]))
        return IncrementalBasedNumber(intermediate, len(numbers))

    @staticmethod
    def _to_perm(intermediate: IntermediateNumber) -> List[int]:
        assert isinstance(intermediate, IncrementalBasedNumber)
        appeared = set()
        num_count = intermediate.digits
        permutation = [0] * num_count
        for i, num in enumerate(intermediate.numbers):
            temp = num + 1 # trying from smaller_count + 1
            smaller_count = len([i for i in appeared if i < temp])
            while temp in appeared or temp - smaller_count != num + 1:
                assert(temp <= 9)
                temp += 1
                smaller_count = len([i for i in appeared if i < temp])
            appeared.add(temp)
            permutation[i] = temp
        last = list(set([i + 1 for i in range(num_count)]).difference(appeared))
        assert len(last) == 1
        permutation[-1] = last[0]
        return permutation


class IncrementalBasedMapping(PermutationMapping):

    @staticmethod
    def _from_perm(numbers: List[int]) -> IntermediateNumber:
        intermediate = []
        n = len(numbers)
        while n >= 2:
            intermediate.append(len([i for i in numbers[numbers.index(n) + 1:] if i < n]))
            n -= 1  
        return IncrementalBasedNumber(intermediate, len(numbers))

    @staticmethod
    def _to_perm(intermediate: IntermediateNumber) -> List[int]:
        assert isinstance(intermediate, IncrementalBasedNumber)
        num_count = intermediate.digits
        permutation = [0] * num_count
        for i, space_num in enumerate(intermediate.numbers):
            target = num_count - i
            j = num_count - 1
            space_count = 0
            while space_count < space_num or permutation[j] != 0:
                if permutation[j] == 0:
                    space_count += 1
                j -= 1
            permutation[j] = target
        assert permutation.count(0) == 1
        permutation[permutation.index(0)] = 1
        return permutation


class DecrementalBasedMapping(PermutationMapping):

    @staticmethod
    def _from_perm(numbers: List[int]) -> IntermediateNumber:
        intermediate = []
        n = 2
        while n <= len(numbers):
            intermediate.append(len([i for i in numbers[numbers.index(n) + 1:] if i < n]))
            n += 1
        return DecrementalBasedNumber(intermediate, len(numbers))

    @staticmethod
    def _to_perm(intermediate: IntermediateNumber) -> List[int]:
        assert isinstance(intermediate, DecrementalBasedNumber)
        num_count = intermediate.digits
        permutation = [0] * num_count
        for i, space_num in enumerate(reversed(intermediate.numbers)):
            target = num_count - i
            j = num_count - 1
            space_count = 0
            while space_count < space_num or permutation[j] != 0:
                if permutation[j] == 0:
                    space_count += 1
                j -= 1
            permutation[j] = target
        assert permutation.count(0) == 1
        permutation[permutation.index(0)] = 1
        return permutation
    

class SJTMapping(PermutationMapping):

    @staticmethod
    def _from_perm(numbers: List[int]) -> IntermediateNumber:
        num_count = len(numbers)
        intermediate = [0] * (num_count - 1)
        directions = [False] * (num_count - 1)
        for i in range(num_count - 1):
            target = i + 2
            direction = False # default to left
            if i % 2 == 0 and i >= 2:
                direction = (intermediate[i - 1] + intermediate[i - 2]) % 2 == 1
            else:
                direction = intermediate[i - 1] % 2 == 1
            pos = numbers.index(target)
            if not direction: # points to left, look right
                intermediate[i] = len([i for i in numbers[pos + 1:] if i < target])
            else: # look left
                intermediate[i] = len([i for i in numbers[:pos] if i < target])
            directions[i] = direction
        return DirectionalDecrementalBasedNumber(intermediate, directions, len(numbers))

    @staticmethod
    def _to_perm(intermediate: IntermediateNumber) -> List[int]:
        assert isinstance(intermediate, DecrementalBasedNumber)
        num_count = intermediate.digits
        permutation = [0] * num_count
        numbers = intermediate.numbers
        for i in reversed(range(num_count - 1)):
            target = i + 2
            space_num = numbers[i]
            direction = False # default to left
            if i % 2 == 0 and i >= 2:
                direction = (numbers[i - 1] + numbers[i - 2]) % 2 == 1
            else:
                direction = numbers[i - 1] % 2 == 1
            if not direction: # points to left, start from right
                j = num_count - 1
                space_count = 0
                while space_count < space_num or permutation[j] != 0:
                    if permutation[j] == 0:
                        space_count += 1
                    j -= 1
                permutation[j] = target
            else: # start from left
                j = 0
                space_count = 0
                while space_count < space_num or permutation[j] != 0:
                    if permutation[j] == 0:
                        space_count += 1
                    j += 1
                permutation[j] = target
        assert permutation.count(0) == 1
        permutation[permutation.index(0)] = 1
        return permutation
