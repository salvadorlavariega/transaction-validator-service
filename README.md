# Ejercicio 3: Evaluación de reglas de negocio

## Enunciado

Tienes la siguiente función escrita por otro desarrollador. La función decide si una operación debe aprobarse o rechazarse.

```java
public boolean shouldApprove(Transaction tx) {
    if (tx.amount > 0) {
        if (tx.currency.equals("MXN") ||
            tx.currency.equals("USD")) {
            if (tx.customerActive) {
                if (!tx.blockedAccount) {
                    if (tx.amount < 100000) {
                        return true;
                    } else {
                        if (tx.hasManagerApproval) {
                            return true;
                        }
                    }
                }
            }
        }
    }
    return false;
}
```

## Objetivo

Refactorizar la función para que sea más clara, mantenible y fácil de probar.

## Reglas de negocio

Una transacción se aprueba si:

1. El monto es mayor a 0.
2. La moneda es MXN o USD.
3. El cliente está activo.
4. La cuenta no está bloqueada.
5. Si el monto es menor a 100,000, se aprueba.
6. Si el monto es igual o mayor a 100,000, requiere aprobación del manager.

## Patrón de diseño: Chain of Responsibility

## Desiciones Técnicas:

Este problema se me hizo muy familiar, he usado este patrón de diseño anteriormente para
resolver el sinfin de validaciones que se pueden desencadenar a la hora de validar un objeto,
en este caso una transaccion.
Si bien los IF anidados y uno dentro de otro caben perfectamente en una sola función
y mas compactado se vuelve un dolor de cabeza a la hora de testear, o cuando quieres cambiar el orden
de las validaciones o cuando quieres quitar o agregar una validación nueva.
Este código en Python no solo resuelve el problema, si no que implementa:

- Principio abierto/cerrado: Si se necesita agregar una validacion, se crea una nueva clase en
  Handlers.py sin afectar las existentes.
- Principio de responsabilidad única: Cada validacion vive en su propia clase,y tienen una sola razon para cambiar.
- Estrategia Fail-Fast: Si una regla falla, la ejecución se detiene evitando que las otras clases
  se inicialicen y hagan llamadas a servicios externos.
- Testeabilidad: No quiero imaginar el resultado de sonarqube diciendo que dentro del if anidado
  te falta probar un caso, o que ningun test entra al else del tercer IF, con Chain of Responsability puedes probar cada regla de forma aislada.

### Diagrama de clases

![Diagrama de clases](docs/diagrama-clases.png)

### Diagrama de secuencia (transacción válida)

![Diagrama de secuencia](docs/diagrama-secuencia.png)

### Dónde se detiene cada test (fail-fast)

| Test                                            | 1 · Monto | 2 · Moneda | 3 · Cliente      | 4 · Cuenta     | Resultado esperado             |
| ----------------------------------------------- | --------- | ---------- | ---------------- | -------------- | ------------------------------ |
| `test_should_approve_valid_transaction`         | ✅ 500    | ✅ USD     | ✅ cust_active   | ✅ acc_active  | `isValid = True`               |
| `test_should_fail_when_amount_exceeds_limit`    | ❌ 1500   | –          | –                | –              | `AmountLimitValidationRule`    |
| `test_should_fail_when_currency_is_not_allowed` | ✅ 500    | ❌ EUR     | –                | –              | `CurrencyValidationRule`       |
| `test_should_fail_when_customer_is_inactive`    | ✅ 500    | ✅ USD     | ❌ cust_inactive | –              | `CustomerStatusValidationRule` |
| `test_should_fail_when_account_is_blocked`      | ✅ 500    | ✅ MXN     | ✅ cust_active   | ❌ acc_blocked | `AccountStatusValidationRule`  |

`–` = la regla no se evalúa porque una anterior ya falló.

## Declaración del uso de documentación, herramientas externas o IA generativa.

    *Github Copilot* : Ocupé copilot como asistente de creación de código
    *Gemini* : Discutimos temas sobre Clean Code, Chain of Responsability y Arquitectura de Software
    *Claude Code* : Generación de diagramas de clases, diagrama de secuencia y matriz de pruebas visual.
