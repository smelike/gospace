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
                "COM3", 19200, timeout = 0.015
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
        # 读取 9 bytes 的返回数据
        resp = self.serial.read(9)
        # '01 03 04 ff ff ff f9 7b a5'
        print(len(resp), resp, "::\r\n")
        weight_val_str = ' '.join(
            map(lambda x: '%02x' % x, resp)
            )
        return weight_val_str
    
    # 去皮

    # 读取内码值和净重

    def run(self):
        weights = []
        start = time.time()
        while True:
            try:
                val_str = self.get_weight_value()
                weights.append(val_str) if val_str else None
                if time.time() - start >= 1:
                    print(len(weights), weights)
                    break
            except Exception as e:
               print("读取失败,重新启动程序和设备")
            time.sleep(0.002)


if __name__ == "__main__":
    weighting = Weighter()
    weighting.run()
    # time.sleep(2000)
