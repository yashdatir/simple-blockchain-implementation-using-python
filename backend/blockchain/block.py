import time
from backend.util.crypto_hash import crypto_hash
from backend.util.hex_to_bin import hex_to_bin
from backend.config import MINE_RATE

GENESIS_DATA = {
    'time_stamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}
class Block:
    """
    Block : is a unit of storage
    store transactions in a blockchain that supports a cryptocurrency
    """
    def __init__(self, time_stamp, last_hash, hash, data, difficulty, nonce):
        self.time_stamp = time_stamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce


    def __repr__(self):
        return (
            '\nBlock('
            f'Timestamp: {self.time_stamp}'
            f', Last_hash: {self.last_hash}'
            f', Hash: {self.hash}'
            f', Data: {self.data}'
            f', Difficulty: {self.difficulty}'
            f', Nonce: {self.nonce})'
            )

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the last block given and data
        """
        time_stamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, time_stamp)
        nonce = 0
        hash = crypto_hash(time_stamp, last_hash, data, difficulty, nonce)

        while hex_to_bin(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            time_stamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, time_stamp)
            hash = crypto_hash(time_stamp, last_hash, data, difficulty, nonce)
        
        return Block(time_stamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def genesis():
        """
        This part generates the genesis block
        """
        return Block(**GENESIS_DATA)

    @staticmethod
    def adjust_difficulty( last_block, new_timestamp ):
        """
        This method, adjusts the difficulty according to the mine rate
        It increases the difficulty for quickly mined blocks,
        It decreases the difficulty for slowly mined blocks
        """
        if ( new_timestamp - last_block.time_stamp ) < MINE_RATE:
            return last_block.difficulty + 1

        if ( last_block.difficulty - 1 ) > 0:
            return last_block.difficulty - 1

        return 1

def main():
    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block,'y')
    print(block)

if __name__ == '__main__':
    main()