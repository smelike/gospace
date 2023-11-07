import json
import traceback
import serial
import atexit
import time
from common import fn
from common import sys_data, data_parse
import crc16


class pipeline_motor:
    def __init__(self):
        self.relay_writing = False
        self.motor_writing = False
        self.motor_serial_list = dict()
        self.motor_serial_list_lock = dict()
        self.motor_serial_cfg = dict()
        if sys_data.web_api.config["simulation"] != 2:
            if sys_data.serial_dict["relay_serial"]:
                self.relay_serial = serial.Serial(
                    sys_data.serial_dict["relay_serial"]["serial_port"], 
                    9600,
                    timeout=sys_data.web_api.config.get("relay_serial_timeout", 0.02)
                    )
            else:
                fn.logger(f"没有寻找到继电器串口", level='error', r_path=sys_data.r_path)
            if sys_data.serial_dict.get("motor_serial", None):
                if sys_data.serial_dict.get("motor_serial", None):
                    self.motor_serial_list_lock[sys_data.serial_dict["motor_serial"]["serial_port"]] = 0
                    self.motor_serial_list[sys_data.serial_dict["motor_serial"]["serial_port"]] = serial.Serial(
                        sys_data.serial_dict["motor_serial"]["serial_port"],
                        sys_data.serial_dict["motor_serial"]["baud_rate"],
                        timeout=sys_data.web_api.config.get("relay_serial_timeout", 0.02))
                # 从配置文件读取中大电机配置
                self.motor_serial_cfg = sys_data.web_api.config.get("motor_cfg", {})
                if self.motor_serial_cfg:
                    for motor_area, motor_value in self.motor_serial_cfg.items():
                        # 检查串口是否存在：
                        if motor_value.get("com", None) is not None:
                            if motor_value.get("com") not in self.motor_serial_list:
                                try:
                                    exec(
                                        f"""
                                        self.motor_serial_list["{motor_value.get("com")}"] 
                                        = serial.Serial(
                                            "{motor_value.get("com")}", 
                                        {sys_data.web_api.config.get("motor_cfg", {}).get("given_baud_rate", 19200)}, 
                                        timeout=sys_data.web_api.config.get("relay_serial_timeout", 0.02))
                                        """)
                                    exec(f"""self.motor_serial_list_lock["{motor_value.get("com")}"]= 0""")
                                except Exception as e:
                                    fn.logger(f"电机{motor_area}连接指定串口失败：{e}", level='error',
                                              r_path=sys_data.r_path)
                        # 构建命令 地址1b,功能码1b,寄存器地址2b,数据2b，校验码2b
                        motor_addr = str(hex(int(motor_value['addr'])))[2:].zfill(2)
                        motor_speed = str(hex(int(motor_value['speed'])))[2:].zfill(4)
                        speed_cmd = f"{motor_addr} 06 20 01 {motor_speed[:2]} {motor_speed[2:]}"
                        speed_cmd_crc_16 = crc_16.get_crc16_modbus(speed_cmd)
                        speed_cmd = f"{speed_cmd} {speed_cmd_crc_16}"
                        # 设定速度
                        result = data_parse.hexShow(
                            self.motor_write(
                                speed_cmd, 
                                motor_value.get("com", sys_data.serial_dict["motor_serial"]["serial_port"])
                            )).replace(" ", "")
                            speed_cmd = speed_cmd.replace(" ", "")
                        if result == speed_cmd:
                            fn.logger(f"设定电机{motor_area}  转速：{motor_value['speed']} 成功", level='info',
                                      r_path=sys_data.r_path)
                        else:
                            fn.logger(
                                f"设定电机{motor_area}  转速：{motor_value['speed']} 失败 命令{speed_cmd} 结果{result}",
                                level='error', r_path=sys_data.r_path)
            else:
                fn.logger(f"没有寻找到电机串口", level='error', r_path=sys_data.r_path)
        # self.relay_serial = serial.Serial("COM9", 9600, timeout=0.05)
        self.exit_hook()
        self.weight_object = sys_data.Weigh
        self.t_motor = None
        # laser 控制
        self.do1 = 0  # 0代表开，1代表关
        self.do2 = 0  # 0代表开，1代表关
        self.di1 = 0  # 0代表无遮挡，1代表遮挡
        self.di2 = 0
        self.relay_first_list = []
        self.last_di1 = 0
        self.last_di2 = 0
        self.send_time = int(time.time())
        self.di2_in_time = None
        if sys_data.web_api.config["simulation"] == 2:
            self.d_value_time = time.time() - float(sys_data.simulation["motor"][0][1])

    def relay_laser_run(self):
        """
        激光光耦事件检测处理
        :return:
        """
        if sys_data.web_api.config["simulation"] in [1, 0]:
            response_bytes = self.relay_write("FE 01 00 00 00 04 29 C6")
            response = " ".join(map(lambda x: "%02x" % x, response_bytes))
            relay_status_list = list(
                bin(
                    int(response.split(" ")[-3], 16))[2:].zfill(4)
                )
            relay_status_list.reverse()
            self.do1 = 1 if relay_status_list[0] == "1" else 0
            self.do2 = 1 if relay_status_list[1] == "1" else 0
        last_count_time = 0
        serial_read_speed_interval = 5
        serial_read_speed_count = 0
        while True:
            try:
                if sys_data.web_api.config["simulation"] == 0:
                    response_bytes = self.relay_write("FE 02 00 00 00 04 6D C6")
                    response_str = " ".join(map(lambda x: "%02x" % x, response_bytes))
                elif sys_data.web_api.config["simulation"] == 1:
                    response_bytes = self.relay_write("FE 02 00 00 00 04 6D C6")
                    response_str = " ".join(map(lambda x: "%02x" % x, response_bytes))
                    if sys_data.simulation_temp:
                        sys_data.simulation["motor"].append([response_str, str(time.time())])
                    else:
                        sys_data.simulation_temp_data["motor"].append([response_str, str(time.time())])
                elif sys_data.web_api.config["simulation"] == 2:
                    if sys_data.simulation["motor"]:
                        if time.time() - float(sys_data.simulation["motor"][0][1]) >= self.d_value_time:
                            response_str = sys_data.simulation["motor"][0][0]
                            sys_data.simulation["motor"].pop(0)
                        else:
                            time.sleep(0.01)
                            continue
                    else:
                        fn.logger(f"继电器仿真结束", level='info', r_path=sys_data.r_path)
                        time.sleep(5000)
                        continue
                else:
                    continue
                response_array = response_str.split(" ")
                if len(response_array) == 6:
                    for i in range(0, len(response_array), 6):
                        status_str = bin(int(response_array[-3], 16))[2:].zfill(4)
                        status_str_reversed = ""
                        i = len(status_str) - 1
                        while i >= 0:
                            status_str_reversed += status_str[i]
                            i -= 1
                        current_di1, 
                        current_di2, 
                        current_di3, 
                        current_di4 = map(lambda x: int(x), status_str_reversed)
                        if sys_data.web_api.config.get("relay_debug",0):
                            fn.logger(f"current_di1:{current_di1},current_di2:{current_di2},status_str_reversed:{status_str_reversed},status_str:{status_str},response_array:{response_array}", level='info', r_path=r"D:\nextsls\motor_log.txt")
                        self.di1 = current_di1
                        self.di2 = current_di2

                        # 配置了 debug 的数据处理记录
                        if sys_data.web_api.config["debug"]:
                            if int(time.time()) - self.send_time > 0.2:
                                self.send_time = int(time.time())
                                sys_data.debug_data["laser1"] = current_di1
                                sys_data.debug_data["laser2"] = current_di2
                        # 激光事件
                        # 第一光耦
                            #第一光耦遮挡了
                        if self.last_di1 == 0 and current_di1 == 1:
                            self.t_motor.create_thread(func=self.event_di1_in)
                            # 离开了第一光耦，进入了第二光耦
                        if self.last_di1 == 1 and current_di1 == 0:
                            self.t_motor.create_thread(func=self.event_di1_out)
                        # 将光耦1 的状态给到了 last_di1    
                        self.last_di1 = current_di1

                        # 第二光耦事件处理
                        if self.last_di2 == 0 and current_di2 == 1:
                            self.t_motor.create_thread(func=self.event_di2_in)
                        if self.last_di2 == 1 and current_di2 == 0:
                            self.t_motor.create_thread(func=self.event_di2_out)
                        self.last_di2 = current_di2

                        # 激光数据记录（不是光耦返回列表吗？）
                        if not sys_data.laser1_recode_list:
                            sys_data.laser1_recode_list.append(
                                {"hide": current_di1, "time": time.time()}
                            )
                        else:
                            if time.time() - sys_data.laser1_recode_list[-1]["time"] >= 0.5:
                                sys_data.laser1_recode_list.append({"hide": current_di1, "time": time.time()})
                        if len(sys_data.laser1_recode_list) > 6:
                            sys_data.laser1_recode_list.pop(0)
                    if sys_data.debug and len(fn.debug_levels) > 0:
                        serial_read_speed_count += 1
                        int_time = int(time.time())
                        if int_time != last_count_time and int_time % serial_read_speed_interval == 0:
                            last_count_time = int_time
                            fn.dp('motor serial read speed count', serial_read_speed_count, level='motor_serial_speed')
                            serial_read_speed_count = 0
                else:
                    if sys_data.web_api.config.get("relay_debug",0):
                        fn.logger(
                            f"response_array:{response_array}",
                            level='error', 
                            r_path=r"D:\nextsls\motor_log.txt"
                        )
            except Exception as e:
                fn.logger(f"继电器错误：{e}", level='error', r_path=sys_data.r_path)
            time.sleep(0.01)

    def event_di1_in(self):
        """
        检查和创建货箱id和创建id对象
        :return:
        """
        # sys_data.web_api.window.evaluate_js('check_last_data()') #当排队时会出错，暂时不用
        fn.logger("\n\n\n\n\n\n")
        fn.logger(f"光耦1-进入", 
            level='info', event='di1_in', 
            r_path=sys_data.r_path)
        if sys_data.data_dict["measuring"]:
            fn.logger(
                f"测量中,暂停白滚筒运行", 
                level='info', event='di1_in', 
                r_path=sys_data.r_path, 
                print_to_c=True
                )
            # playsound(fn.format_path(sys_data.base_path + '/static/video/block.mp3'))
            self.white_motor_turn_off()


    @staticmethod
    def event_di1_out():
        fn.logger(f"光耦1-离开", level='info', event='di1_out')

    def event_di2_in(self):
        """
        触发称重
        :return:
        """
        self.di2_in_time = time.time()
        fn.logger(f"光耦2-进入", event='di2_in')
        log_msg = [['当前是否正在测量', sys_data.data_dict["measuring"]]
        fn.logger(log_msg, "高光幕是否遮挡",sys_data.data_dict["height_hide"]], event='di2_in')
        # 在测量中，并且高光是 非 height_hide 的
        if sys_data.data_dict["measuring"] and (not sys_data.data_dict["height_hide"]):
            time.sleep(0.1)
            fn.logger(f"开始计算重量", level='info', event='di2_out')
            self.t_motor.create_thread(func=self.weight_object.weigh_calculate)
            sys_data.data_dict["last_mongoid"] = sys_data.data_dict["current_id"]

    def event_di2_out(self):
        fn.logger(f"光耦2-离开", event='di2_out')
        # 判断货物是不是Noread
        if sys_data.data_dict["current_id"] is None:
            # 兼容超长货箱情况
            current_id = sys_data.data_dict["last_mongoid"]
        else:
            current_id = sys_data.data_dict["current_id"]
        if current_id is not None:
            if sys_data.data_dict["parcel_object_dict"][current_id]["barcode"] == "NoRead":
                fn.logger(f"光耦2-离开 条码为NoRead 停止", level='info', r_path=sys_data.r_path)
                sys_data.web_api.stop()
            if sys_data.data_dict["parcel_object_dict"][current_id]["status"] == 0:
                sys_data.web_api.play_sound("gauging_failure")
        # 出去时的重量小于最小称重
        leave_status = False
        out_time = time.time()
        if out_time - self.di2_in_time < sys_data.web_api.config.get("di2_judgment_time", 0.3):
            print(out_time - self.di2_in_time)
            if sys_data.data_dict["current_id"] is None:
                pass
            else:
                current_id = sys_data.data_dict["current_id"]
                sys_data.data_dict["parcel_object_dict"][current_id]["status"] = 0
                sys_data.data_dict["parcel_object_dict"][current_id]["info"] += "出货口有异物阻挡"
                # 推送到前端
                sys_data.web_api.parcel_update_data(current_id)
        print(f"高的阻挡值{sys_data.data_dict['height_hide']}")
        if not sys_data.data_dict["height_hide"]:
            fn.logger(
                ["sys_data.weight_recode_list:", sys_data.weight_recode_list], 
                event='di2_out')
            for weight_recode in sys_data.weight_recode_list:
                # fn.dp(f"""out_time - weight_recode["time"] < 3:{out_time - weight_recode["time"] < 3}  weight_recode["weight"]:{weight_recode["weight"]} """)
                # 通过最近两秒有无重量判断是否为货物离开
                fn.logger(
                    f'两秒有无重量判断:{out_time, out_time - weight_recode["time"] < 2, weight_recode["weight"]}', 
                    event='di2_out')
                # out_time - weight_recode["time"] < 2 
                # and 
                # weight_recode["weight"] > sys_data.web_api.config.get("min_weight", 0.5)
                if out_time - weight_recode["time"] < 2 and weight_recode["weight"] > sys_data.web_api.config.get("min_weight", 0.5):
                    fn.logger(
                        f"判断为物品离开光耦2,当前光耦1遮挡状态为：{self.di1},启动状态为：{sys_data.web_api.is_start}", 
                        event='di2_out')
                    leave_status = True
                    if self.di1 == 1 and sys_data.web_api.is_start:
                        self.white_motor_turn_on()
                    sys_data.data_dict["measuring"] = False
                    if sys_data.web_api.config["debug"]:
                        sys_data.debug_data["measuring"] = "无测量"
                    break
        # 判断是不是货物出去的语音提示
        if not leave_status:
            fn.logger(f"判断为非货物离开光耦2", event='di2_out', level='error')

    def relay_write(self, code_str, first=False):
        """
        继电器写入命令
        :param code_str: 写入命令
        :param first:优先级
        :return:
        """
        while True:
            if self.relay_writing:
                time.sleep(0.01)
                continue
            else:
                self.relay_writing = True
                if sys_data.web_api.config["simulation"] != 2:
                    # 检查优先级 优先写入优先级
                    while self.relay_first_list:
                        code_str = self.relay_first_list.pop(0)
                        print(code_str)
                        self.relay_serial.write(bytes.fromhex(code_str))
                        result = self.relay_serial.readall()
                        while not result:
                            result = self.relay_serial.readall()
                            time.sleep(0.01)
                        time.sleep(0.01)
                    self.relay_serial.write(bytes.fromhex(code_str))
                    result = self.relay_serial.readall()
                    while not result:
                        result = self.relay_serial.readall()
                        time.sleep(0.01)
                    self.relay_writing = False
                    return result

    def motor_write(self, code_str, mod=None):
        """
        中大电机写入命令
        :param code_str: 写入命令
        :param mod:模块串口
        :return:
        """
        while True:
            if mod is None:
                mod = sys_data.serial_dict["motor_serial"]["serial_port"]
            else:
                pass
            if self.motor_serial_list_lock[mod]:
                time.sleep(0.01)
                continue
            else:
                self.motor_serial_list_lock[mod] = True
                if sys_data.web_api.config["simulation"] != 2:
                    self.motor_serial_list[mod].write(bytes.fromhex(code_str))
                    result = False
                    while not result:
                        result = self.motor_serial_list[mod].readall()
                        time.sleep(0.01)
                    self.motor_serial_list_lock[mod] = False
                    return result

    def exit_hook(self):
        """
        注册函数 解释器退出时 自动执行
        :return:
        """
        atexit.register(self.white_motor_turn_off)
        atexit.register(self.black_motor_turn_off)
        atexit.register(self.barcode_light_turn_off)

    def motor_turn_on(self):
        """
        流水线总开
        :return:
        """
        file_name, _, def_name, _ = traceback.extract_stack()[-2]
        fn.logger(f"---文件路径：{file_name}，方法名：{def_name} ，流水线总开---", level='info', r_path=sys_data.r_path)
        self.white_motor_turn_on()
        self.black_motor_turn_on()
        self.barcode_light_turn_on()

    def motor_turn_off(self):
        """
        流水线总关
        :return:
        """
        file_name, _, def_name, _ = traceback.extract_stack()[-2]
        fn.logger(f"---文件路径：{file_name}，方法名：{def_name} ，流水线总关---", level='info', r_path=sys_data.r_path)
        self.white_motor_turn_off()
        self.black_motor_turn_off()
        self.barcode_light_turn_off()

    def white_motor_turn_on(self):
        """
        白滚筒开
        :return:
        """
        file_name, _, def_name, _ = traceback.extract_stack()[-2]
        fn.logger(f"---文件路径：{file_name}，方法名：{def_name} ，白滚筒开---", level='info', r_path=sys_data.r_path)
        if "mod2" not in self.motor_serial_cfg:
            self.relay_first_list.append('FE050001FF00C9F5')
        else:
            motor_value = self.motor_serial_cfg["mod2"]
            # 构建命令 地址1b,功能码1b,寄存器地址2b,数据2b，校验码2b
            motor_addr = str(hex(int(motor_value["addr"])))[2:].zfill(2)
            if motor_value['corotation']:
                corotation_cmd = f"{motor_addr} 06 20 00 00 01"
            else:
                corotation_cmd = f"{motor_addr} 06 20 00 00 02"
            # 校验
            corotation_crc_16 = crc_16.get_crc16_modbus(corotation_cmd)
            corotation_cmd = f"{corotation_cmd} {corotation_crc_16}"
            res = self.motor_write(corotation_cmd,motor_value.get("com", sys_data.serial_dict["motor_serial"]["serial_port"]))
            result = data_parse.hexShow(res).replace(" ", "")
            corotation_cmd = corotation_cmd.replace(" ", "")
            if result == corotation_cmd:
                fn.logger(f"进货白滚筒电机  转向：{motor_value['corotation']} 成功", level='info',
                          r_path=sys_data.r_path)
            else:
                fn.logger(f"进货白滚筒电机  转向：{motor_value['corotation']} 失败 命令{corotation_cmd} 结果{result}",
                          level='error', r_path=sys_data.r_path)
        sys_data.white_motor = {"status": True, "time": int(time.time())}
        if sys_data.web_api.config["debug"]:
            sys_data.debug_data["white_motor"] = "开启"

    def white_motor_turn_off(self):
        """
        白滚筒关
        :return:
        """
        file_name, _, def_name, _ = traceback.extract_stack()[-2]
        fn.logger(f"---文件路径：{file_name}，方法名：{def_name} ，白滚筒关---", level='info', r_path=sys_data.r_path)
        if "mod2" not in self.motor_serial_cfg:
            self.relay_first_list.append('FE05000100008805')
        else:
            motor_value = self.motor_serial_cfg["mod2"]
            # 构建命令 地址1b,功能码1b,寄存器地址2b,数据2b，校验码2b
            motor_addr = str(hex(int(motor_value["addr"])))[2:].zfill(2)
            corotation_cmd = f"{motor_addr} 06 20 00 00 05"
            # 校验
            corotation_crc_16 = crc_16.get_crc16_modbus(corotation_cmd)
            corotation_cmd = f"{corotation_cmd} {corotation_crc_16}"
            res = self.motor_write(corotation_cmd,motor_value.get("com", sys_data.serial_dict["motor_serial"]["serial_port"]))
            result = data_parse.hexShow(res).replace(" ", "")
            corotation_cmd = corotation_cmd.replace(" ", "")
            if result == corotation_cmd:
                fn.logger(f"进货白滚筒电机关闭  成功", level='info', r_path=sys_data.r_path)
            else:
                fn.logger(f"进货白滚筒电机关闭  失败 命令{corotation_cmd} 结果{result}", level='error',
                          r_path=sys_data.r_path)
        sys_data.white_motor = {"status": False, "time": int(time.time())}
        if sys_data.web_api.config["debug"]:
            sys_data.debug_data["white_motor"] = "关闭"

    def black_motor_turn_on(self):
        """
        黑皮带开
        :return:
        """
        file_name, _, def_name, _ = traceback.extract_stack()[-2]
        fn.logger(f"---文件路径：{file_name}，方法名：{def_name} ，黑皮带开---", level='info', r_path=sys_data.r_path)
        if "mod3" not in self.motor_serial_cfg:
            self.relay_first_list.append('FE050000FF009835')
        else:
            motor_value = self.motor_serial_cfg["mod3"]
            # 构建命令 地址1b,功能码1b,寄存器地址2b,数据2b，校验码2b
            motor_addr = str(hex(int(motor_value["addr"])))[2:].zfill(2)
            if motor_value['corotation']:
                corotation_cmd = f"{motor_addr} 06 20 00 00 01"
            else:
                corotation_cmd = f"{motor_addr} 06 20 00 00 02"
            # 校验
            corotation_crc_16 = crc_16.get_crc16_modbus(corotation_cmd)
            corotation_cmd = f"{corotation_cmd} {corotation_crc_16}"
            res = self.motor_write(corotation_cmd,
                                   motor_value.get("com", sys_data.serial_dict["motor_serial"]["serial_port"]))
            result = data_parse.hexShow(res).replace(" ", "")
            corotation_cmd = corotation_cmd.replace(" ", "")
            if result == corotation_cmd:
                fn.logger(f"测量黑皮带电机  转向：{motor_value['corotation']} 成功", level='info',
                          r_path=sys_data.r_path)
            else:
                fn.logger(f"测量黑皮带电机  转向：{motor_value['corotation']} 失败 命令：{corotation_cmd} 结果{result}",
                          level='error', r_path=sys_data.r_path)
        sys_data.black_motor = {"status": True, "time": int(time.time())}
        if sys_data.web_api.config["debug"]:
            sys_data.debug_data["black_motor"] = "开启"

    def black_motor_turn_off(self):
        """
        黑皮带关
        :return:
        """
        file_name, _, def_name, _ = traceback.extract_stack()[-2]
        fn.logger(f"---文件路径：{file_name}，方法名：{def_name} ，黑皮带关---", level='info', r_path=sys_data.r_path)
        if "mod3" not in self.motor_serial_cfg:
            self.relay_first_list.append('FE0500000000D9C5')
        else:
            motor_value = self.motor_serial_cfg["mod3"]
            # 构建命令 地址1b,功能码1b,寄存器地址2b,数据2b，校验码2b
            motor_addr = str(hex(int(motor_value["addr"])))[2:].zfill(2)
            corotation_cmd = f"{motor_addr} 06 20 00 00 05"
            # 校验
            corotation_crc_16 = crc_16.get_crc16_modbus(corotation_cmd)
            corotation_cmd = f"{corotation_cmd} {corotation_crc_16}"
            res = self.motor_write(corotation_cmd,
                                   motor_value.get("com", sys_data.serial_dict["motor_serial"]["serial_port"]))
            result = data_parse.hexShow(res).replace(" ", "")
            corotation_cmd = corotation_cmd.replace(" ", "")
            if result == corotation_cmd:
                fn.logger(f"测量黑皮带电机关闭 成功", level='info', r_path=sys_data.r_path)
            else:
                fn.logger(f"测量黑皮带电机关闭 失败 命令{corotation_cmd} 结果{result}", level='error',
                          r_path=sys_data.r_path)
        sys_data.black_motor = {"status": False, "time": int(time.time())}
        if sys_data.web_api.config["debug"]:
            sys_data.debug_data["black_motor"] = "关闭"

    def take_photo(self):
        """
        执行拍照
        :return:
        """
        file_name, _, def_name, _ = traceback.extract_stack()[-2]
        fn.logger(f"---文件路径：{file_name}，方法名：{def_name} ，执行拍照---", level='info', r_path=sys_data.r_path)
        fn.logger(f"触发扫码", level='info', r_path=sys_data.r_path)
        self.relay_first_list.append('FE05000200007805')
        self.relay_first_list.append('FE050002FF0039F5')
        fn.logger(f"触发扫码完成", level='info', r_path=sys_data.r_path)

    def barcode_scan_start(self):
        sys_data.barcode_scan_status['top'] = time.time()
        self.relay_first_list.append('FE050002FF0039F5')
        fn.logger(f"扫码进行中", event='barcode_scan_start')

    def barcode_scan_end(self):
        sys_data.barcode_scan_status['top'] = 0
        self.relay_first_list.append('FE05000200007805')
        fn.logger(f"扫码已结束", event='barcode_scan_end')

    def barcode_light_turn_on(self):
        """
        条形码灯开
        :return:
        """
        file_name, _, def_name, _ = traceback.extract_stack()[-2]
        fn.logger(f"---文件路径：{file_name}，方法名：{def_name} ，条形码灯开---", level='info', r_path=sys_data.r_path)
        if sys_data.web_api.config["simulation"] != 2:
            self.relay_first_list.append('FE050003FF006835')

    def barcode_light_turn_off(self):
        """
        条形码灯关
        :param api:
        :return:
        """
        file_name, _, def_name, _ = traceback.extract_stack()[-2]
        fn.logger(f"---文件路径：{file_name}，方法名：{def_name} ，条形码灯关---", level='info', r_path=sys_data.r_path)
        if sys_data.web_api.config["simulation"] != 2:
            self.relay_first_list.append('FE050003000029C5')


if __name__ == '__main__':
    motor = pipeline_motor()
    # motor.motor_turn_on()
    # motor.take_photo()
    # while True:
    #     motor.take_photo()
    #     time.sleep(0.5)
    # time.sleep(5)
    motor.motor_turn_off()
    # motor.relay_laser_run()
    # time.sleep(2)
