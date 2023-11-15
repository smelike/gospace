from serial_device_base import SerialDeviceBase
import time

class Lwter(SerialDeviceBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        

if __name__ == "__main__":

    # 长宽光幕初始化
    lwter = Lwter("COM7", 19200)
    # 打开串口成功，则获取主动发出的数据
    # print("a", lwter.open_port(), "b")
    resp_list = []
    start = time.time()
    while True:
        resp = lwter.read_data()
        if resp:
            resp_list.append(resp)
            # print(resp)

        if time.time() - start > 6:
            print("计算时间：{}".format(start - time.time()))
            print(resp_list)
            break
