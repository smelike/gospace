import serial
import time

from serial.serialutil import to_bytes

# 串口设备的父类

class serial_device_base:

    ser = None
    port = ""
    baudrate = ""
    modbus_cmd = ""


    def __init__(self, port : str, baudrate : int, ):
        self.port = port
        self.baudrate = baudrate
        print(port, baudrate)
        # self.modbus_cmd = modbus_cmd
        # pass

    def open_port(self):
        if self.port and self.baudrate:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=0.02)
        return True if self.ser and self.ser.is_open else False
    
    # 执行指令，并返回响应值
    def execute_command(self, modbus_cmd: bytes) -> bytes:
        self.modbus_cmd = modbus_cmd
        bytes_written =  0
        resp = False
        if self.open_port() and not self.ser.in_waiting:
            bytes_written = self.ser.write(self.modbus_cmd)
            # print(self.ser.out_waiting)
            # time.sleep(0.05)
            if bytes_written:
                while not self.ser.out_waiting:
                    resp = self.ser.readall()
                    print(resp)
                # self.ser.flush()
        return resp

    # 退出时，做了串口的关闭，防止串口的占用
    # def __exit__(self):
    #     self.ser.close()


if __name__ == "__main__":
    base = serial_device_base("COM5", 9600)
    cmd = "FE0100000002A9C4"
    cmd = bytes.fromhex(cmd)
    print(cmd)
    print(base.execute_command(cmd))