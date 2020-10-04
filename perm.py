#!/usr/bin/env python3

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, ClassVar

class IntermediateNumber(ABC):

    numbers: ClassVar[List[int]]

    def __init__(self, number: int, from_natural: bool):

        if from_natural:
            self.numbers = self.from_natural(number)
        else:
            numbers = [int(c) for c in str(number)]
            if not self.check(numbers):
                raise ValueError(f'number not valid: {numbers}')
            self.numbers = numbers
    
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

class IncrementalBaseNumber(IntermediateNumber):

    def __init__(self, numbers: int, from_natural: bool = False):
        super(IncrementalBaseNumber, self).__init__(numbers, from_natural)

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

    def add(self, rhs: IncrementalBaseNumber):
        return IncrementalBaseNumber(self.to_natural() + rhs.to_natural(), True)
    
    def sub(self, rhs: IncrementalBaseNumber):
        return IncrementalBaseNumber(self.to_natural() - rhs.to_natural(), True)


class DecrementalBaseNumber(IntermediateNumber):

    digits: int

    def __init__(self, numbers: int, digits = 9, from_natural: bool = False):
        self.digits = digits
        super(DecrementalBaseNumber, self).__init__(numbers, from_natural)

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

    def add(self, rhs: DecrementalBaseNumber):
        return DecrementalBaseNumber(self.to_natural() + rhs.to_natural(), self.digits, True)
    
    def sub(self, rhs: DecrementalBaseNumber):
        return DecrementalBaseNumber(self.to_natural() - rhs.to_natural(), self.digits, True)


if __name__ == '__main__':
    a = IncrementalBaseNumber(279905, True)
    b = IncrementalBaseNumber(2020, True)
    print(a, b)
    print(a.to_natural(), b.to_natural())
    print(a + b, a - b)
    a = DecrementalBaseNumber(1222447, 8)
    b = DecrementalBaseNumber(2020, 8, True)
    print(a, b)
    print(a.to_natural(), b.to_natural())
    print(a + b, a - b)
