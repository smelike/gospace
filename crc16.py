import crcmod

def crc16(byte_str):
    crc = crcmod.predefined.Crc('crc-16-modbus')
    crc.update(byte_str)
    return crc.crcValue

cmd = "01 10 00 54 00 02 04 7f ff ff ff df 34"
cmd = " ".join(map(lambda x: "%02x" % x, int(cmd.split(), 16)))
cmd = bytes(cmd)
print(cmd)
print(cmd.hex())
cmd = bytes.fromhex(cmd)
crc16(b'\x01\x03\x05\x00\x00\x02\xC4\x1A') 
def get_crc16_modbus(hex_str):
    hex_str = hex_str.replace(' ', '')
    hex_str_length = len(hex_str)
    if hex_str_length % 2 != 0 or hex_str_length == 0:
        return ''
    hex_list = []
    for i in range(0, hex_str_length, 2):
        hex_list.append(hex_str[i:i + 2])
    b = len(hex_list)
    c = 65535
    f = [0, 49345, 49537, 320, 49921, 960, 640, 49729, 50689, 1728, 1920, 51009, 1280, 50625, 50305, 1088, 52225, 3264,
         3456, 52545, 3840, 53185, 52865, 3648, 2560, 51905, 52097, 2880, 51457, 2496, 2176, 51265, 55297, 6336, 6528,
         55617, 6912, 56257, 55937, 6720, 7680, 57025, 57217, 8E3, 56577, 7616, 7296, 56385, 5120, 54465, 54657, 5440,
         55041, 6080, 5760, 54849, 53761, 4800, 4992, 54081, 4352, 53697, 53377, 4160, 61441, 12480, 12672, 61761,
         13056,
         62401, 62081, 12864, 13824, 63169, 63361, 14144, 62721, 13760, 13440, 62529, 15360, 64705, 64897, 15680, 65281,
         16320, 16E3, 65089, 64001, 15040, 15232, 64321, 14592, 63937, 63617, 14400, 10240, 59585, 59777, 10560, 60161,
         11200, 10880, 59969, 60929, 11968, 12160, 61249, 11520, 60865, 60545, 11328, 58369, 9408, 9600, 58689, 9984,
         59329,
         59009, 9792, 8704, 58049, 58241, 9024, 57601, 8640, 8320, 57409, 40961, 24768, 24960, 41281, 25344, 41921,
         41601,
         25152, 26112, 42689, 42881, 26432, 42241, 26048, 25728, 42049, 27648, 44225, 44417, 27968, 44801, 28608, 28288,
         44609, 43521, 27328, 27520, 43841, 26880, 43457, 43137, 26688, 30720, 47297, 47489, 31040, 47873, 31680, 31360,
         47681, 48641, 32448, 32640, 48961, 32E3, 48577, 48257, 31808, 46081, 29888, 30080, 46401, 30464, 47041, 46721,
         30272, 29184, 45761, 45953, 29504, 45313, 29120, 28800, 45121, 20480, 37057, 37249, 20800, 37633, 21440, 21120,
         37441, 38401, 22208, 22400, 38721, 21760, 38337, 38017, 21568, 39937, 23744, 23936, 40257, 24320, 40897, 40577,
         24128, 23040, 39617, 39809, 23360, 39169, 22976, 22656, 38977, 34817, 18624, 18816, 35137, 19200, 35777, 35457,
         19008, 19968, 36545, 36737, 20288, 36097, 19904, 19584, 35905, 17408, 33985, 34177, 17728, 34561, 18368, 18048,
         34369, 33281, 17088, 17280, 33601, 16640, 33217, 32897, 16448]
    i = 0
    while b > 0:
        d = c & 255
        c = c >> 8 ^ int(f[(d ^ int(hex_list[i], 16)) & 255])
        b -= 1
        i += 1
    c = c & 65535
    hex_result = hex(c)[2:]
    if len(hex_result) % 2 != 0:
        hex_result = '0' + hex_result
    hex_result = hex_result[2:] + ' ' + hex_result[0:2]
    return hex_result

# 1 - 3000 - 01 06 20 01 0b b8 d4 88
# 2 - 1350 - 02 06 20 01 05 46 51 5b
# 3 - 3000 - 03 06 20 01 05 46 50 8a
# motor_addr = str(hex(3))[2:].zfill(2)
# motor_speed = str(hex(1350))[2:].zfill(4)
# speed_cmd = f"{motor_addr} 06 20 01 {motor_speed[:2]} {motor_speed[2:]}"
# speed_cmd_crc_16 = get_crc16_modbus(speed_cmd)
# speed_cmd = f"{speed_cmd} {speed_cmd_crc_16}"
# print(speed_cmd)
# exit()

def crc16(data: bytes):
    crc = 0xFFFF
    for b in data:
        cur_byte = 0xFF & b
        for _ in range(0, 8):
            if (crc & 0x0001) ^ (cur_byte & 0x0001):
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
            cur_byte >>= 1
    return crc

def crc16byStr(data: str) -> int:
    data = bytes.fromhex(data)
    crc = 0xFFFF
    for b in data:
        cur_byte = 0xFF & b
        for _ in range(0, 8):
            if (crc & 0x0001) ^ (cur_byte & 0x0001):
                crc = (crc >> 1) ^ 0xA001
            else: 
                crc >>= 1
            cur_byte >>= 1
    return crc

def crc162(data: bytes):
    crc = 0xFFFF
    for b in data:
        crc = crc ^ b
        for _ in range(8):
            if (crc & 0x0001):
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc


# data = bytes.fromhex('01 06 30 05 0B B8')
# crc = crc16(data)
# print(f"CRC16: {crc:04x}")

if __name__ == '__main__':
    # for num in range(51):
    #     hex_num = hex(num)[2:].zfill(2)
    #     cmd = '01 10 00 23 00 01 02 00 ' + hex_num
    #     crc_16 = get_crc16_modbus(cmd)
    #     fn.dp(crc_16)
    #  01 10 00 54 00 02 04 7f ff ff ff 
    # cmd = '01 06 30 05 0B B8'
    cmd = "01 10 00 54 00 02 04 7f ff ff ff df 34"
    crc_16 = get_crc16_modbus(cmd)
    print(crc_16)
    crc_resp = crc16byStr(cmd)
    print(crc_resp)
    crc_resp = crc16(bytes.fromhex(cmd))
    print(crc_resp)
