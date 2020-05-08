from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transactions import Transaction
from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain

def test_set_transaction():
    transaction_pool = TransactionPool()
    transaction = Transaction(Wallet(), 'reciepient', 1)
    transaction_pool.set_transaction(transaction)

    assert transaction_pool.transaction_map[transaction.id] == transaction

def test_clear_blockchain_transaction():
    transaction_pool = TransactionPool()
    transaction_1 = Transaction(Wallet(), 'reciepient', 1)
    transaction_2 = Transaction(Wallet(), 'reciepient', 2)

    transaction_pool.set_transaction(transaction_1)
    transaction_pool.set_transaction(transaction_2)

    blockchain = Blockchain()
    blockchain.add_block([transaction_1.to_json(), transaction_2.to_json()])

    assert transaction_1.id in transaction_pool.transaction_map
    assert transaction_2.id in transaction_pool.transaction_map

    transaction_pool.clear_blockchain_transactions(blockchain)

    assert not transaction_1.id in transaction_pool.transaction_map
    assert not transaction_2.id in transaction_pool.transaction_map