import time

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from backend.blockchain.block import Block

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-0510e2a0-8e47-11ea-8e98-72774568d584'
pnconfig.publish_key = 'pub-c-c15517c6-6801-42ff-b169-6ae40b5e4113'

CHANNELS = {
    'TEST' : 'TEST',
    'BLOCK': 'BLOCK'
}

class Listener(SubscribeCallback):
    def __init__(self, blockchain):
        self.blockchain = blockchain
    
    def message(self, pubnub, msg_obj):
        print(f'\n-- Incoming Channel: {msg_obj.channel} | message: {msg_obj.message}')
        if msg_obj.channel == CHANNELS['BLOCK']:
            block = Block.from_json(msg_obj.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                print('successfullt replaced the chaihn')
            except Exception as e:
                print(f'\n -- Did not replace chain {e}')

class PubSub():
    """
    Handles the publish / subscribe layer of the application,
    Provides the communication between the nodes of the blockchain network.
    """
    def __init__(self, blockchain):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain))

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

def main():
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'], {'name':'india'})

if __name__ == '__main__':
    main()