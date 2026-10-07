## Arquitectura: Chain of Responsibility

### Diagrama de clases

![Diagrama de clases](docs/diagrama-clases.png)

### Diagrama de secuencia (transacción válida)

![Diagrama de secuencia](docs/diagrama-secuencia.png)

### Dónde se detiene cada test (fail-fast)

| Test | 1 · Monto | 2 · Moneda | 3 · Cliente | 4 · Cuenta | Resultado esperado |
|---|---|---|---|---|---|
| `test_should_approve_valid_transaction` | ✅ 500 | ✅ USD | ✅ cust_active | ✅ acc_active | `isValid = True` |
| `test_should_fail_when_amount_exceeds_limit` | ❌ 1500 | – | – | – | `AmountLimitValidationRule` |
| `test_should_fail_when_currency_is_not_allowed` | ✅ 500 | ❌ EUR | – | – | `CurrencyValidationRule` |
| `test_should_fail_when_customer_is_inactive` | ✅ 500 | ✅ USD | ❌ cust_inactive | – | `CustomerStatusValidationRule` |
| `test_should_fail_when_account_is_blocked` | ✅ 500 | ✅ MXN | ✅ cust_active | ❌ acc_blocked | `AccountStatusValidationRule` |

`–` = la regla no se evalúa porque una anterior ya falló.
