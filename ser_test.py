import sys
import serial
import time
import serial.tools.list_ports

class Sertest:

    serial_port = dict()

    def __init__(self):
        port_list = serial.tools.list_ports.comports()
        print(port_list)
        
        if len(port_list) <= 0:
            print("No serial devices online, please check the connect line.")
            exit()

        # exit()
        # print(port_list.keys(), port_list.values())
        for port in port_list:
            ser = serial.Serial(port[0], 9600, timeout=0.05)
            wlen = ser.write(bytes.fromhex("FE0100000002A9C4"))
            resp = ser.readall()
            print("jidianqi", resp)
            ser.close()

            ser = serial.Serial(port[0], 19200, timeout=0.05)               
            ser.write(bytes.fromhex("0106200000054209"))
            resp = ser.readall()
            print("zhongda", resp)
            ser.close()
            
            ser = serial.Serial(port[0], 115200, timeout=0.05)
            ser.write(bytes.fromhex("03 03 00 00 00 0F 04 2C"))
            resp = ser.readall()
            print("gaodu", resp)
            ser.close()

            ser = serial.Serial(port[0], 115200, timeout=0.05)
            resp = ser.readall()
            if resp:
                print("resp", resp)
            else:
                print("no resp")
            print("changkuan\r\n", resp)
            ser.close()

if __name__ == "__main__":

    test = Sertest()