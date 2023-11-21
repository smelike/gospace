from serial_device_base import SerialDeviceBase
import time

# 长宽光幕 L1RZ
# 型号: ECSL16005L1RZ-1
# 160 个 LED 
class Lwter(SerialDeviceBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        

if __name__ == "__main__":

    # 长宽光幕初始化
    lwter = Lwter("COM7", 115200)
    # 打开串口成功，则获取主动发出的数据
    # print("a", lwter.open_port(), "b")
    resp_list = []
    start = time.time()
    loop = 0
    while True:
        loop += 1
        resp = lwter.read_data()
        if resp:
            resp_list.append(resp)
            # print(resp)
        # time.sleep(0.1) 
        # 100 ms * 9 = 900 ms

        if time.time() - start > 1:
            print("计算时间：{}".format(start - time.time()))
            print(loop, len(resp_list), resp_list)
            break
