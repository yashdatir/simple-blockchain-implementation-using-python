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

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        """
        Serialize a block into a dictionary of its attribute 
        """
        return self.__dict__

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
    def from_json(block_json):
        """
        Deserialize a block's json representation back to block instance
        """
        return Block(**block_json)

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

    @staticmethod
    def is_valid_block(last_block, block):
        """
        Validate the block by enforcing the following rules:
            - the block must have proper last_hash reference
            - the block must see the proof of work requirement
            - difficult must be adjust by 1
            - the block hash must be valid combination of the block fields
        """
        if block.last_hash != last_block.hash:
            raise Exception('the last_hash mustbe correct')

        if hex_to_bin(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('the proof of requirement was not meet')

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('the block difficulty should change by 1')

        reconstructed_hash = crypto_hash (
            block.time_stamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce
        )

        if block.hash != reconstructed_hash:
            raise Exception('The block hash must be correct')


def main():
    genesis_block = Block.genesis()
    bad_block = Block.mine_block(genesis_block, 'test_data')
    #bad_block.last_hash = 'evil_data'
    try:
        Block.is_valid_block(genesis_block, bad_block)
    except Exception as e: 
        print(f'The is valid block: {e}')       

if __name__ == '__main__':
    main()