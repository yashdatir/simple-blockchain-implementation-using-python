from backend.blockchain.block import Block
from backend.wallet.wallet import Wallet
from backend.wallet.transactions import Transaction
from backend.config import MINING_REWARD, MINING_REWARD_INPUT

class Blockchain:
    """
    Blockchain is a public ledger of Transactions.
    Implemented as a list of blocks - data sets of transactions
    """
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f'{self.chain}'

    def replace_chain(self, chain):
        """
        Replace the local chain with incoming one if the followinf applies:
         - The incoming chain must be longer than local one
         - The incoming chain must be formatted properly
        """
        if len(chain) <= len(self.chain):
            raise Exception('Cannot Replace! Incoming chain must be longer')

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot Replace! The chain is invalid: {e}') 

        self.chain = chain

    def to_json(self):
        """
        Serialize a blockchain into a list of blocks
        """
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json):
        """
        Deserialize a list of serialized blocks into a blockchain instance
        The result will contain the chain list of block instance
        """
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda block_json: Block.from_json(block_json), chain_json))
        return blockchain
    
    @staticmethod
    def is_valid_chain(chain):
        """
        Validate the incoming chain
        Enforce the following set of rules: 
         - The chain must start with a genesis block
         - blocks must be formatted correctly
        """

        if chain[0] != Block.genesis():
            raise Exception('The genesis block must be correct')

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)

        Blockchain.is_valid_transaction_chain(chain)
    
    @staticmethod
    def is_valid_transaction_chain(chain):
        """
        Enforce the rules of a chain composed of blocks of transactions
         - each transaction must only appear once in the chain
         - There can be only one mining reward per block
         - Each transaction must be valid
        """
        transaction_ids = set()
        for i in range(len(chain)): 
            block = chain[i]
            has_mining_reward = False

            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)

                if transaction.id in transaction_ids:
                    raise Exception(f'Transaction: {transaction.id} is not unique')

                transaction_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception(f'There can be only one mining reward per block check this block: {block.hash}')
                    has_mining_reward = True

                else:
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]
                    historic_balance = Wallet.calculate_balance(historic_blockchain, transaction.input['address'])
                    if historic_balance != transaction.input['amount']:
                        raise Exception(f'Transaction {transaction.id} has '\
                            'invalid input amount')
                    Transaction.transaction_is_valid(transaction)

def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')
    print(blockchain)

if __name__ == '__main__':
    main()