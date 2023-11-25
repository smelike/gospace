import sys
import time
from serial_device_base import SerialDeviceBase

# 高光幕
# 光幕型号:ESCL16005L1RZ-1
# 光幕光束:160个 0.5mm LED

class Highter(SerialDeviceBase):

    def __init__(self, *args, **kwargs):
        # 串口
       super(Highter, self).__init__(*args, **kwargs)

 
    def get_height_value(self):
        modbus = "03 03 00 00 00 0F 04 2C"
        modbus = bytes.fromhex(modbus)
        respBytes = self.execute_command(modbus)
        if respBytes and len(respBytes) > 2:
            # 0 1 2 3 ~ len - 2
            heightBytes = respBytes[3:len(respBytes)-2]
            # print(heightBytes)
            data_bytes = heightBytes
            return [data_bytes[i:i+3].hex() for i in range(0, len(data_bytes), 3)]
        else:
            return None

# 返回数据：摆放不动的箱子
# 03 03 00 00 00 0F 04 2C □
# [17:10:11.957]收←◆03 03 1E 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 AD D9 
# [17:10:14.101]发→◇03 03 00 00 00 0F 04 2C □
# [17:10:14.117]收←◆03 03 1B 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 F0 ED 


# [17:10:14.452]发→◇03 03 00 00 00 0F 04 2C □
# [17:10:14.469]收←◆03 03 18 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 ED CA 

# [17:10:14.653]发→◇03 03 00 00 00 0F 04 2C □
# [17:10:14.660]收←◆03 03 1E 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 37 02 36 AD D9 

if __name__ == "__main__":
    highter = Highter("COM8", 115200, timeout=0.02)
    modbus = "03 03 00 00 00 0F 04 2C"
    modbus = bytes.fromhex(modbus)
    start = time.time()
    resp_list = []
    loop = 0
    while True:
        loop += 1
        print(highter.get_height_value())
        # print("((发)){0}:".format(time.time() * 1000), modbus.hex())
        # resp = highter.execute_command(modbus)
        # # print("returns{}:".format(loop), resp)
        # if resp:
        #     print("[[收]]{0}:".format(time.time() * 1000), resp.hex())
        #     resp_list.append(resp)
        # time.sleep(0.1)

        # if time.time() - start >= 3:
        #     print(loop, len(resp_list), resp_list)
        #     break