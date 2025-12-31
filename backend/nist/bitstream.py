def hex_to_bits(hex_string):
    return ''.join(format(int(c, 16), '04b') for c in hex_string)

def entropy_blocks_to_bitstream(entropy_blocks):
    bitstream = ""
    for block in entropy_blocks:
        bitstream += hex_to_bits(block)
    return bitstream
