from web3 import Web3
import time

# Connect to the Base network via RPC
rpc_url = "https://mainnet.base.org"
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Check if the connection is successful
if not web3.is_connected():
    raise Exception("Failed to connect to Base network")

# Constants
CHAIN_ID = 8453  # Base Chain ID
TO_ADDRESS = "0xEA8D2079CF3D5aD4766213aAE29E59C091BF0E28"  # Recipient Address

# Function to send 0 ETH transaction
def send_0_eth_transaction(private_key, to_address, repetitions):
    # Get the sender address from the private key
    sender_address = web3.eth.account.from_key(private_key).address

    # Loop for the specified number of repetitions
    for i in range(repetitions):
        # Get the current transaction count (nonce)
        nonce = web3.eth.get_transaction_count(sender_address)

        # Fetch the current gas price from the network and increase it by 10%
        gas_price = web3.eth.gas_price * 1.1  # Increase gas price by 10%

        # Estimate the required gas limit for the transaction
        estimated_gas_limit = web3.eth.estimate_gas({
            'from': sender_address,
            'to': to_address,
            'value': 0
        })

        # Add some buffer (e.g., 20%) to the estimated gas limit
        gas_limit = int(estimated_gas_limit * 1.2)

        # Create the transaction dictionary
        tx = {
            'nonce': nonce,
            'to': to_address,
            'value': 0,  # 0 ETH
            'gas': gas_limit,  # Estimated gas limit with buffer
            'gasPrice': int(gas_price),  # Apply the increased gas price
            'chainId': CHAIN_ID
        }

        # Sign the transaction with the private key
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)

        # Send the transaction
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        # Print the transaction hash
        print(f"Transaction {i+1}/{repetitions} sent! Tx Hash: {web3.to_hex(tx_hash)}")

        # Wait a few seconds between transactions to avoid nonce issues
        time.sleep(5)

    # Print task completion message
    print("Task done!")

# Main script
if __name__ == "__main__":
    # Get the private key from the user (ensure you keep this secure!)
    private_key = input("Enter your private key: ")

    # Ask how many times to perform the transaction
    repetitions = int(input("How many times do you want to perform the transaction? "))

    # Call the function to send transactions
    send_0_eth_transaction(private_key, TO_ADDRESS, repetitions)
