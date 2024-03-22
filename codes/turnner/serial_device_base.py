# 串口设备的父类

from __future__ import absolute_import
from serial.serialutil import SerialException, PortNotOpenError, SerialTimeoutException

import serial
import time

# from common import fn


# 串口设备的父类
class SerialDeviceBase:
    """
    Base class for serial devices.
    """

    def __init__(self, port: str, baudrate: int, timeout: float = 0.01,):
        """
        Initialize a new instance of the SerialDeviceBase class.

        :param port: The port to connect to.
        :param baudrate: The baud rate.
        :param timeout: timeout (float) – Set a read timeout value in seconds.
        timeout = None, 永远处于等待,或收到请求的字节数后,立即返回。必须要与 read() 或 read_until(expected=LF, size=None) 一起使用。
        timeout = 0, 立即返回,无论是否有数据。上限就是返回所要求的字节数。
        timeout = x, 请求数据是可用时,就立刻返回;否则,等待 x 秒,并返回所有收到的字节数。
        (考虑到设备的响应时间,一般 timeout = 0.015~0.025)
        """
        self.ser = None
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.modbus_cmd = ""
        
    # AttributeError: 'NoneType' object has no attribute 'is_open'
    def open_port(self):
       if self.ser is None:
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        except SerialException as e:
            raise e
        
    def read_data(self, len: int = 0) -> bytes:
        if self.ser is not None:
            if len:
                data_readed = self.ser.read(len)
            else:
                data_readed = self.ser.readall()
            return data_readed
        return False
    

    # 执行指令,并返回响应值
    def execute_command(self, modbus_cmd: bytes) -> bytes:
        self.modbus_cmd = modbus_cmd
        bytes_written = 0
        resp = False
        
        if self.ser is not None:
            if self.ser.in_waiting:
                # 有排队等待的状况，则做sleep 3s 处理（待观察调整）
                time.sleep(3)
                bytes_written = self.ser.write(self.modbus_cmd)
                if bytes_written:
                    while not self.ser.out_waiting and not resp:
                        resp = self.ser.readall()
                # fn.logger(resp)
                # self.ser.flush()
        return resp

    # 写入命令的排队队列
    def __command_queue(self):
        pass

    # 退出时,做了串口的关闭,防止串口的占用
    def __exit__(self):
       if self.ser is not None:
         self.ser.__del__()
        # serial.close() # close() is a method of serial.Serial object, Close port immediately.
        # serial.__del__() # close() Close port when serial port instance is free.


if __name__ == "__main__":
    base = SerialDeviceBase("COM5", 19200)
    cmd = "FE0100000002A9C4"
    cmd_hex = bytes.fromhex(cmd)
    print(cmd)
    print(cmd_hex)
    print(base.execute_command(cmd_hex))
