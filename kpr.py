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

# 注意事项：
# 通电时，传感器会进行自动置零操作。如果称台上有货物，则零点会被设置为负值。

import time
class Kpr(SerialDeviceBase):

    # 分度值,应该是在初始化读取配置出来
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
        # print(weight_hex_value.hex("-"))
        # 获取高位和低位的测量数据
        sp = weight_hex_value.split(",")[3:7]
        # 十六进制转换为十进制，并乘以分度值
        print(sp)
        # exit()
        if sp and len(sp) > 0:
            calc_weight = int("".join(sp), 16) * 0.01 
            weight_dec = round(calc_weight, 3)
            return [sp, weight_dec]
    

    # 对重量为负的情况进行处理
    # 如：返回值为 'ff', 'ff', 'ff', 'd4'
    def calc_weight_neg(self, weight_hex_value):
        pass
    # 'ff', 'ff', 'ff', 'd4'
    # ffffffd4 - ffffffff + 1

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
    
    # 置零，有货物在称台上，置零操作会导致零点被设置为该重量值。
    #  b'\x01\x10\x00^\x00\x01`\x1b'
    def set_zero(self):
        modbus = "01 10 00 5E 00 01 02 00 01 6A EE"
        modbus = bytes.fromhex(modbus)
        resp = self.execute_command(modbus)
        return resp

    # 设置分度
    def set_scale(self):

        # 01 10 00 58 00 01 02 00 09 6B 4E 
        # 称台分度值；使用称台功能前需先设置此值。
        # 0x00:0.0001   0x01:0.0002   0x02:0x0005
        # 0x03:0.001    0x04:0.002    0x05:0.005
        # 0x06:0.01     0x07:0.02     0x08;0.05
        # 0x09:0.1      0x0A:0.2      0x0B:0.5
        # 0x0C:1        0x0D:2        0x0E:5
        # 0x0F:10       0x10:20       0x11:50
        pass

    # 应答延时设置
    def set_response_delay(self):
        # 当延时10ms时，转换成十六进制为0A。
        # 指令格式：01 10 00 04 00 01 02 00 0A 27 D3
        # 单位为ms，应答延时用于RS485通信，因为RS485是半双工，只能发或收，不能同时发收。
        # 有些主机收发切换比较慢，导致应答指令丢失，所以通过合理设置应答延时时间可避免指令丢失。
        pass

    # 判稳定范围
    def set_stability_range(self):
        # 判稳范围（098）
        # 指令格式：01 10 00 62 00 01 02 00 64 AF F9（设置100d时）
        pass

    # 判稳时间设置
    def set_stability_time(self):
        # 01 10 00 63 00 01 02 00 0A 2F C4
        pass

    # 设置最大称量
    def set_max_weight(self):
        # 01 10 00 56 00 02 04 00 00 27 10 6C 85（假设输入10000）
        pass

    # 设置滤波
    def set_filter_type(self):
        # 默认为09：滑动平均滤波+一阶滤波，改为08：中位值滤波+一阶滤波时
        # 指令格式：01 10 00 22 00 01 02 00 08 A1 14
        # 根据不同应用场合选择合适的滤波方式
        # 0x00:不使用       0x01:平均值滤波
        # 0x02:中位值滤波   0x03:一阶滤波
        # 0x04:滑动平均滤波 0x05:中位值平均滤波
        # 0x06:滑动中位值平均滤波
        # 0x07:平均值滤波 + 一阶滤波
        # 0x08:中位值滤波 + 一阶滤波
        # 0x09:滑动平均滤波 + 一阶滤波
        # 0x0A:中位值平均滤波 + 一阶滤波

        pass


if __name__ == "__main__":

    # 测试1 
    # kpr = Kpr("COM3", 19200)
    
    # 测试2
    kpr = Kpr("COM6", 19200, 0.02)
    # print("置零", kpr.set_zero())
    start = time.time()
    resp = []
    while True:
        # 01 03 04 ff ff ff ff fb a7
        # remove_stick = kpr.remove_stick()
        # print("去皮：", remove_stick)
        retbytes = kpr.get_weight_value()
        # response = " ".join(map(lambda x: "%02x" % x, retbytes))
        if retbytes:
            # time.sleep(2)
            weight_dec = kpr.calc_weight(retbytes.hex(","))
            # print(response)
            resp.append(weight_dec) 
        
        if time.time() - start >= 1:
            time_elapsed = "计算时间：{}".format(start - time.time())
            print(time_elapsed)
            break
        # time.sleep(1)
    print(len(resp), resp)
    

