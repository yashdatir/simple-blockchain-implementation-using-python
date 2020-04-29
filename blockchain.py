from block import Block
class Blockchain:
    """
    Blockchain is a public ledger of Transactions.
    Implemented as a list of blocks - data sets of transactions
    """
    def __init__(self):
        self.chain = []

    def add_block(self, data):
        self.chain.append(Block(data))

    def __repr__(self):
        return f'{self.chain}'

def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')
    print (blockchain)
    print(f'block.py __name__: {__name__}')

if __name__ == '__main__':
    main()