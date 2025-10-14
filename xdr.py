"""
This example demonstrates how to parse an XDR string into an XDR object.
Note: if you need to parse a transaction envelope,
refer to the file `parse_transaction_envelope.py`.
"""

from stellar_sdk.xdr import TransactionResult

# XDR string representing the result of a Stellar transaction
result_xdr = "AAAAAAAAAGQAAAAAAAAAAQAAAAAAAAADAAAAAAAAAAAAAAABAAAAAD/jlpBCTX53ogvts02Ryn5GjO6gx0qW3/3ARB+gOh/nAAAAADGRC/wAAAAAAAAAAU5VQwAAAAAAR74W04RzO2ryJo94Oi0FUs0KHIVQisRnpe9FWrqvumQAAAAAAEFWjwjgcksQkG4uAAAAAAAAAAAAAAAA"

print("Transaction XDR:", result_xdr)

# Parse the XDR string into a TransactionResult object
transaction_result = TransactionResult.from_xdr(result_xdr)

# Display the parsed TransactionResult object
print("TransactionResult object:", transaction_result)

# Extract and display the transaction fee charged
fee_charged = transaction_result.fee_charged
print("Fee charged:", fee_charged)

# Extract and display the transaction result code
result_code = transaction_result.result.code
print("Result code:", result_code)

# Check if the transaction result includes a ledger sequence number
if hasattr(transaction_result, 'ledger') and transaction_result.ledger:
    print("Ledger sequence:", transaction_result.ledger.sequence)
else:
    print("Ledger sequence not available")

# Check if extra data fields exist in the transaction result
if hasattr(transaction_result, 'extra_data'):
    print("Extra data available:", transaction_result.extra_data)
else:
    print("No extra data available")
