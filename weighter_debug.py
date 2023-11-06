import time
import tkinter as tk
import serial
import serial.tools.list_ports

port = "COM5"
port_list = list(serial.tools.list_ports.comports())


def hexShow(argv):
    """
    分割十六进制数据
    :param argv: 16进制字节流 b'\x00\x01\x02\x03\x04\x05'
    :return: 字符串 '00 01 02 03 04 05 '
    """
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


# 检测
for k, _ in enumerate(port_list):
    portTmp = list(port_list[k])
    # 长宽
    try:
        if portTmp[0] in ["COM8", "COM9"]:
            continue
        SerialOp = serial.Serial(portTmp[0], 9600, timeout=0.05)
        SerialOp.write(bytes.fromhex('FE 01 00 00 00 10 29 C9'))
        # SerialOp.write(bytes.fromhex("FE0100000002A9C4"))
        response = SerialOp.readall()
        result = ' '.join(map(lambda x: '%02x' % x, response)).strip()
        if len(result) == 20:
            port = portTmp[0]
            print(port)
            SerialOp.close()
            break
        SerialOp.close()
    except Exception as e:
        print(f"发生错误:{e}")


class motor:
    def __init__(self):
        global port
        if port is None:
            print("未检测到串口")
        else:
            self.relay_serial = serial.Serial(port, 9600, timeout=1)
        self.relay_writing = False

    def relay_write(self, code_str):
        """
        继电器写入命令
        :param code_str: 写入命令
        :return:
        """
        while True:
            if self.relay_writing:
                time.sleep(0.01)
                continue
            else:
                self.relay_writing = True
                self.relay_serial.write(bytes.fromhex(code_str))
                result = self.relay_serial.readall()
                self.relay_writing = False
                return result

    def open_1(self):
        self.relay_write('FE 05 00 00 FF 00 98 35')

    def close_1(self):
        self.relay_write('FE 05 00 00 00 00 D9 C5')

    def open_2(self):
        self.relay_write('FE 05 00 01 FF 00 C9 F5')

    def close_2(self):
        self.relay_write('FE 05 00 01 00 00 88 05')

    def open_3(self):
        self.relay_write('FE 05 00 02 FF 00 39 F5')

    def close_3(self):
        self.relay_write('FE 05 00 02 00 00 78 05')

    def open_4(self):
        self.relay_write('FE 05 00 03 FF 00 68 35')

    def close_4(self):
        self.relay_write('FE 05 00 03 00 00 29 C5')

    def open_5(self):
        self.relay_write('FE 05 00 04 FF 00 D9 F4')

    def close_5(self):
        self.relay_write('FE 05 00 04 00 00 98 04')

    def open_6(self):
        self.relay_write('FE 05 00 05 FF 00 88 34')

    def close_6(self):
        self.relay_write('FE 05 00 05 00 00 C9 C4')

    def open_7(self):
        self.relay_write('FE 05 00 06 FF 00 78 34')

    def close_7(self):
        self.relay_write('FE 05 00 06 00 00 39 C4')

    def open_8(self):
        self.relay_write('FE 05 00 07 FF 00 29 F4')

    def close_8(self):
        self.relay_write('FE 05 00 07 00 00 68 04')

    def open_9(self):
        self.relay_write('FE 05 00 08 FF 00 19 F7')

    def close_9(self):
        self.relay_write('FE 05 00 08 00 00 58 07')

    def open_10(self):
        self.relay_write('FE 05 00 09 FF 00 48 37')

    def close_10(self):
        self.relay_write('FE 05 00 09 00 00 09 C7')

    def open_11(self):
        self.relay_write('FE 05 00 0A FF 00 B8 37')

    def close_11(self):
        self.relay_write('FE 05 00 0A 00 00 F9 C7')

    def open_12(self):
        self.relay_write('FE 05 00 0B FF 00 E9 F7')

    def close_12(self):
        self.relay_write('FE 05 00 0B 00 00 A8 07')

    def open_13(self):
        self.relay_write('FE 05 00 0C FF 00 58 36')

    def close_13(self):
        self.relay_write('FE 05 00 0C 00 00 19 C6')

    def open_14(self):
        self.relay_write('FE 05 00 0D FF 00 09 F6')

    def close_14(self):
        self.relay_write('FE 05 00 0D 00 00 48 06')

    def open_15(self):
        self.relay_write('FE 05 00 0E FF 00 F9 F6')

    def close_15(self):
        self.relay_write('FE 05 00 0E 00 00 B8 06')

    def open_16(self):
        self.relay_write('FE 05 00 0F FF 00 A8 36')

    def close_16(self):
        self.relay_write('FE 05 00 0F 00 00 E9 C6')

    def modules1_rise(self):
        self.open_1()
        self.open_2()
        self.close_3()
        self.close_4()

    def modules1_decline(self):
        self.open_3()
        self.open_4()
        self.close_2()
        self.close_1()

    def modules2_rise(self):
        self.open_5()
        self.open_6()
        self.close_7()
        self.close_8()

    def modules2_decline(self):
        self.open_7()
        self.open_8()
        self.close_5()
        self.close_6()

    def modules3_rise(self):
        self.open_9()
        self.open_10()
        self.close_11()
        self.close_12()

    def modules3_decline(self):
        self.open_11()
        self.open_12()
        self.close_9()
        self.close_10()

    def modules4_rise(self):
        self.open_13()
        self.open_14()
        self.close_15()
        self.close_16()

    def modules4_decline(self):
        self.open_15()
        self.open_16()
        self.close_13()
        self.close_14()


# 初始化
relay = motor()


def on_button1_clicked():
    print("Button 1 clicked")
    relay.modules1_rise()
    relay.modules2_decline()
    relay.modules3_decline()
    relay.modules4_decline()


def on_button2_clicked():
    print("Button 2 clicked")
    relay.modules1_decline()
    relay.modules2_rise()
    relay.modules3_decline()
    relay.modules4_decline()


def on_button3_clicked():
    print("Button 3 clicked")
    relay.modules1_decline()
    relay.modules2_decline()
    relay.modules3_rise()
    relay.modules4_decline()


def on_button4_clicked():
    print("Button 4 clicked")
    relay.modules1_decline()
    relay.modules2_decline()
    relay.modules3_decline()
    relay.modules4_rise()


if __name__ == '__main__':
    root = tk.Tk()
    # 界面设置
    root.geometry('900x850+{}+{}'.format(
        (root.winfo_screenwidth() - 1000) // 2, 
        (root.winfo_screenheight() - 800) // 2
        )
    )
    root.title("砝码矫正程序")

    button1 = tk.Button(root, text='Button 1', padx=200, pady=200, command=on_button1_clicked)
    button2 = tk.Button(root, text='Button 2', padx=200, pady=200, command=on_button1_clicked)
    button3 = tk.Button(root, text='Button 3', padx=200, pady=200, command=on_button1_clicked)
    button4 = tk.Button(root, text='Button 4', padx=200, pady=200, command=on_button1_clicked)

    # 将四个按钮按田字形排列
    button1.grid(row=0, column=0, sticky='nsew')
    button2.grid(row=0, column=2, sticky='nsew')
    button3.grid(row=2, column=0, sticky='nsew')
    button4.grid(row=2, column=2, sticky='nsew')
    root.mainloop()
