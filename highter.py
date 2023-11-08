import sys
import ser


# 高光幕
class Highter:

    def __init__(self):
        # 串口
        ser = serial.Serial("COM8", 115200, timeout=0.05)
        result = data_parse.hexShow(SerialOp.read(1000))

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
