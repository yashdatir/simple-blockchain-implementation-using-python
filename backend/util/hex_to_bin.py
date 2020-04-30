from backend.util.crypto_hash import crypto_hash
HEX_TO_BIN_TABLE = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111'  
}

def hex_to_bin(hex):
    binary_string = ''

    for character in hex:
        binary_string += HEX_TO_BIN_TABLE[character]

    return binary_string

def main():
    number = 13
    hex_no = hex(number)[2:]
    binary = hex_to_bin(hex_no)
    print(f'hex number: {hex_no}, equivalent Binary is: {binary}')
    hex_to_binary_crypto_hash = hex_to_bin(crypto_hash('Yash'))
    print(f'hex_to_binary_crypto_hash: {hex_to_binary_crypto_hash}')

if __name__ == '__main__':
    main()