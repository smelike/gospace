import sys
import serial
import serial.tools.list_ports


class Ser:

    def __init__(self):
        port_list = list(serial.tools.list_ports.comports())
        
        if len(port_list) <= 0:
            print("No serial devices online, please check the connect line.")
        else:
            # print(port_list)
            for k, _ in enumerate(port_list):
                print(port_list[k])
                port = port_list[k][0]
                print(port, port[k][1])
        
    # send_break(duration = 0.25)
    # break_condition
    # def ser_send(self, data, timebreak = ):




if __name__ == "__main__":
    ser = Ser()