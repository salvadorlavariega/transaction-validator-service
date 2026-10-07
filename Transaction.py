from dataclasses import dataclass

@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    amount: float
    currency: str
    customerId: str
    accountId: str