from serial_device_base import SerialDeviceBase
import time

# 长宽光幕 L1RZ
# 型号: ECSL16005L1RZ-1
# 160 个 LED 
# 返回数据格式：01 03 08 00 22 00 77 00 56 00 17 C3 C0 
# 数据段是：00 22 00 77 00 56 00 17
class Lwter(SerialDeviceBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    
    def get_led_data(self):
        respBytes = self.read_data()
        if respBytes and len(respBytes) > 13:
            # 0 1 2 3 ~ len - 2
            # heightBytes = respBytes[3:len(respBytes)-2]
            # print(heightBytes)
            # data_bytes = heightBytes
            # 01 03 08 00 00 00 00 00 00 00 00 95 D7
            # 返回数据：去掉前面3个字节，后面2个字节是CRC校验
            return [respBytes[i+3:i+11].hex() for i in range(0, len(respBytes), 13)]
        else:
            return None

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
        # resp = lwter.read_data()
        resp = lwter.get_led_data()
        if resp:
            resp_list += resp
            # print(resp)
        # time.sleep(0.1) 
        # 100 ms * 9 = 900 ms

        if time.time() - start > 1:
            print("计算时间：{}".format(start - time.time()))
            print(loop, len(resp_list), resp_list)
            break
