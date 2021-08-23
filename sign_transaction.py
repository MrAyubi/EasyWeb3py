from web3 import Web3
from functools import wraps


class Transaction:
    web3 = Web3(Web3.HTTPProvider("https://kovan.infura.io/v3/637fda9528f348d29733ddd54fd2e2c7"))

    def get_nonce(self, user_address):
        return self.web3.eth.getTransactionCount(user_address)

    def transaction_builder(self, transaction_data):
        gas = 0
        raw_transaction = transaction_data['transaction'].buildTransaction({
            'from': transaction_data['user_address'],
            'nonce': self.get_nonce(transaction_data['user_address']),
            'gas': gas,
            'gasPrice': self.estimate_gas_price()
        })
        gas = self.estimate_gas(raw_transaction)
        return raw_transaction

    def sign_and_publish(self):
        def transaction_signer(transaction, private_key):
            signed_transaction = self.web3.eth.account.signTransaction(transaction, private_key)
            output = self.web3.eth.sendRawTransaction(signed_transaction.rawTransaction)
            transaction_receipt = self.web3.eth.wait_for_transaction_receipt(output)
            return transaction_receipt

        return transaction_signer

    def estimate_gas(self, transaction):
        return self.web3.eth.estimate_gas(transaction)

    def estimate_gas_price(self):
        return self.web3.eth.web3.eth.gas_price
