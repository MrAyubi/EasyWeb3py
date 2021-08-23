from web3 import Web3

import sign_transaction



class ERC20Functions():
    erc20_abi = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"src","type":"address"},{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"guy","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Withdrawal","type":"event"}]'
    web3 = Web3(Web3.HTTPProvider("https://kovan.infura.io/v3/637fda9528f348d29733ddd54fd2e2c7"))

    def __init__(self, user_address, token_address):
        self.token_address = token_address
        self.user_address = user_address
        self.contract = self.web3.eth.contract(address=token_address, abi=self.erc20_abi)

    def approve_internal(self, spender_address, amount, user_private_key):
        transaction = self.contract.functions.approve(spender_address, amount)
        transaction_data = {
            'user_address': self.user_address,
            'user_private_key': user_private_key,
            'transaction': transaction
        }
        return transaction_data

    def transaction_signer(self, transaction, private_key):
        signed_transaction = self.web3.eth.account.signTransaction(transaction, private_key)
        return signed_transaction

    def get_transaction_receipt(self, signed_transaction):
        output = self.web3.eth.sendRawTransaction(signed_transaction.rawTransaction)
        transaction_receipt = self.web3.eth.wait_for_transaction_receipt(output)
        return transaction_receipt

    def approve(self, spender_address, amount, user_private_key):
        transaction = self.approve_internal(self.user_address, spender_address, amount)
        signed_transaction = self.transaction_signer(transaction, user_private_key)
        return self.get_transaction_receipt(signed_transaction)

    def allowance(self, spender_address):
        return self.contract.functions.allowance(self.user_address, spender_address).call()

    def transfer_internal(self, recipient, amount):
        gas = 81000
        transaction = self.contract.functions.transfer(recipient, amount).buildTransaction({
            'from': self.user_address,
            'nonce': self.nonce,
            'gas': gas,
            'gasPrice': self.estimate_gas_price()
        })
        gas = self.estimate_gas(transaction)
        return transaction

    def transfer(self, recipient, amount, user_private_key):

        transaction = self.transfer_internal(recipient, amount)
        signed_transaction = self.transaction_signer(transaction, user_private_key)
        return self.get_transaction_receipt(signed_transaction)

    def transfer_from_internal(self, sender, recipient, amount):
        gas = 81000
        transaction = self.contract.functions.transferFrom(sender, recipient, amount).buildTransaction({
            'from': self.user_address,
            'nonce': self.nonce,
            'gas': gas,
            'gasPrice': self.estimate_gas_price()
        })
        gas = self.estimate_gas(transaction)
        return transaction

    def transfer_from(self, sender, recipient, amount, user_private_key):
        transaction = self.transfer_from_internal(sender, recipient, amount)
        signed_transaction = self.transaction_signer(transaction, user_private_key)
        return self.get_transaction_receipt(signed_transaction)

    def estimate_gas(self, transaction):
        return self.web3.eth.estimate_gas(transaction)
    def estimate_gas_price(self):
        return self.web3.eth.web3.eth.gas_price

m = ERC20Functions("0x48ce090bE4B92434D1cA0072AB48B0C644747491", "0x710084B71AD459C412f0fDb6722e9742C3c5b52e")
# c = m.approve("0x92bc291Dfcff59caB6179b07EdDDD43d15A6ACfa", 300, "7dfe316f2280bb1477f217ac85eadedd01508686205139772cada931196e87f1")
t = m.transfer("0xfcFf94b5387438001a71932d7a0b71906254dc22", 10, "7dfe316f2280bb1477f217ac85eadedd01508686205139772cada931196e87f1")
# d= m.allowance()
print(t)