from serial_device_base import serial_device_base

import time
class Kpr(serial_device_base):

    def __init__(self, *args, **kwargs):
        # print(*args)
        super(Kpr, self).__init__(*args, **kwargs)

    def get_weight_value(self):
        print("get_weight_value")
        modbus = "010300500002c41a"
        modbus = bytes.fromhex(modbus)
        resp = self.execute_command(modbus)
        print(resp)

if __name__ == "__main__":

    kpr = Kpr("COM3", 19200)

    start = time.time()
    while True:
        kpr.get_weight_value()
        if time.time() - start > 10:
            str = "计算时间：{}".format(start - time.time())
            print(str)
            break
        # time.sleep(1)
    

