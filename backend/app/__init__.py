import os
import requests
import random

from flask import Flask, jsonify, request

from backend.blockchain.blockchain import Blockchain
from backend.wallet.wallet import Wallet
from backend.wallet.transactions import Transaction
from backend.wallet.transaction_pool import TransactionPool
from backend.pubsub import PubSub

app = Flask(__name__)

blockchain = Blockchain()
wallet = Wallet()
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool)

@app.route('/')
def route_default():
    return 'Welcome to BlockChain Network'

@app.route('/Blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())

@app.route('/Blockchain/mine')
def route_blockchain_mine():
    transaction_data = 'stubbed_transaction_data'
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    return jsonify(block.to_json())

@app.route('/wallet/transact', methods=['POST'])
def route_wallet_transact():
    transaction_data = request.get_json()
    transaction = transaction_pool.existing_transaction(wallet.address)
    
    if transaction:
        transaction.update(wallet, transaction_data['reciepient'], transaction_data['amount'])
    else:
        transaction = Transaction(wallet, transaction_data['reciepient'], transaction_data['amount'])
    
    pubsub.broadcast_transaction(transaction)
    return jsonify(transaction.to_json())

ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)

    result = requests.get(f'http://localhost:{ROOT_PORT}/Blockchain')
    result_blockchain = Blockchain.from_json(result.json())
    try:
        blockchain.replace_chain(result_blockchain)
        print('\n-- Successfully synchronized the chain')
    except Exception as e:
        print(f'\n-- Error synchronizing the chain: {e}')

app.run(port = PORT)