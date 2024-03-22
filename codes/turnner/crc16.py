# 1 - 3000 - 01 06 20 01 0b b8 d4 88
# 2 - 1350 - 02 06 20 01 05 46 51 5b
# 3 - 3000 - 03 06 20 01 05 46 50 8a
# motor_addr = str(hex(3))[2:].zfill(2)
# motor_speed = str(hex(1350))[2:].zfill(4)
# speed_cmd = f"{motor_addr} 06 20 01 {motor_speed[:2]} {motor_speed[2:]}"
# speed_cmd_crc_16 = get_crc16_modbus(speed_cmd)
# speed_cmd = f"{speed_cmd} {speed_cmd_crc_16}"
# fn.logger(speed_cmd)
# exit()
# from common import fn


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
    crc16_decimal_data = crc16(bytes.fromhex(data))
    # format decimal crc16 data to hexadecimal digits
    # fn.logger("crc16 format crc with x pattern " + format(crc16_decimal_data, "x"))
    crcHex = format(crc16_decimal_data, "x").zfill(4)
    crcLow = crcHex[2:]
    crcHigh = crcHex[0:2]
    # crcLow = format(int(crcHex[2:], 16), '02x')
    # crcHigh = format(int(crcHex[0:2], 16), '02x')
    cmd = f"{data} {crcLow} {crcHigh}"
    return cmd


def int_to_hex(n, length):
    return format(n, '0{}x'.format(length))


if __name__ == '__main__':
    # for num in range(51):
    #     hex_num = hex(num)[2:].zfill(2)
    #     cmd = '01 10 00 23 00 01 02 00 ' + hex_num
    #     crc_16 = get_crc16_modbus(cmd)
    #     fn.dp(crc_16)
    #  01 10 00 54 00 02 04 7f ff ff ff 
    # cmd = '01 06 30 05 0B B8'
    # data = bytes.fromhex('01 06 30 05 0B B8')
    # data = bytes.fromhex("03 03 21 02 00 01")
    # crc = crc16(data)
    # print(f"CRC16: {crc:04x}")
    # exit(200)
    data = bytes.fromhex('03 03 21 02 00 01')
    crc = crc16(data)
    hexcrc = hex(crc)
    print(f"crc16 cmd: 01 03 04 ff ff ff ff, checksum:{crc}, 低8位:{hexcrc[2:4]}, 高8位:{hexcrc[4:]}")
    print(f"crc16 CRC16: {crc:04x}")
    print(str(crc16_modbus('03 03 21 02 00 01')))


    print("crc16 \\r\\n---------[Error Test: Set RPM]-----------\\r\\n")

    motor_addr_hex = format(3, "02x") #03
    speed_hex = format(2000, "04x") # 0320
    cmd = f"03 06 20 01 {speed_hex}"
    cmd_crc = crc16_modbus(cmd)
    print("crc16 cmd_crc: " + cmd_crc)
