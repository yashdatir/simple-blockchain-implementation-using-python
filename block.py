class Block:
    """
    Block : is a unit of storage
    store transactions in a blockchain that supports a cryptocurrency
    """
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f'{self.data}'

def main():
    block = Block('yash')
    print(block)
    print(f'block.py __name__: {__name__}')

if __name__ == '__main__':
    main()