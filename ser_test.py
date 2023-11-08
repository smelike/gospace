import sys
import serial
import time
import serial.tools.list_ports

class Sertest:

    serial_port = dict()
    baudrate = [9600, 19200, 115200]
    def __init__(self):
        port_list = list(serial.tools.list_ports.comports())
        for port in port_list:
            for b in self.baudrate:
                ser = serial.Serial(port[0], b, timeout=0.05)
                if ser.is_open and (b == 9600):
                    time.sleep(0.02)
                    wlen = ser.write(bytes.fromhex("FE0100000002A9C4"))
                    resp = ser.readall()
                    print("jidianqi", resp)
                    break
                elif ser.is_open and (b == 19200):
                    ser.write(bytes.fromhex("0106200000054209"))
                    resp = ser.readall()
                    print("zhongda", resp)
                    break
                elif ser.is_open and (b == 115200):
                    ser.write(bytes.fromhex("03 03 00 00 00 0F 04 2C"))
                    resp = ser.readall()
                    print("gaodu", resp)
                    break
                else:
                    print("open failed")
                    break

        exit()    
        print(port_list)
        if len(port_list) <= 0:
            print("No serial devices online, please check the connect line.")
            exit()
        for k, val in enumerate(port_list):
            print(port_list[k],val)
            port = list(val)
            print(port)

if __name__ == "__main__":

    test = Sertest()