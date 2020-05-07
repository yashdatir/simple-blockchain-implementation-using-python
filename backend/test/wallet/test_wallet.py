from backend.wallet.wallet import Wallet

def test_verify_valid_signatures():
    data = { 'foo': 'bar' }
    wallet = Wallet()
    signature = wallet.sign(data)

    assert Wallet.verify(wallet.public_key, data, signature)

def test_verify_invalid_signaturess():
    data = { 'foo': 'bar' }
    wallet = Wallet()
    signature = wallet.sign(data)

    assert not Wallet.verify(Wallet().public_key, data, signature)