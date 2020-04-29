import time
from crypto_hash import crypto_hash

class Block:
    """
    Block : is a unit of storage
    store transactions in a blockchain that supports a cryptocurrency
    """
    def __init__(self, time_stamp, last_hash, hash, data):
        self.time_stamp = time_stamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data


    def __repr__(self):
        return (
            'Block('
            f'Timestamp: {self.time_stamp}'
            f', Last_hash: {self.last_hash}'
            f', Hash: {self.hash}'
            f', Data: {self.data})'
            )

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the last block given and data
        """
        time_stamp = time.time_ns()
        last_hash = last_block.hash
        hash = crypto_hash(time_stamp, last_hash, data)
        return Block(time_stamp, last_hash, hash, data)

    @staticmethod
    def genesis():
        """
        This part generates the genesis block
        """
        return Block(1,'genesis_last_hash','genesis_hash',[])


def main():
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block,'y')
    print(block)

if __name__ == '__main__':
    main()