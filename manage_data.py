# === Import required libraries ===
import requests  # Used to make HTTP requests to the Stellar Horizon API
from stellar_sdk import Server, Keypair, TransactionBuilder, Network  # Core classes from the Stellar SDK
from stellar_sdk.operation import ManageData  # Used to perform the ManageData operation on Stellar
import base64  # Library for encoding and decoding data in Base64 format


# === Function to add data to a Stellar account ===
def add_data_to_account(account_id: str, data_name: str, data_value: str):
    """
    Adds (or updates) a key-value pair on a Stellar account using the ManageData operation.
    """
    # Define the secret key of the source account — required to sign and authorize the transaction
    secret = "SDMT7RM5DI6K5LKMD4OU6VZDFOU66RJ4W3L7KRNIHK3KZEV4OQUH3UFB" # change for your secret key
    keypair = Keypair.from_secret(secret)  # Create the keypair (public/private) from the secret key

    # Connect to the Stellar Testnet Horizon server
    # Horizon is the REST API layer used to interact with the Stellar blockchain
    server = Server("https://horizon-testnet.stellar.org")

    # Create a ManageData operation — used to attach arbitrary data to an account
    manage_data_op = ManageData(
        data_name=data_name,         # Key name for the data entry
        data_value=data_value,       # Value to be stored under this key
        source=keypair.public_key    # Source account that authorizes this operation
    )
    
    # Load the target account from the Stellar blockchain using its public key
    account = server.load_account(account_id)

    # Build the transaction that includes the ManageData operation
    transaction = (
        TransactionBuilder(
            source_account=account,  # The account that will pay for the transaction
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE  # Identifies we’re using the Testnet
        )
        .append_operation(manage_data_op)  # Attach the ManageData operation
        .build()  # Finalize (build) the transaction
    )

    # Sign the transaction with the source account's private key
    # Signing proves that the account owner authorizes this transaction
    transaction.sign(keypair)

    # Submit the signed transaction to the Stellar network via Horizon
    response = server.submit_transaction(transaction)

    # Print the transaction response — includes status and transaction hash
    print("Transaction submitted:", response)


# === Function to query data stored on a Stellar account ===
def query_data(account_id: str, data_name: str):
    """
    Queries the data stored under a specific key on a Stellar account.
    """
    # Construct the Horizon API URL for the specific data key
    url = f"https://horizon-testnet.stellar.org/accounts/{account_id}/data/{data_name}"
    
    # Send a GET request to the Horizon server
    response = requests.get(url)
    
    # Check if the request was successful (HTTP 200)
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response into a Python dictionary
        print(f"Data found: {data}")
    else:
        # Print error details if the request failed
        print(f"Error fetching data: {response.status_code}, {response.text}")


# === Example usage ===
account_id = "GAQ3DMYZ37GE5YIYTN75N7KONOCUTOJTCSUZMIZ7SQ4L466GO77I65DM"  # Destination account ID
data_name = "example_key"  # Data key name
data_value = "example_value"  # Data value to be stored


# === Main script entry point ===
if __name__ == "__main__":
    # Add data to the Stellar account
    add_data_to_account(account_id, data_name, data_value)
    
    # Query the same data back from the account
    query_data(account_id, data_name)

    # Example of decoding a Base64 value returned by Horizon
    encoded_value = "ZXhhbXBsZV92YWx1ZQ=="  # Base64-encoded version of "example_value"
    decoded_value = base64.b64decode(encoded_value).decode('utf-8')  # Decode the Base64 string
    print(decoded_value)
