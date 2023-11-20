from serial_device_base import SerialDeviceBase

# 指令格式：模块地址+功能代码+数据+CRC16校验
# 如：01 03 00 50 00 02 c4 1a, 
# 01 模块地址，03 (读寄存器)功能代码，0050 - 寄存器起始位置，00 02 - 寄存器数量，c41a CRC16校验
# 功能代码：01 -> 

# 皮重(084)
# 指令格式：01 10 00 54 00 02 04 00 00 00 00 64 F6 8B（假设皮重为100）

# 皮重值;范围:-8000000~8000000;写入0x7fffffff执行自动去皮
# 当设备称重的物品有包装时，如果我们只需要称重物品自身的重量，就要把包装物作为皮重预去除。
# 可以把包装实物直接放在称台上，然后去皮，写入0x7fffffff执行自动去皮。
# 如果包装不便分开，而且已知包装的重量，则可以通过发送指令把皮重重量输入称重设备，这个就是所谓的数字去皮。

import time
class Kpr(SerialDeviceBase):

    def __init__(self, *args, **kwargs):
        # print(*args)
        super(Kpr, self).__init__(*args, **kwargs)

    def get_weight_value(self):
        modbus = "010300500002c41a"
        modbus = bytes.fromhex(modbus)
        resp = self.execute_command(modbus)
        return resp
    
    # 计算十进制的重量
    def calc_weight(self, weight_hex_value):
        sp = weight_hex_value.split(" ")[3:7]
        calc_weight = int("".join(sp), 16) * 0.001
        weight_dec = round(calc_weight, 3)
        return [sp, weight_dec]
    

    # 对重量为负的情况进行处理
    # 如：返回值为 'ff', 'ff', 'ff', 'd4'
    def calc_weight_neg(self, weight_hex_value):
        pass

    # 去皮
    def remove_stick(self):
        modbus = "01 10 00 54 00 02 04 7f ff ff ff df 34"
        modbus = bytes.fromhex(modbus)
        resp = self.execute_command(modbus)
        return resp
    
    # 获取净重
    def get_net_weight(self):
        modbus = "01 03 00 52 00 02 65 DA"
        modbus = bytes.fromhex(modbus)
        resp = self.execute_command(modbus)
        return resp
    
    # 置零
    #  b'\x01\x10\x00^\x00\x01`\x1b'
    def set_zero(self):
        modbus = "01 10 00 5E 00 01 02 00 01 6A EE"
        modbus = bytes.fromhex(modbus)
        resp = self.execute_command(modbus)
        return resp


if __name__ == "__main__":

    # 测试1 
    # kpr = Kpr("COM3", 19200)
    
    # 测试2
    kpr = Kpr("COM6", 19200, 0.02)
    print("置零", kpr.set_zero())
    start = time.time()
    resp = []
    while True:
        # 01 03 04 ff ff ff ff fb a7
        # remove_stick = kpr.remove_stick()
        # print("去皮：", remove_stick)
        retbytes = kpr.get_weight_value()
        response = " ".join(map(lambda x: "%02x" % x, retbytes))
        weight_dec = kpr.calc_weight(response)
        # print(response)
        resp.append(weight_dec)
        if time.time() - start > 6:
            time_elapsed = "计算时间：{}".format(start - time.time())
            print(time_elapsed)
            break
        # time.sleep(1)
    print(len(resp), resp)
    

