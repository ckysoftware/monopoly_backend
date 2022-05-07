from dataclasses import dataclass


@dataclass(kw_only=True, slots=True)
class Cash:
    balance: int

    def add(self, amount):
        self.balance += amount

    def sub(self, amount):
        self.balance -= amount
