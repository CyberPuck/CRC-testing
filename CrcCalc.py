"""
Python functions for calculating CRC7 and CRC16 on a given byte array.
Each element is expected to be an 8-bit number.
Polynomials are defined in the functions (called polynomial)
"""
def calc_crc(message_array):
    """
    CRC7 Algorithm, given an array of "bytes" (8-bit numbers) calculate a CRC7.
    Polynomial: 0x89
    @param message_array, array of bytes to calculate a CRC7.
    """
    message_length = len(message_array) * 8
    remainder = message_array[0]

    polynomial = 0x89

    # original design, do we need to run through the PADDING bits?
    for bit_index in range(0, message_length):
        # Pull from next byte, skip when we have pulled in the last byte (8 bits ahead of end)
        # last 7 bits are zeros (padding)
        if bit_index != 0 and bit_index < (message_length - 8):
            # grab the next byte
            # -1 ensures the starting bit of a byte gets the last bit of its byte
            next_byte_index = int((bit_index-1) / 8) + 1
            # Need to offset for next bit to add
            next_byte_bit_position = (bit_index + 8) % 8
            # Convert out of range case (8) to 0, ensure offset is in order for shifting in the byte
            next_byte_bit_position = (8 - next_byte_bit_position) % 8
            next_value = (message_array[next_byte_index] >> next_byte_bit_position) & 0x1

            remainder |= next_value

        # This will always skip the MSB (CRC-7 is 7 bits long and SD card CMD MSB is always '0b0')
        if remainder & 0x80:
            remainder ^= polynomial
        # the final bit has been processed, kick out of loop
        if bit_index >= message_length - 1:
            break
        remainder <<= 1
        # keep only the first 8 bits
        # NOTE: Do not move this to the C version (C type have a defined size)
        remainder &= 0xFF
    return remainder


def calc_crc16(message_array):
    """
    CRC16 Algorithm, given an array of "bytes" (8-bit numbers) calculate a CRC16.
    Polynomial: 0x11021 (17-bits)
    @param message_array, array of bytes to calculate a CRC16.
    """
    message_length = len(message_array) * 8
    # setup initial remainder (17 bits)
    remainder = message_array[0]
    remainder <<= 8
    remainder |= message_array[1]
    remainder <<= 1
    last_value = message_array[2] & 0x80
    last_value >>= 7
    remainder |= last_value

    polynomial = 0x11021

    # original design, do we need to run through the PADDING bits?
    for bit_index in range(0, message_length):
        # Pull from next byte, skip when we have pulled in the last byte (8 bits ahead of end)
        # last 17 bits are zeros (padding)
        if bit_index != 0 and bit_index < (message_length - 16):
            # grab the next byte
            # -1 ensures the starting bit of a byte gets the last bit of its byte
            next_byte_index = int((bit_index-1) / 8) + 2
            # Need to offset for next bit to add
            next_byte_bit_position = (bit_index + 8) % 8
            # Convert out of range case (8) to 0, ensure offset is in order for shifting in the byte
            next_byte_bit_position = (8 - next_byte_bit_position) % 8
            next_value = (message_array[next_byte_index] >> next_byte_bit_position) & 0x1

            remainder |= next_value

        # This will always skip the MSB (CRC-7 is 7 bits long and SD card CMD MSB is always '0b0')
        if remainder & 0x10000:
            remainder ^= polynomial
        # the final bit has been processed, kick out of loop
        if bit_index >= message_length - 1:
            break
        remainder <<= 1
        # keep only the first 17 bits
        # NOTE: Remove for the C version, not needed
        remainder &= 0x1FFFF
    return remainder


if __name__ == "__main__":
    # Messages with known CRC values
    MESSAGE_ARRAY_1 = [0x40, 0x00, 0x00, 0x00, 0x00]
    MESSAGE_ARRAY_2 = [0x51, 0x00, 0x00, 0x00, 0x00]
    MESSAGE_ARRAY_3 = [0x11, 0x00, 0x00, 0x09, 0x00]
    # generate 512 byte array of 0xFF
    MESSAGE_ARRAY_4 = []
    for i in range(0, 512):
        MESSAGE_ARRAY_4.append(0xFF)
    # CRC-7 tests
    RESULT_1 = calc_crc(MESSAGE_ARRAY_1)
    RESULT_2 = calc_crc(MESSAGE_ARRAY_2)
    RESULT_3 = calc_crc(MESSAGE_ARRAY_3)
    # CRC-16 tests
    RESULT_4 = calc_crc16(MESSAGE_ARRAY_4)

    # print out the results
    print("----CRC-7 Results----")
    print("Result1: ", bin(RESULT_1)) # expect: b1001010
    print("Result2: ", bin(RESULT_2)) # expect: b0101010
    print("Result3: ", bin(RESULT_3)) # expect: b0110011

    print("====CRC-16 Results====")
    print("Result4: ", hex(RESULT_4)) # expect: 0x7FA1
