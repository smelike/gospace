import serial
import time

# 串口设备的父类

import serial
import time

class SerialDeviceBase:
    """
    Base class for serial devices.
    """

    def __init__(self, port: str, baudrate: int, timeout: int = 0):
        """
        Initialize a new instance of the SerialDeviceBase class.

        :param port: The port to connect to.
        :param baudrate: The baud rate.
        :param timeout: The timeout value.
        """
        self.ser = None
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.modbus_cmd = ""

    def open_port(self):
        if isinstance(self.ser, serial.Serial):
            return True
        if self.port and self.baudrate:
            self.ser = serial.Serial(self.port, self.baudrate, timeout = self.timeout)
            if not self.ser.is_open:
                print("open port success")
                return False
            # if self.ser.timeout == 0.015:
            #     print("open port timeout")
            #     return False
            return True
        return False
    
    def read_data(self):
        if self.open_port():
            return self.ser.readall()
        print("not open port")
        return False
    # 执行指令，并返回响应值
    def execute_command(self, modbus_cmd: bytes) -> bytes:
        self.modbus_cmd = modbus_cmd
        bytes_written =  0
        resp = False
        # print(self.open_port())
        exit_flag = False
        if self.open_port() and not self.ser.in_waiting:
            bytes_written = self.ser.write(self.modbus_cmd)
            # print(self.ser.out_waiting)
            # time.sleep(0.05)
            if bytes_written:
                while not self.ser.out_waiting and not resp:
                    resp = self.ser.readall()
                # print(resp)
                self.ser.flush()
        return resp

    # 写入命令的排队队列
    def __command_queue(self):
        pass
    # 退出时，做了串口的关闭，防止串口的占用
    def __exit__(self):
        self.ser.__del__()
        # serial.close() # close() is a method of serial.Serial object, Close port immediately.
        # serial.__del__() # close() Close port when serial port instance is free. 


if __name__ == "__main__":
    base = SerialDeviceBase("COM5", 9600)
    cmd = "FE0100000002A9C4"
    cmd = bytes.fromhex(cmd)
    print(cmd)
    print(base.execute_command(cmd))