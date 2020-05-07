from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transactions import Transaction
from backend.wallet.wallet import Wallet

def test_set_transaction():
    transaction_pool = TransactionPool()
    transaction = Transaction(Wallet(), 'reciepient', 1)
    transaction_pool.set_transaction(transaction)

    assert transaction_pool.transaction_map[transaction.id] == transaction