import unittest

from TransactionCompliancePipeline import TransactionCompliancePipeline
from Handlers import (
    AmountLimitValidationRule, 
    CurrencyValidationRule,
    CustomerStatusValidationRule,
    AccountStatusValidationRule
)
from Transaction import Transaction

class TestTransactionCompliancePipeline(unittest.TestCase):

    def setUp(self):
        """Configuración base para los tests (Fixture)."""
        self.configured_rules = [
            AmountLimitValidationRule(max_amount=1000.0),
            CurrencyValidationRule(allowed_currencies=["USD", "MXN"]),
            CustomerStatusValidationRule(inactive_customer_ids=["cust_inactive"]),
            AccountStatusValidationRule(blocked_accounts=["acc_blocked"])
        ]
        self.pipeline = TransactionCompliancePipeline(self.configured_rules)

    def test_should_approve_valid_transaction(self):
        """Caso 1: Transacción completamente válida que pasa todas las reglas."""
        tx = Transaction(
            transaction_id="tx_001", 
            amount=500.0, 
            currency="USD", 
            customerId="cust_active", 
            accountId="acc_active"
        )
        
        result = self.pipeline.validate_transaction(tx)
        
        self.assertTrue(result.isValid)
        self.assertIsNone(result.error_message)
        self.assertIsNone(result.failed_rule)

    def test_should_fail_when_amount_exceeds_limit(self):
        """Caso 2: Falla en la primera regla (Límite de monto). Comprueba Fail-Fast."""
        tx = Transaction(
            transaction_id="tx_002", 
            amount=1500.0,  # Excede el límite de 1000.0
            currency="INVALID_CURRENCY", # Aunque esto es inválido, no debe evaluarse por Fail-Fast
            customerId="cust_inactive",  # Tampoco importa, se detiene antes
            accountId="acc_blocked"
        )
        
        result = self.pipeline.validate_transaction(tx)
        
        self.assertFalse(result.isValid)
        self.assertEqual(result.failed_rule, "AmountLimitValidationRule")
        self.assertIn("amount", result.error_message.lower())

    def test_should_fail_when_currency_is_not_allowed(self):
        """Caso 3: Pasa el monto pero falla en la segunda regla (Moneda)."""
        tx = Transaction(
            transaction_id="tx_003", 
            amount=500.0, 
            currency="EUR",  # Moneda no permitida
            customerId="cust_active", 
            accountId="acc_active"
        )
        
        result = self.pipeline.validate_transaction(tx)
        
        self.assertFalse(result.isValid)
        self.assertEqual(result.failed_rule, "CurrencyValidationRule")

    def test_should_fail_when_customer_is_inactive(self):
        """Caso 4: Pasa monto y moneda, pero falla en la tercera regla (Cliente inactivo)."""
        tx = Transaction(
            transaction_id="tx_004", 
            amount=500.0, 
            currency="USD", 
            customerId="cust_inactive",  # Cliente en lista negra
            accountId="acc_active"
        )
        
        result = self.pipeline.validate_transaction(tx)
        
        self.assertFalse(result.isValid)
        self.assertEqual(result.failed_rule, "CustomerStatusValidationRule")

    def test_should_fail_when_account_is_blocked(self):
        """Caso 5: Llega hasta el final de la cadena y falla en la última regla (Cuenta bloqueada)."""
        tx = Transaction(
            transaction_id="tx_005", 
            amount=500.0, 
            currency="MXN", 
            customerId="cust_active", 
            accountId="acc_blocked"  # Cuenta bloqueada
        )
        
        result = self.pipeline.validate_transaction(tx)
        
        self.assertFalse(result.isValid)
        self.assertEqual(result.failed_rule, "AccountStatusValidationRule")


if __name__ == "__main__":
    unittest.main()