from serial_device_base import SerialDeviceBase

import time
class Kpr(SerialDeviceBase):

    def __init__(self, *args, **kwargs):
        # print(*args)
        super(Kpr, self).__init__(*args, **kwargs)

    def get_weight_value(self):
        modbus = "010300500002c41a"
        modbus = bytes.fromhex(modbus)
        resp = self.execute_command(modbus)
        return resp
    
    # 计算十进制的重量
    def calc_weight(self, weight_hex_value):
        sp = weight_hex_value.split(" ")[3:7]
        calc_weight = int("".join(sp), 16) * 0.001
        weight_dec = round(calc_weight, 3)
        return [sp, weight_dec]

if __name__ == "__main__":

    # 测试1 
    # kpr = Kpr("COM3", 19200)
    
    # 测试2
    kpr = Kpr("COM6", 19200, 0.02)
    start = time.time()
    resp = []
    while True:
        # 01 03 04 ff ff ff ff fb a7
        retbytes = kpr.get_weight_value()
        response = " ".join(map(lambda x: "%02x" % x, retbytes))
        weight_dec = kpr.calc_weight(response)
        # print(response)
        resp.append(weight_dec)
        if time.time() - start > 6:
            time_elapsed = "计算时间：{}".format(start - time.time())
            print(time_elapsed)
            break
        # time.sleep(1)
    print(len(resp), resp)
    

