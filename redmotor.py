import sys
import serial

class Redmot:
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
    # 01 06 20 00 00 00 01 43 CA 
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
    # 01 03 21 02 00 01 2F F6 - 01 03 02 00 0A 38 43 
    # 01 03 02 00 00 B8 44
    # (读地址 2102H，故障码：0x0A 欠压故障)

    def __init__(self):
        # 串口
        self.ser = serial.Serial("COM4", 19200, timeout=0.05)


    # 启动电机
    def turn_on(self):
        # 01 06 20 00 00 00 01 43 CA
        resp = self.ser.write(bytes.fromhex("01 06 20 00 00 00 01 43 CA"))
        if resp:
            print("启动电机成功", resp)
        else:
            print("启动电机失败", resp)
    
    # 关闭电机
    def turn_off(self):
        pass

    # 电机状态
    def run_status(self):
        pass

if __name__ == "__main__":
        print("start")
        rm = Redmot()
        rm.turn_on()
        time.sleep(1)
        rm.turn_off()
        print("end")