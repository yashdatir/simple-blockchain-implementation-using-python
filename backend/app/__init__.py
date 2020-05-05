import os
import requests
import random

from flask import Flask, jsonify

from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub

app = Flask(__name__)

blockchain = Blockchain()
pubsub = PubSub(blockchain)

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