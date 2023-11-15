import sys
import ser
from serial_device_base import SerialDeviceBase

# 高光幕
class Highter(SerialDeviceBase):

    def __init__(self, *args, **kwargs):
        # 串口
       super(Highter, self).__init__(*args, **kwargs)

    def formatHex(argv):
        result = ''
        hLen = len(argv)
        for i in range(hLen):
            if isinstance(argv[i], int):
                hvol = argv[i]
            else:
                hvol = ord(argv[i])
            hhex = '%02x' % hvol
            result += hhex + ' '
        return result

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
    highter = Highter("COM8", 115200)
    modbus = "03 03 00 00 00 0F 04 2C"
    modbus = bytes.fromhex(modbus)
    while True:
        resp = highter.execute_command(modbus)
        print(resp)
   