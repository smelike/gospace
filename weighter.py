import json
import math
import serial
import time
from common import sys_data, data_parse, fn
from copy import deepcopy


class Weigh:
    def __init__(self):
       self.w_serial_port = list()
       self.supply = "kpr"
       self.simulation = 0
       self.init_serial()

    def init_serial(self):
        if self.simulation != 2:
            self.serial = serial.Serial(
                "COM7", 19200, 0.015
                )
        else:
            self.serial = None

    # 获取厂商的 modbus 指令
    def modbus_cmd(self, modbus): 
        if self.supply == 'kpr':
            modbus = "010300500002c41a"
        elif self.supply == 'xy':
            modbus = "010300000002c40b"
        else:
            modbus = "010300500002c41a"
        return modbus
    
    # 写串口后，读取串口的返回数据
    def get_weight_value(self, weight_val):
        cmd = self.modbus_cmd()
        self.serial.write(bytes.fromhex(cmd))
        resp = self.serial.readall()
        weight_val = ' '.join(
            map(lambda x: '%02x' % x, resp)
            )
        return weight_val

    def run(self):

        modbus_cmd = self.modbus_cmd()
        last_count_time = 0
        serial_read_speed_interval = 5
        serial_read_speed_count = 0
        while True:
            try:
                if len(self.w_serial) > 0:
                    msg_data = self.w_serial.pop(0)
                    self.weight_serial.write(bytes.fromhex(msg_data))
                    response = self.weight_serial.readall()
                    response_str = ' '.join(map(lambda x: '%02x' % x, response))
                    fn.logger(f"去皮操作", level='info', r_path=sys_data.r_path)
                    continue
                if sys_data.web_api.config["simulation"] == 0:
                    self.weight_serial.write(bytes.fromhex(modbus_cmd))
                    response = self.weight_serial.readall()
                    response_str = ' '.join(map(lambda x: '%02x' % x, response))
                if sys_data.web_api.config["simulation"] == 1:
                    self.weight_serial.write(bytes.fromhex(modbus_cmd))
                    response = self.weight_serial.readall()
                    response_str = ' '.join(map(lambda x: '%02x' % x, response))
                    if sys_data.simulation_temp:
                        sys_data.simulation["weight"].append([response_str, str(time.time())])
                    else:
                        sys_data.simulation_temp_data["weight"].append([response_str, str(time.time())])
                if sys_data.web_api.config["simulation"] == 2:
                    if sys_data.simulation["weight"]:
                        if time.time() - float(sys_data.simulation["weight"][0][1]) - self.d_value_time >= 0:
                            response_str = sys_data.simulation["weight"][0][0]
                            sys_data.simulation["weight"].pop(0)
                        else:
                            time.sleep(0.01)
                            continue
                    else:
                        fn.logger(f"重量仿真结束", level='info', r_path=sys_data.r_path)
                        time.sleep(5000)
                        continue
                # 规避应答指令丢失
                if response_str == "":
                    continue
                # 规避未知读取不到的错误
                if is_kpr:
                    is_complement, ture_form = self.check_data(
                        bin(int("".join(response_str.split(" ")[3:7]), 16))[2:].zfill(32))
                    if is_complement:
                        current_weight = round(-int(ture_form, 2) * 0.01, 3)
                    else:
                        current_weight = round(int(ture_form, 2) * 0.01, 3)
                # elif sys_data.web_api.config["weight_module"] == 'xy':
                else:
                    current_weight = round(int("".join(response_str.split(" ")[3:7]), 16) * 0.001, 3)
                if time.time() - self.send_time > 0.5:
                    self.send_time = int(time.time())
                    sys_data.debug_data["weight"] = str(current_weight)
                    # sys_data.web_api.window.evaluate_js('update_current_weight(' + str(current_weight) + ')')
                # 检测重量 最小重量
                if self.last_weight <= self.min_weight <= current_weight and current_weight > 0:
                    sys_data.data_dict["current_weight"] = True
                    self.current_weight = True
                if self.last_weight > self.min_weight >= current_weight >= 0:
                    sys_data.data_dict["current_weight"] = False
                    self.current_weight = False
                    self.t_motor.create_thread(func=self.event_end)
                # fn.dp(current_weight)
                self.last_weight = current_weight
                if not sys_data.weight_recode_list:
                    sys_data.weight_recode_list.append({"weight": current_weight, "time": time.time()})
                else:
                    if time.time() - sys_data.weight_recode_list[-1]["time"] >= 0.5:
                        sys_data.weight_recode_list.append({"weight": current_weight, "time": time.time()})
                if len(sys_data.weight_recode_list) > 4:
                    sys_data.weight_recode_list.pop(0)
                if self.recode and self.current_weight:
                    self.weight_data.append(current_weight)
                if current_weight > self.min_weight:
                    self.effective_values.append(current_weight)
                else:
                    if len(self.effective_values) > 0:
                        fn.dp(self.effective_values, len(self.effective_values), level='weight_effective_values')
                    self.effective_values = []
                if sys_data.debug and len(fn.debug_levels) > 0:
                    serial_read_speed_count += 1
                    int_time = int(time.time())
                    if int_time != last_count_time and int_time % serial_read_speed_interval == 0:
                        last_count_time = int_time
                        fn.dp('weight serial read speed count', serial_read_speed_count, level='weighting_serial_speed')
                        serial_read_speed_count = 0
            except Exception as e:
                fn.logger(f"重量读取失败：{e}", level='error', r_path=sys_data.r_path)
            time.sleep(0.0001)

    @staticmethod
    def check_data(ori_str: str):
        """
        检查是否为补码 输出 原码
        :param ori_str: 二进制字符串
        :return: bool:是否为整数，str:原码
        """
        # 检查是否为补码
        if ori_str[0] == "0":
            return False, ori_str
        elif ori_str[0] == "1":
            inverse_code = str(int(ori_str[1:]) - 1)
            # 反码再取反到原码
            true_form = ""
            for i in inverse_code.__iter__():
                if i == "0":
                    true_form += "1"
                else:
                    true_form += "0"
            return True, true_form

    @staticmethod
    def is_stable(weights, average_weight, precision):
        """
        重量减去平均值测量稳定性
        :param weights:[]:list
        :param average_weight:重量平均值
        :param precision:稳定性精度界限
        :return:0 or 平均值
        """
        count = len(weights)
        for index, number in enumerate(weights):
            if index == count - 1:
                continue
            if weights[index] - weights[index + 1] > precision:
                return False
        return True

    def get_stable_weight(self, weights):
        """
        拿到稳定的测量值，采用滑动窗口的形式
        :param weights: []:list
        :return: 0 or 平均值
        """
        try:
            count = int(sys_data.web_api.config.get('weight_stable_count'))
            iterations = int(sys_data.web_api.config.get('weight_stable_iteration_count'))
            precision = sys_data.web_api.config.get('weight_precision')
            for i in range(iterations):
                target_weights = weights[i:i + count]
                average_weight = sum(target_weights) / len(target_weights)
                if self.is_stable(target_weights, average_weight, precision):
                    return average_weight
            fn.logger(f"拿重量稳定值失败", level='error', r_path=sys_data.r_path)
            return 0
        except Exception as e:
            fn.logger(f"拿重量稳定值处理程序失败：{e}", level='error', r_path=sys_data.r_path)
            return 0

    @staticmethod
    def adjust_weight_value(weight):
        """
        矫正重量
        :param weight: 重量
        :return:
        """
        if weight == 0:
            return 0
        weight = weight + (weight * sys_data.web_api.config['weight_adjust_value'])
        if sys_data.web_api.config['weight_critical_value'] > 0:
            weight_array = math.modf(weight)
            if 0 < weight_array[0] < 0.5 and weight_array[0] + sys_data.web_api.config['weight_critical_value'] > 0.5:
                weight = weight_array[1] + 0.51
            elif 0.5 < weight_array[0] < 1 and weight_array[0] + sys_data.web_api.config['weight_critical_value'] > 1:
                weight = weight_array[1] + 1.01
        if sys_data.web_api.config['step_weight'] > 0:
            weight = math.ceil(weight / sys_data.web_api.config['step_weight']) * sys_data.web_api.config['step_weight']
        w = round(weight, 2)
        return w

    def event_start(self):
        """
        重量事件开始
        :return:
        """
        self.recode = True
        current_id = sys_data.data_dict.get('current_id', None)
        if current_id is not None:
            self.current_id = current_id
            return None
        fn.logger(f"当前没有id，测重失败", level='error', r_path=sys_data.r_path)

    def event_end(self):
        """
        重量事件结束
        :return:
        """
        fn.logger(f"重量回零", level='info', r_path=sys_data.r_path)

    def weigh_calculate(self):
        time.sleep(0.2)
        self.recode = False
        weights = deepcopy(self.weight_data)
        fn.logger(f"重量源数据：{str(weights)}")
        fn.logger(['超最小测量重量数据', self.effective_values])
        current_id = self.current_id
        self.weight_data = []
        try:
            if current_id is not None:
                if not len(weights):
                    sys_data.web_api.play_sound("fail_weight")
                    sys_data.data_dict["parcel_object_dict"][current_id]["status"] = 0
                    sys_data.data_dict["parcel_object_dict"][current_id]["info"] = "重量值测量失败,可能为出货口阻挡"
                    # 推送到前端
                    sys_data.web_api.parcel_update_data(current_id)
                weights.sort(reverse=True)
                # 取得稳定值
                weight = self.get_stable_weight(weights)
                # 重量矫正
                weight = round(self.adjust_weight_value(weight), 2)
                if sys_data.web_api.config.get("fixed_value", {}).get("weight", None):
                    fn.logger(f"修正重的固定值为：{sys_data.web_api.config['fixed_value']['weight']}")
                    weight = sys_data.web_api.config['fixed_value']['weight']
                sys_data.data_dict["parcel_object_dict"][current_id]["weight"] = weight
                fn.logger(['稳定的重量数据', sys_data.data_dict["order_recode"], weights, '数量'+str(len(weights))], level='weight_effective_values')
                if weight == 0:
                    sys_data.web_api.play_sound("fail_weight")
                    sys_data.data_dict["parcel_object_dict"][current_id]["status"] = 0
                    sys_data.data_dict["parcel_object_dict"][current_id]["info"] = "重量测量失败"
                else:
                    sys_data.web_api.play_sound("success_weight")
                # 推送到前端
                sys_data.web_api.parcel_update_data(current_id)
                data_parse.is_data_completed(sys_data.data_dict["parcel_object_dict"][current_id], '重量计算完成')
                fn.logger(f"重量值为：{weight}")
        except Exception as e:
            if sys_data.web_api.config["fail_stop"]:
                sys_data.web_api.stop()
                fn.logger(data="重量处理失败_stop", r_path=sys_data.r_path)
            sys_data.web_api.play_sound("fail_weight")
            fn.logger(f"重量处理失败：{e}", level='error')

    @staticmethod
    def adjust_values(weight):
        """
        矫正值
        :param weight:
        :return:
        """
        weight += sys_data.web_api.config['weight_adjust_value']
        weight = data_parse.adapt_value('weight', weight)
        return weight


if __name__ == "__main__":
    weighting = Weigh()
    weighting.run()
    time.sleep(10000)
