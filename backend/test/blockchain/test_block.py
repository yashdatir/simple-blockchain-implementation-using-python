import pytest
import time
from backend.blockchain.block import Block, GENESIS_DATA
from backend.config import MINE_RATE, SECONDS
from backend.util.hex_to_bin import hex_to_bin

def test_mine_block():
    last_block = Block.genesis()
    data = 'Test-Data'
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_bin(block.hash)[0:block.difficulty] == '0' * block.difficulty

def test_genesis():
    genesis = Block.genesis()

    assert isinstance(genesis, Block)

    for key, value in GENESIS_DATA.items():
        getattr(genesis, key) == value

def test_quickly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'Yash')
    mined_block = Block.mine_block(last_block, 'Datir')

    assert mined_block.difficulty == last_block.difficulty + 1

def test_slowly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'Yash')
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'Datir')

    assert mined_block.difficulty == last_block.difficulty - 1


def test_minedblock_difficulty_limit_at_1():
    last_block = Block(
        time.time_ns(),
        'test_last_hash',
        'test_hash',
        'test_data',
        1,
        0 
    )

    time.sleep(MINE_RATE / SECONDS)

    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == 1

@pytest.fixture
def last_block():
    return Block.genesis()

@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block, 'test_data')

def test_is_valid_block(last_block, block):
    Block.is_valid_block(last_block, block)

def test_is_valid_bad_block(last_block, block):
    block.last_hash = 'last_hash'
    with pytest.raises(Exception, match='the last_hash mustbe correct'):
        Block.is_valid_block(last_block, block)

def test_is_valid_block_bad_proof_of_work(last_block, block):
    block.hash = 'fff'
    with pytest.raises(Exception, match='the proof of requirement was not meet'):
        Block.is_valid_block(last_block, block)

def test_is_valid_block_jumped_difficulty(last_block, block):
    jumped_difficulty = 10
    block.difficulty = jumped_difficulty
    block.hash = f'{"0" * jumped_difficulty}abc111'
    with pytest.raises(Exception, match='the block difficulty should change by 1'):
        Block.is_valid_block(last_block, block)

def test_is_valid_block_bad_block_hash(last_block, block):
    block.hash = '0000000000fabc111'

    with pytest.raises(Exception, match='The block hash must be correct'):
        Block.is_valid_block(last_block, block)