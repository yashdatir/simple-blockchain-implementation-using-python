from backend.blockchain.block import Block
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


def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')
    print(blockchain)

if __name__ == '__main__':
    main()