import sys
import time
import serial
import serial.tools.list_ports



class Relayer:

    def __init__(self):
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) <= 0:
            print("no serial devices.")

        self.ser = serial.Serial("COM5", 9600, timeout=0.02)
        

    def execute_command(self, command):
        while True:
            self.ser.write(bytes.fromhex(command))
            time.sleep(0.1)
            result = self.ser.readall()
            if self.ser.in_waiting > 0:
                break
            return result

if __name__ == "__main__":
    relayer = Relayer()
    result = relayer.execute_command("FE 02 00 00 00 04 6D C6")
    # result = bytes('FF', "utf-8")
    str = " ".join(map(lambda x: "%02X" % x, result))
    # lambda x: "0x%02x" % x
    # 0xfe 0x02 0x01 0x08 0x90 0x5a
    print(result)
    print(str)
    x = 2
    xr = lambda x: "%02X" % x
    print(xr(0))
