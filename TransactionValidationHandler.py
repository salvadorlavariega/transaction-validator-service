from abc import ABC, abstractmethod
from typing import Optional
from Transaction import Transaction
from ValidationContext import ValidationContext

class TransactionValidationHandler(ABC):
    def __init__(self, next_handler: Optional['TransactionValidationHandler'] = None):
        self.next_handler = next_handler

    @abstractmethod
    def _validate(self, transaction: Transaction, context: ValidationContext) -> None:
        pass
    def handle(self, transaction: Transaction, context: ValidationContext) -> None:
        if not context.isValid:
            return  # fail firsft, no need to continue
        try:
            self._validate(transaction, context)
        except Exception as e:
            context.isValid = False
            context.error_message = str(e)
            context.failed_rule = self.__class__.__name__
            return
        if context.isValid and self.next_handler:
            self.next_handler.handle(transaction, context)
