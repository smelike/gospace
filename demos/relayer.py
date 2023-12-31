import sys
import time
import serial
import serial.tools.list_ports

# 定义一个类，用于实现朗汉得 LH-IO404 继电器控制
# LH-IO404 四路输入 DI，四路输出 DO，四路继电器控制


## 两路光电，通过出货口的光电状态，来决定电机的是否暂停和转动吗？

class Relayer:

    # 是否在过货的状态, -1 - 默认，1 - 过货遮挡，0 -  未遮挡
    do_status = -1

    def __init__(self):
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) <= 0:
            print("no serial devices.")

        self.ser = serial.Serial("COM5", 9600, timeout=0.02)
        self.ser.flushInput()
    
    # 查询四路开关量输入状态
    def read_di_status(self):
        # 使用循环监听，读取多少秒
        cmd = "FE 02 00 00 00 04 6D C6"
        self.ser.write(bytes.fromhex(cmd))
        resp = self.ser.readall()
        # 第四字节是开关量的状态值，如 01，代表的是高位在前，低位在后，01 转换为二进制 00 01
        status_str = ' '.join(
            map(lambda x: '%02x' % x, resp)
            )
        return status_str

    # 查询是否在进货或出货
    def read_do_status(self): 
       
        status0 = []
        status1 = []
        while True:
            result = relayer.execute_command("FE 02 00 00 00 04 6D C6")
            str = " ".join(map(lambda x: "%02X" % x, result))
           
            if(result[3] > 0):
                print("遮挡")
                self.do_status = 1
                status1.append(str)
            else:
                print("未遮挡")
                # 未遮挡时，0 和 1 都是有状态值的，代表着货物过完了
                if len(status1) and (self.do_status == 1): 
                    self.do_status = 0
                    status1.append(str)
                    status0.clear()
                status0.append(str)
               
            # 清除数据，防止空转时，数据堆积，光电回到默认值
            if self.do_status == 0:
                print(status0, status1)
                self.do_status = -1
                status0.clear()
                status1.clear()
                # break
                
    # 打开关闭继电器
    def switch_relay(self, number):
        if number == 1:
            opens = "FE 05 00 00 FF 00 98 35"
            close = "FE 05 00 00 00 00 D9 C5"
        elif number == 2:
            opens = "FE 05 00 01 FF 00 C9 F5"
            close = "FE 05 00 01 00 00 88 05"
        elif number == 3:
            opens = "FE 05 00 02 FF 00 39 F5"
            close = "FE 05 00 02 00 00 78 05"
        elif number == 4:
            opens = "FE 05 00 03 FF 00 68 35"
            close = "FE 05 00 03 00 00 29 C5"
        else:
            # 全开
            opens = "FE 0F 00 00 00 04 01 0F 31 96"
            # 全闭
            close = "FE 0F 00 00 00 04 01 00 71 92"
        

    def execute_command(self, command):
        while True:
            self.ser.write(bytes.fromhex(command))
            # 10ms 后再读取, 防止读取不到数据
            # 10ms 是可以取到最多 14 条数据
            time.sleep(0.01) 
            result = self.ser.readall()
            if self.ser.in_waiting > 0:
                break
            return result

if __name__ == "__main__":
    relayer = Relayer()
    relayer.read_do_status()
    # x = 2
    # xr = lambda x: "%02X" % x
    # print(xr(0))
