from backend.util.hex_to_bin import hex_to_bin

def test_hex_to_binary():
    number = 789
    hex_number = hex(number)[2:]

    binary = hex_to_bin(hex_number)

    assert int(binary, 2) == number