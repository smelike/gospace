import sys
import serial
import time
import serial.tools.list_ports

class Sertest:

    serial_port = dict()
    comports = list()
    ser = None
    def __init__(self):
        self.comports = serial.tools.list_ports.comports()
        # print(port_list)
        
        if len(self.comports) <= 0:
            exit("No serial devices online, please check the connect line.")

    def run(self):
        for port in self.comports:
            print(port, port[0])
            if self.device_detect(port[0]):
                self.comports.remove(port)

    def open_port(self, port, baudrate, timeout=0.05):
        # Open serial port
        try:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)
        except IOError as e:
            print(e)
            return None
        
    def read_data(self):
        # Read data from serial port
        data = False
        print(self)
        try:
            if self.ser.in_waiting:
                data = self.ser.readall()
        except AttributeError as e:
            print(e)
        return data

    def write_data(self, data):
        # Write data to serial port
        # print(self.ser)
        bytes_written = 0
        try:
           if self.ser.is_open:
            bytes_written = self.ser.write(data)
        except AttributeError as e:
            print("Error writing to serial port: ", e)
        return bytes_written > 0

    def device_detect(self, port):
        self.open_port(port, 9600, timeout=0.05)
        ok = self.write_data(bytes.fromhex("FE0100000002A9C4"))
       
        if ok:
            resp = self.read_data()
            print("jidianqi:", resp)
            self.ser.close()
            return True
        self.open_port(port, 19200, timeout=0.05)               
        ok = self.write_data(bytes.fromhex("0106200000054209"))
        
        if ok:
            resp = self.read_data()
            print("zhongda", resp)
            self.ser.close()
            return True
        
        self.open_port(port, 115200, timeout=0.05)
        ok = self.write_data(bytes.fromhex("03 03 00 00 00 0F 04 2C"))
        if ok:
            resp = self.read_data()
            print("gaodu", resp)
            self.ser.close()
            return True

        self.open_port(port, 115200, timeout=0.05)
        resp = self.read_data()
        if resp:
            print("changkuan", resp)
            self.ser.close()
            return True
        return False

    def __exit__(self):
        self.ser.close()

    

if __name__ == "__main__":

    test = Sertest()
    test.run()