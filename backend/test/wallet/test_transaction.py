import pytest

from backend.wallet.transactions import Transaction
from backend.wallet.wallet import Wallet

def test_transaction():
    sender_wallet = Wallet()
    reciepient = 'reciepient'
    amount = 50
    transaction = Transaction(sender_wallet, reciepient, amount)

    assert transaction.output[reciepient] == amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount
    assert 'timestamp' in transaction.input
    assert transaction.input['amount'] == sender_wallet.balance
    assert transaction.input['address'] == sender_wallet.address
    assert transaction.input['public_key'] == sender_wallet.public_key

    assert Wallet.verify(transaction.input['public_key'], transaction.output, transaction.input['signature'])

def test_transaction_exceeds_balance():
    with pytest.raises(Exception, match='Amount exceeds the Balance'):
        Transaction(Wallet(), 'reciepient', 1998)


def test_transaction_update_exceeds_balance():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'reciepient', 50)

    with pytest.raises(Exception, match='Amount exceeds balance'):
        transaction.update(sender_wallet, 'new_reciepient', 1998)

def test_transaction_update():
    sender_wallet = Wallet()
    first_recipient = 'first_person'
    first_amount = 50
    transaction = Transaction(sender_wallet, first_recipient, first_amount)

    next_reciepient = 'other_person'
    next_amount = 80
    transaction.update(sender_wallet, next_reciepient, next_amount)

    assert transaction.output[next_reciepient] == next_amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - first_amount - next_amount
    assert Wallet.verify(transaction.input['public_key'], transaction.output, transaction.input['signature'])

    to_first_again_amount = 25
    transaction.update(sender_wallet, first_recipient, to_first_again_amount)

    assert transaction.output[first_recipient] == first_amount + to_first_again_amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - first_amount - next_amount - to_first_again_amount
    assert Wallet.verify(transaction.input['public_key'], transaction.output, transaction.input['signature'])

def test_valid_transaction():
    Transaction.transaction_is_valid(Transaction(Wallet(), 'reciepient', 50))

def test_valid_transaction_with_invalid_outputs():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'reciepient', 50)
    transaction.output[sender_wallet.address] = 1998

    with pytest.raises(Exception, match='Invalid transaction output values'):
        Transaction.transaction_is_valid(transaction)

def test_valid_transaction_with_invalid_signature():
    transaction = Transaction(Wallet(), 'reciepient', 50)
    transaction.input['signature'] = Wallet().sign(transaction.output)

    with pytest.raises(Exception, match='Invalid signature'):
        Transaction.transaction_is_valid(transaction)