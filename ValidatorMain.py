from TransactionCompliancePipeline import TransactionCompliancePipeline
from Handlers import (AmountLimitValidationRule, 
                      CurrencyValidationRule,
                      CustomerStatusValidationRule,
                      AccountStatusValidationRule)
from Transaction import Transaction
if __name__ == "__main__":

    #Please add more rules to the configured_rules list as needed. The order of rules in the list determines the order of validation.
    configured_rules = [
        AmountLimitValidationRule(max_amount=1000.0),
        CurrencyValidationRule(allowed_currencies=["USD", "MXN"]),
        CustomerStatusValidationRule(inactive_customer_ids=["cust456", "cust789"]),
        AccountStatusValidationRule(blocked_accounts=["acc456", "acc789"])
    ]

    pipeline = TransactionCompliancePipeline(configured_rules)

    tx = Transaction(transaction_id="tx123", amount=1000.0, currency="dd", customerId="cust123", accountId="acc123")
    result = pipeline.validate_transaction(tx)
    if result.isValid:
        print("Transaction is valid.")
    else:
        print(f"Transaction is invalid. Error: {result.error_message}, Failed Rule: {result.failed_rule}")