"""
This example shows how to parse XDR string into an XDR object.
But please note that if you need to parse a transaction envelope,
please refer to `parse_transaction_envelope.py`
"""

from stellar_sdk.xdr import TransactionResult

result_xdr = "AAAAAAAAAGQAAAAAAAAAAQAAAAAAAAADAAAAAAAAAAAAAAABAAAAAD/jlpBCTX53ogvts02Ryn5GjO6gx0qW3/3ARB+gOh/nAAAAADGRC/wAAAAAAAAAAU5VQwAAAAAAR74W04RzO2ryJo94Oi0FUs0KHIVQisRnpe9FWrqvumQAAAAAAEFWjwjgcksQkG4uAAAAAAAAAAAAAAAA"
print("XDR da transação:", result_xdr)
transaction_result = TransactionResult.from_xdr(result_xdr)
print("Objeto TransactionResult:", transaction_result)
fee_charged = transaction_result.fee_charged
print("Fee charged:", fee_charged)
result_code = transaction_result.result.code
print("Result code:", result_code)

if hasattr(transaction_result, 'ledger') and transaction_result.ledger:
    print("Ledger sequence:", transaction_result.ledger.sequence)
else:
    print("Ledger sequence não disponível")

if hasattr(transaction_result, 'extra_data'):
    print("Dados extras disponíveis:", transaction_result.extra_data)
else:
    print("Sem dados extras disponíveis")