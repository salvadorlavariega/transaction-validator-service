from TransactionValidationHandler import TransactionValidationHandler

from typing import Optional

class AmountLimitValidationRule(TransactionValidationHandler):
    def __init__(self, max_amount:float, next_handler: Optional[TransactionValidationHandler] = None):
        super().__init__(next_handler)
        self.max_amount = max_amount

    def _validate(self, transaction, context):
        if transaction.amount < 0:
            raise ValueError("Transaction amount must be greater than zero.")
        if transaction.amount > self.max_amount:
            raise ValueError(f"Transaction amount exceeds the maximum limit of {self.max_amount}. \nit needs to be approved by a manager.")

class CurrencyValidationRule(TransactionValidationHandler):
    def __init__(self, allowed_currencies: list, next_handler: Optional[TransactionValidationHandler] = None):
        super().__init__(next_handler)
        self.allowed_currencies = allowed_currencies

    def _validate(self, transaction, context):
        if transaction.currency not in self.allowed_currencies:
            raise ValueError(f"Currency {transaction.currency} is not allowed. Allowed currencies are: {', '.join(self.allowed_currencies)}.")


class CustomerStatusValidationRule(TransactionValidationHandler):
    def __init__(self, inactive_customer_ids: list, next_handler: Optional[TransactionValidationHandler] = None):
        super().__init__(next_handler)
        self.inactive_customer_ids = inactive_customer_ids

    def _validate(self, transaction, context):
        if transaction.customerId in self.inactive_customer_ids:
            raise ValueError(f"Customer {transaction.customerId} is inactive and cannot perform transactions.")

class AccountStatusValidationRule(TransactionValidationHandler):
    def __init__(self, blocked_accounts: list, next_handler: Optional[TransactionValidationHandler] = None):
        super().__init__(next_handler)
        self.blocked_accounts = blocked_accounts
    def _validate(self, transaction, context):
        if transaction.accountId in self.blocked_accounts:
            raise ValueError(f"Account {transaction.accountId} is blocked and cannot perform transactions.")    