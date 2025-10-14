# Stellar Data Management - Usage Example

This repository contains a simple example of how to interact with the **Stellar** network using the **Stellar SDK** to add and query data on Stellar accounts. The code uses the **Testnet** network to perform operations without the risk of spending real tokens.

## Features

The script performs two main operations:

1. **Add Data to a Stellar Account**:  
   - The `add_data_to_account` function allows you to store arbitrary data (key/value) associated with a key inside a Stellar account.
   
2. **Query Stored Data from a Stellar Account**:  
   - The `query_data` function allows you to query data stored in a Stellar account using the associated key.

3. **manage_data.py**:  
   - Connects to the Stellar Testnet and performs two key operations:
   1. Adds a key–value pair to a Stellar account (ManageData operation).
   2. Retrieves that data back from the account.
   You can edit the script and replace the account’s secret key and public key with your own from the Stellar Testnet.
  
4. **xdr.py**:  
   - Demonstrates how to parse an XDR (External Data Representation) string returned by a Stellar transaction, convert it into a Python object, and inspect its fields.
   
## Requirements

Make sure your development environment is set up with the following dependencies:

- **Python 3.x**  
- **requests**: Used to make HTTP requests.  
- **stellar-sdk**: The official Stellar library for interacting with the Stellar network.  

You can install the required dependencies using `pip`:

```bash
pip install requests stellar-sdk
```

