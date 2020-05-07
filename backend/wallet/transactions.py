import uuid
import time

from backend.wallet.wallet import Wallet

class Transaction:
    """
    Document an exchange in currency from sender to one or more reciepients
    """
    def __init__(self, sender_wallet=None, reciepient=None, amount=None, id=None, output=None, input=None):
        self.id = id or str(uuid.uuid4())[0:8]
        self.output = output or self.create_output(sender_wallet, reciepient, amount)
        self.input = input or self.create_input(sender_wallet, self.output)

    def create_output(self, sender_wallet, reciepient, amount):
        """
        Structure the output data for the transaction
        """
        if amount > sender_wallet.balance:
            raise Exception('Amount exceeds the Balance')

        output = {}
        output[reciepient] = amount
        output[sender_wallet.address] = sender_wallet.balance - amount
        return output

    def create_input(self, sender_wallet, output):
        """
        Structure the input data for the transaction
        Sign the transaction and include the sender's public key address
        """
        return {
            'timestamp': time.time_ns(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(output)
        }

    def update(self, sender_wallet, reciepient, amount):
        """
        Update the transaction with an existing or new reciepients
        """
        if amount > self.output[sender_wallet.address]:
            raise Exception('Amount exceeds balance')

        if reciepient in self.output:
            self.output[reciepient] = self.output[reciepient] + amount
        
        else:
            self.output[reciepient] = amount

        self.output[sender_wallet.address] = self.output[sender_wallet.address] - amount

        self.input = self.create_input(sender_wallet, self.output)

    def to_json(self):
        """
        Serialize a transaction
        """
        return self.__dict__

    @staticmethod
    def from_json(transaction_json):
        """
        Deserialize a transaction's json representation back into a
        Transaction instance
        """
        return Transaction(**transaction_json)

    @staticmethod
    def transaction_is_valid(transaction):
        """
        Validate a transaction,
         raise an exception for invalid transaction
        """
        output_total = sum(transaction.output.values())
        if transaction.input['amount'] != output_total:
            raise Exception('Invalid transaction output values')

        if not Wallet.verify(transaction.input['public_key'], transaction.output, transaction.input['signature']):
            raise Exception('Invalid signature')


def main():
    transaction = Transaction(Wallet(),'reciepient',13)
    print(f'transaction: {transaction.__dict__}')
    transaction_json = transaction.to_json()
    restored_transaction = Transaction.from_json(transaction_json)
    print(f'transaction: {restored_transaction.__dict__}')

if __name__ == '__main__':
    main()
