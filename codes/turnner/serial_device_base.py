import serial

# 串口设备的父类

class SerialDeviceBase:
    """
    Base class for serial devices.
    """
    def __init__(self, port: str, baudrate: int, timeout: float = 0.01):
        """
        Initialize a new instance of the SerialDeviceBase class.

        :param port: The port to connect to.
        :param baudrate: The baud rate.
        :param timeout: timeout (float) – Set a read timeout value in seconds.
        timeout = None, 永远处于等待，或收到请求的字节数后，立即返回。必须要与 read() 或 read_until(expected=LF, size=None) 一起使用。
        timeout = 0, 立即返回，无论是否有数据。上限就是返回所要求的字节数。
        timeout = x, 请求数据是可用时，就立刻返回；否则，等待 x 秒，并返回所有收到的字节数。
        （考虑到设备的响应时间，一般 timeout = 0.015~0.025）
        """
        self.ser = None
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.modbus_cmd = ""
        # self.open_port()

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
    
    def read_data(self, len: int = 0) -> bytes:
        if self.open_port():
            return self.ser.readall()
        if self.open_port and len:
            return self.ser.read(len)
        print("not open port")
        return False
    # 执行指令，并返回响应值
    def execute_command(self, modbus_cmd: bytes) -> bytes:
        self.modbus_cmd = modbus_cmd
        bytes_written =  0
        resp = False
        if self.open_port() and not self.ser.in_waiting:
            bytes_written = self.ser.write(self.modbus_cmd)
            # print("out_waiting:", self.ser.out_waiting)
            # print("in_waiting:", self.ser.in_waiting)
            # time.sleep(0.05)
            if bytes_written:
                while not self.ser.out_waiting and not resp:
                    resp = self.ser.readall()
                    # resp = self.ser.read(self.ser.in_waiting)
                # print(resp)
                # self.ser.flush()
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