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

# 计算crc16校验
# return checksum's decimal integer, in hexadecimal: 高8位低8位
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

# 计算modbus指令的crc16校验，并返回字节尾带有验证码的指令
# 如：01 03 04 ff ff ff ff, 带上校验码后：01 03 04 ff ff ff ff a7 fb
def crc16_modbus(data: str):
    crc = crc16(bytes.fromhex(data))
    cmd = f"{data} {hex(crc)[4:]} {hex(crc)[2:4]}"
    return cmd



if __name__ == '__main__':
    # for num in range(51):
    #     hex_num = hex(num)[2:].zfill(2)
    #     cmd = '01 10 00 23 00 01 02 00 ' + hex_num
    #     crc_16 = get_crc16_modbus(cmd)
    #     fn.dp(crc_16)
    #  01 10 00 54 00 02 04 7f ff ff ff 
    # cmd = '01 06 30 05 0B B8'
    # data = bytes.fromhex('01 06 30 05 0B B8')
    # crc = crc16(data)
    # print(f"CRC16: {crc:04x}")
    data = bytes.fromhex('01 03 04 ff ff ff ff')
    crc = crc16(data)
    hexcrc = hex(crc)
    print(f"cmd: 01 03 04 ff ff ff ff, checksum:{crc}, 低8位:{hexcrc[2:4]}, 高8位:{hexcrc[4:]}")
    print(f"CRC16: {crc:04x}")
    print(crc16_modbus('01 03 04 ff ff ff ff'))

