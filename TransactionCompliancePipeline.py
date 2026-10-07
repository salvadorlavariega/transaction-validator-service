from typing import List
from TransactionValidationHandler import TransactionValidationHandler
from Transaction import Transaction
from ValidationContext import ValidationContext

class TransactionCompliancePipeline:
    def __init__(self, validation_rules: List[TransactionValidationHandler]):
        self._chain = None
        self._assemble_chain(validation_rules)
    def _assemble_chain(self, validation_rules: List[TransactionValidationHandler]):
        if not validation_rules:
            raise ValueError("Validation rules list cannot be empty.")
        self._chain = validation_rules[0]
        current_handler = self._chain
        for rule in validation_rules[1:]:
            current_handler.next_handler = rule
            current_handler = rule

    def validate_transaction(self, transaction: Transaction) -> ValidationContext:
        context = ValidationContext()
        self._chain.handle(transaction, context)
        return context