"""
===============================================================================
Manage Data on the Stellar Blockchain + Parse Transaction XDR Results
===============================================================================

This script demonstrates how to:
1. Add arbitrary key-value data to a Stellar account using the ManageData operation.
2. Query and decode the stored data from the Stellar Testnet.
3. Parse the XDR (External Data Representation) result of a transaction using the Stellar SDK.

-------------------------------------------------------------------------------
Installation Guide
-------------------------------------------------------------------------------
Before running this example, install the required libraries:

    pip install stellar-sdk requests

-------------------------------------------------------------------------------
Description
-------------------------------------------------------------------------------
This code interacts with the Stellar blockchain to add and query arbitrary data
stored in a specific account. It uses:

- `requests`: to make HTTP requests (fetch account data from the Horizon API)
- `stellar_sdk`: for interacting with the Stellar network
    - `Server`: connects to the Horizon server (Testnet)
    - `Keypair`: manages public/private keys for transaction signing
    - `TransactionBuilder`: builds and signs transactions
    - `Network`: specifies the network passphrase (Testnet or Mainnet)
    - `ManageData`: creates operations that attach data to Stellar accounts

Documentation references:
- ManageData operation (SDK): https://stellar-sdk.readthedocs.io/en/latest/_modules/stellar_sdk/operation/manage_data.html
- Manage Data (Developers site): https://developers.stellar.org/docs/learn/fundamentals/transactions/list-of-operations#manage-data
- Stellar Expert (Explorer): https://stellar.expert/explorer/testnet
===============================================================================
"""

# === Import required libraries ===
import requests               # Used to make HTTP requests to the Stellar Horizon API
from stellar_sdk import (
    Server,
    Keypair,
    TransactionBuilder,
    Network
)                             # Core classes from the Stellar SDK
from stellar_sdk.operation import ManageData  # Used to perform the ManageData operation
from stellar_sdk.xdr import TransactionResult  # Used to parse XDR strings from Stellar transactions
import base64                 # Library for encoding and decoding Base64 data


# === Function to add data to a Stellar account ===
def add_data_to_account(account_id: str, data_name: str, data_value: str):
    """
    Adds (or updates) a key-value pair on a Stellar account using the ManageData operation.
    """

    # Define the secret key (private key) for signing transactions
    secret = "SDMT7RM5DI6K5LKMD4OU6VZDFOU66RJ4W3L7KRNIHK3KZEV4OQUH3UFB"  # Replace with your own secret key
    keypair = Keypair.from_secret(secret)

    # Connect to the Stellar Testnet via Horizon
    server = Server("https://horizon-testnet.stellar.org")

    # Create a ManageData operation
    manage_data_op = ManageData(
        data_name=data_name,
        data_value=data_value,
        source=keypair.public_key
    )

    # Load the account from the blockchain
    account = server.load_account(account_id)

    # Build the transaction
    transaction = (
        TransactionBuilder(
            source_account=account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE
        )
        .append_operation(manage_data_op)
        .build()
    )

    # Sign the transaction with the private key
    transaction.sign(keypair)

    # Submit the transaction to the Stellar network
    response = server.submit_transaction(transaction)
    print("Transaction submitted:", response)

    # Return the transaction result XDR for later parsing
    return response.get("result_xdr", None)


# === Function to query data stored on a Stellar account ===
def query_data(account_id: str, data_name: str):
    """
    Queries the data stored under a specific key on a Stellar account.
    """
    url = f"https://horizon-testnet.stellar.org/accounts/{account_id}/data/{data_name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f"Data found: {data}")
        # Decode Base64 data value
        decoded_value = base64.b64decode(data["value"]).decode("utf-8")
        print(f"Decoded value: {decoded_value}")
        return decoded_value
    else:
        print(f"Error fetching data: {response.status_code}, {response.text}")
        return None


# === Function to parse an XDR transaction result ===
def parse_xdr_result(result_xdr: str):
    """
    Parses and displays information from a Stellar transaction XDR string.
    """
    print("\n--- Parsing Transaction XDR ---")
    print("Transaction XDR:", result_xdr)

    # Convert XDR string to a TransactionResult object
    transaction_result = TransactionResult.from_xdr(result_xdr)

    # Display parsed details
    print("TransactionResult object:", transaction_result)
    print("Fee charged:", transaction_result.fee_charged)
    print("Result code:", transaction_result.result.code)

    # Optional fields
    if hasattr(transaction_result, 'ledger') and transaction_result.ledger:
        print("Ledger sequence:", transaction_result.ledger.sequence)
    else:
        print("Ledger sequence not available")

    if hasattr(transaction_result, 'extra_data'):
        print("Extra data available:", transaction_result.extra_data)
    else:
        print("No extra data available")


# === Example usage ===
if __name__ == "__main__":
    account_id = "GAQ3DMYZ37GE5YIYTN75N7KONOCUTOJTCSUZMIZ7SQ4L466GO77I65DM"
    data_name = "example_key"
    data_value = "example_value"

    # Add data to account
    result_xdr = add_data_to_account(account_id, data_name, data_value)

    # Query stored data
    query_data(account_id, data_name)

    # Parse XDR result (if available)
    if result_xdr:
        parse_xdr_result(result_xdr)

"""
===============================================================================
Expected Output Example
===============================================================================

UserWarning: It looks like you haven't set a TimeBounds for the transaction.
We strongly recommend setting it to prevent timeout issues.

Transaction submitted:
{
  'successful': True,
  'hash': 'ba14ef7c8f2c6150436bcac7abba8e38d51e83ccd093dec4f5ad0862ac308206',
  'ledger': 1106419,
  'result_xdr': 'AAAAAAAAAGQAAAAAAAAAAQAAAAAAAAAKAAAAAAAAAAA='
}

Data found:
{'value': 'ZXhhbXBsZV92YWx1ZQ=='}
Decoded value: example_value

--- Parsing Transaction XDR ---
Transaction XDR: AAAAAAAAAGQAAAAAAAAAAQAAAAAAAAAKAAAAAAAAAAA=
Fee charged: 100
Result code: txSUCCESS
Ledger sequence not available
No extra data available

===============================================================================
Explanation of Encoded Data
===============================================================================

The Base64 value "ZXhhbXBsZV92YWx1ZQ==" corresponds to the string "example_value".
This is how Horizon encodes arbitrary binary data attached to Stellar accounts.

Example query URL:
https://horizon-testnet.stellar.org/accounts/GAQ3DMYZ37GE5YIYTN75N7KONOCUTOJTCSUZMIZ7SQ4L466GO77I65DM/data/example_key
===============================================================================
"""
