import time

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from backend.blockchain.block import Block
from backend.wallet.transactions import Transaction

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'SUBSCRIBE_KEY'
pnconfig.publish_key = 'PUBLISH_KEY'

CHANNELS = {
    'TEST' : 'TEST',
    'BLOCK': 'BLOCK',
    'TRANSACTION' : 'TRANSACTION'
}

class Listener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool
    
    def message(self, pubnub, msg_obj):
        print(f'\n-- Incoming Channel: {msg_obj.channel} | message: {msg_obj.message}')
        if msg_obj.channel == CHANNELS['BLOCK']:
            block = Block.from_json(msg_obj.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                self.transaction_pool.clear_blockchain_transactions(self.blockchain)
                print('successfullt replaced the chaihn')
            except Exception as e:
                print(f'\n -- Did not replace chain {e}')

        elif msg_obj.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(msg_obj.message)
            self.transaction_pool.set_transaction(transaction)
            print('\n-- Set the new transaction in the transaction pool')

class PubSub():
    """
    Handles the publish / subscribe layer of the application,
    Provides the communication between the nodes of the blockchain network.
    """
    def __init__(self, blockchain, transaction_pool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))

    def publish(self, channel, message):
        """
        Publish message object to the channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """
        Broadcast a block object to all nodes
        """
        self.publish(CHANNELS['BLOCK'], block.to_json())

    def broadcast_transaction(self, transaction):
        """
        Broadcast a transaction to all nodes
        """
        self.publish(CHANNELS['TRANSACTION'], transaction.to_json())

def main():
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'], {'name':'india'})

if __name__ == '__main__':
    main()
