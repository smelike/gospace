from serial_device_base import SerialDeviceBase
import time
from crc16 import crc16_modbus

# Constants for addresses
BROADCAST_ADDRESS = 0x00
RESERVED_ADDRESS_START = 0x80

# Constants for commands
READ_REGISTER = 0x03

class Zdrv(SerialDeviceBase):
    # ZDRV.C20 - 120S2
    # MODBUS-RTU 方式
    # ADDR(1 Byte) - CMD(1 Byte) - DATA(n Bytes) - [CRC16_L](1Byte)+[CRC16_H](1 Bytes)

    # a-地址码： 1 Byte
    # 0x00(0) - 广播地址，广播时从机无回复，适用于多台群控
    # 0x01(1) - 0x7F(127) - 从机地址；
    # 0x80(128) - 0xff(255) - 系统保留，请勿使用；

    # b-功能码：1B Byte
    # 0x03(3) - 读寄存器操作
    # 0x06(6) - 写单个寄存器操作
    # 0x10(16) - 写多个寄存器操作

    # c-数据：n Byte
    # 不同指令有不同数据格式

    # d-校验码：2 Byte
    # CRC16 校验对象：地址码+功能码+数据；
    # CRC16校验算法：MODBUS(x16+x15+x2+1)
    # CRC校验码，先发送低字节，后发送高字节；

    # 正转运行 - 发送和应答数据： 
    # 01 06 20 00 00 01 43 CA 
    # 01 06 20 00 00 01 43 CA (地址2000H写0x01)

    # 反转运行 - 发送和应答数据
    # 01 06 20 00 00 02 03 CB
    # 01 06 20 00 00 02 03 CB (地址2000H写0x02)

    # 停机 - 发送和应答数据：
    # 01 06 20 00 00 05 42 09
    # 01 06 20 00 00 05 42 09

    # 故障复位 - 发送和应答数据：
    # 01 06 20 00 00 07 C3 C8
    # 01 06 20 00 00 07 C3 C8 (地址2000H写0x07)

    # 设定转速 - 发送和应答数据：
    # 01 06 20 01 0B B8 D4 88 - 01 06 20 01 0B B8 D4 88 
    # (地址 2001H写0x0BB8，设定转速 3000RPM)

    # 使功能码可写 - 发送和应答数据：
    # 01 06 20 0E 00 00 E3 C9 - 01 06 20 0E 00 00 E3 C9
    #(地址 200FH 写 0x01)

    # 读故障码 - 发送和应答数据：
    # 01 03 21 02 00 01 2F F6 - 01 03 02 00 0A 38 43/01 03 02 00 00 B8 44
    # (读地址 2102H，故障码：0x0A 欠压故障)

    def __init__(self, *args, **kwargs):
        super(Zdrv, self).__init__(*args, **kwargs)

    # 构建指令
    def build_command(self, cmd_type :int, addr :int, data :bytes):
        pass

    def control_motor(self, motor_address: int = 1, action: str = 'start'):
        """
        Controls the motor.

        Parameters:
            motor_address (int): The address of the motor to control. Default is 1.
            action (str): The action to perform. Can be 'start', 'stop', or 'reverse'. Default is 'start'.
        """
        if action == 'start':
            # Start the motor
            command = self.build_command(cmd_type=1, addr=motor_address, data=b'\x00\x01')
        elif action == 'stop':
            # Stop the motor
            command = self.build_command(cmd_type=1, addr=motor_address, data=b'\x00\x00')
        elif action == 'reverse':
            # Reverse the motor
            command = self.build_command(cmd_type=1, addr=motor_address, data=b'\x00\x02')
        else:
            raise ValueError("Invalid action. Must be 'start', 'stop', or 'reverse'.")

        self.execute_command(command)
    # 启动电机
    def turn_on(self, motor_address :int = 1):
        # 地址：2000H
        # 01 06 20 00 00 {00 01} 43 CA 
        # 00 01 - 正转
        # 00 02 - 反转
        # 00 03 - 正转点动
        # 00 04 - 反转点动
        # 00 05 - 停机
        # 00 06 - 自由停机（紧急停机）
        # 00 07 - 故障复位
        # 00 08 - 点动停止
        # 00 09 - 刹车停机
        motor_hex_addr = str(hex(motor_address))[2:].zfill(2)
        print(motor_hex_addr)
        cmd = f"{motor_hex_addr} 06 20 00 00 01"
        cmd_crc = crc16_modbus(cmd)
        print(cmd_crc)
        cmd_byte = bytes.fromhex(cmd_crc)
        # cmd_byte = bytes.fromhex("02 06 20 00 00 01 43 CA")
        resp = self.execute_command(cmd_byte)
        if resp == cmd_byte:
            print("启动电机成功", resp)
        else:
            print("启动电机失败", resp)
    
    # 关闭电机
    def turn_stop(self):
        if self.ser.is_open:
            cmd_byte = bytes.fromhex("02 06 20 00 00 05 42 09")
            resp = self.execute_command(cmd_byte)
            print(" ".join(map(lambda x: "%02x" % x, resp)))
            if resp == cmd_byte:
                print("关闭电机成功", resp)
            else:
                print("关闭电机失败", resp)
        else:
            print("串口未打开")

    def set_rpm(self, rpm = 3000):
        # 2001H 通讯设定转速 
        # 3000rpm - 01 06 20 01 0B B8 D4 88 
        # 地址 2001H写0x0BB8，设定转速 3000RPM
        if not rpm:
            rpm = 1630
        cmd = "02 06 20 01"
        motor_speed = str(hex(rpm))[2:].zfill(4)
        cmd = f"02 06 20 01 {motor_speed}"
        cmd_crc = crc16_modbus(cmd)
        print(cmd_crc)
        cmd_byte = bytes.fromhex(cmd_crc)
        resp = self.execute_command(cmd_byte)
        print(" ".join(map(lambda x: "%02x" % x, resp)))
        if resp == cmd_byte:
            print("设置转速成功", resp)
        else:
            print("设置转速失败", resp)

    # 电机状态
    def run_status(self):
        if self.ser.is_open:
            cmd_byte = bytes.fromhex("01 03 21 02 00 01 2F F6")
            resp = self.execute_command(cmd_byte)
            print(" ".join(map(lambda x: "%02x" % x, resp)))
            print("电机状态码：", resp)
        else:
            print("串口未打开")

if __name__ == "__main__":
        print("start")
        rm = Zdrv("COM15", 19200)
        rm.turn_on(2)
        time.sleep(8)
        rm.set_rpm()
        time.sleep(6)
        rm.set_rpm(rpm = 1630)
        # rm.turn_on()
        time.sleep(8)
        rm.turn_stop()
        print("end")