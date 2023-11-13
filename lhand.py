from serial_device_base import serial_device_base
import time
import sys

# 厂家建议，在 9600 速率下，读取时间间隔是 200 ms 以上。
# 9600 速率下，1 秒内只有 3 次；
# 19200 速率下，1 秒内可以读取 31、32 次；

class Lhand(serial_device_base):

    # 调用父类的初始化函数
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def read_di_status(self):
        modbus = "FE 02 00 00 00 04 6D C6"
        modbus = bytes.fromhex(modbus)
        resp = self.execute_command(modbus)

        return resp
    
    # 继电器状态切换 
    def swith():
        pass

if __name__ == "__main__":
    
    lhand = Lhand("COM5", 19200, timeout = 0)

    start = time.time()

    resp = []

    read_order = 0
    while True:
        read_order +=1
        value = lhand.read_di_status()
        resp.append(value)
        if time.time() - start > 1:
            print("Duration: {}".format(time.time() - start))
            print("次数：{}", read_order)
            break

    print(len(resp), resp)