from dataclasses import dataclass


@dataclass
class Cash:
    balance: int

    def add(self, amount):
        self.balance += amount
    
    def minus(self, amount):
        self.balance -= amount
        