# Cryptocurrency Wallet
################################################################################

# This file contains the Ethereum transaction functions that you have created throughout this module’s lessons. By using import statements, you will integrate this `crypto_wallet.py` Python script into the Fintech Finder interface program that is found in the `fintech_finder.py` file.

################################################################################
#EH: Imports libraries and dependencies
import os
import requests
from dotenv import load_dotenv
load_dotenv()
from bip44 import Wallet
from web3 import Account
from web3 import middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy

################################################################################
#EH: Wallet functionality

def generate_account():
    """Create a digital wallet and Ethereum account from a mnemonic seed phrase."""
    #EH: Fetch mnemonic from environment variable.
    mnemonic = os.getenv("MNEMONIC")

    #EH: Create Wallet Object
    wallet = Wallet(mnemonic)

    #EH: Derive Ethereum Private Key
    private, public = wallet.derive_account("eth")

    #EH: Convert private key into an Ethereum account
    account = Account.privateKeyToAccount(private)
    
    #EH: return the Ethereum account string
    return account

#EH: get Ethereum account balance
def get_balance(w3, address):
    """Using an Ethereum account address access the balance of Ether"""
    # EH: Get balance of address in Wei
    wei_balance = w3.eth.get_balance(address)

    #EH: Convert Wei value to ether
    ether = w3.fromWei(wei_balance, "ether")

    #EH: Return the value in ether
    return ether

#EH:  Send transaction function
def send_transaction(w3, account, to, wage):
    """Send an authorized transaction to the Ganache blockchain."""
    #EH: Set gas price strategy
    w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

    #EH: Convert eth amount to Wei
    value = w3.toWei(wage, "ether")

    #EH: Calculate gas estimate
    gasEstimate = w3.eth.estimateGas({"to": to, "from": account.address, "value": value})

    #EH: Construct a raw transaction
    raw_tx = {
        "to": to,
        "from": account.address,
        "value": value,
        "gas": gasEstimate,
        "gasPrice": 0,
        "nonce": w3.eth.getTransactionCount(account.address)
    }

    #EH: Sign the raw transaction with ethereum account
    signed_tx = account.signTransaction(raw_tx)

    #EH: Send the signed transactions
    return w3.eth.sendRawTransaction(signed_tx.rawTransaction)
