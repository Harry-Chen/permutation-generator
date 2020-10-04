#!/usr/bin/env python3

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, ClassVar, Union

class IntermediateNumber(ABC):

    numbers: ClassVar[List[int]]
    digits: int

    def __init__(self, number: Union[List[int], int], digits: int, from_natural: bool):

        self.digits = digits
        if from_natural:
            self.numbers = self.from_natural(number)
        else:
            if isinstance(number, int): # convert int to List[int]
                numbers = [int(c) for c in str(number)]
            else:
                numbers = number
            if not self.check(numbers):
                raise ValueError(f'number not valid: {numbers}')
            self.numbers = numbers
        if digits - 1 > len(self.numbers):
            self.numbers = [0] * (digits - 1 - len(self.numbers)) + self.numbers
    
    def __str__(self):
        return f'{self.__class__.__name__[:3]}({"".join(map(str, self.numbers))})'

    # no actual checking now
    def check(self, number: List[int]) -> bool:
        return True

    def __add__(self, rhs: IntermediateNumber):
        assert isinstance(rhs, IntermediateNumber)
        assert type(self) == type(rhs)
        return self.add(rhs)

    def __sub__(self, rhs: IntermediateNumber):
        assert isinstance(rhs, IntermediateNumber)
        assert type(self) == type(rhs)
        assert self.to_natural() >= rhs.to_natural()
        return self.sub(rhs)
    
    # generate from natural number
    @abstractmethod
    def from_natural(self, natural: int) -> List[int]:
        pass

    # convert back to natural number
    @abstractmethod
    def to_natural(self) -> int:
        pass

    @abstractmethod
    def add(self, rhs: IntermediateNumber):
        pass

    @abstractmethod
    def sub(self, rhs: IntermediateNumber):
        pass

class IncrementalBasedNumber(IntermediateNumber):

    def __init__(self, numbers: Union[List[int], int], digits = 9, from_natural: bool = False):
        super(IncrementalBasedNumber, self).__init__(numbers, digits, from_natural)

    def from_natural(self, natural: int) -> List[int]:
        assert natural > 0
        i, fac = 1, 1
        while fac <= natural:
            i += 1
            fac *= i
        fac //= i
        i -= 1
        numbers = []
        while i > 0:
            numbers.append(natural // fac)
            natural %= fac
            fac //= i
            i -= 1
        return numbers
        
    def to_natural(self) -> int:
        fac, natural = 1, 0
        for i, num in enumerate(reversed(self.numbers)):
            natural += fac * num
            fac *= i + 2
        return natural

    def add(self, rhs: IncrementalBasedNumber):
        return IncrementalBasedNumber(self.to_natural() + rhs.to_natural(), self.digits, True)
    
    def sub(self, rhs: IncrementalBasedNumber):
        return IncrementalBasedNumber(self.to_natural() - rhs.to_natural(), self.digits, True)


class DecrementalBasedNumber(IntermediateNumber):

    def __init__(self, numbers: Union[List[int], int], digits = 9, from_natural: bool = False):
        super(DecrementalBasedNumber, self).__init__(numbers, digits, from_natural)

    def from_natural(self, natural: int) -> List[int]:
        assert natural > 0
        k = self.digits
        numbers = []
        while natural > 0:
            assert k >= 1, 'digits not enough for decremental-based number'
            numbers.append(natural % k)
            natural //= k
            k -= 1
        return list(reversed(numbers))
        
    def to_natural(self) -> int:
        k = self.digits - len(self.numbers) + 1
        natural = 0
        for i, num in enumerate(self.numbers):
            natural *= k
            natural += num
            k += 1
        return natural

    def add(self, rhs: DecrementalBasedNumber):
        return DecrementalBasedNumber(self.to_natural() + rhs.to_natural(), self.digits, True)
    
    def sub(self, rhs: DecrementalBasedNumber):
        return DecrementalBasedNumber(self.to_natural() - rhs.to_natural(), self.digits, True)
