import json
import math
import serial
import time


class Weighter:
    def __init__(self):
       self.w_serial_port = list()
       self.supply = "kpr"
       self.simulation = 0
       self.init_serial()

    def init_serial(self):
        if self.simulation != 2:
            self.serial = serial.Serial(
                "COM27", 19200, timeout = 0.015
                )
        else:
            self.serial = None

    # 获取厂商的 modbus 指令
    def modbus_cmd(self): 
        if self.supply == 'kpr':
            modbus = "010300500002c41a"
        elif self.supply == 'xy':
            modbus = "010300000002c40b"
        else:
            modbus = "010300500002c41a"
        return modbus
    
    # 写串口后，读取串口的返回数据
    def get_weight_value(self):
        cmd = self.modbus_cmd()
        self.serial.write(bytes.fromhex(cmd))
        resp = self.serial.readall()
        print(resp, "---")
        weight_val_str = ' '.join(
            map(lambda x: '%02x' % x, resp)
            )
        return weight_val_str
    
    # 去皮

    # 读取内码值和净重

    def run(self):

        while True:
            try:
               weight_val_str = self.get_weight_value()
               print(weight_val_str, "run--\n\n\n")
            except Exception as e:
               print("读取失败")
            time.sleep(0.0001)


if __name__ == "__main__":
    weighting = Weigh()
    weighting.run()
    time.sleep(10000)
