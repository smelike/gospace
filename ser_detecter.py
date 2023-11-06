import json
import time
from pathlib import Path
import serial
import serial.tools.list_ports
import atexit
from common import sys_data, fn, data_parse


def load_serial():
    """
    检测串口地址
    :return:
    """
    serials_dict = {"lightCurtainHeightPrefix": "", "height_serial": {}, "length_width_serial": {}, "weight_serial": {}, "relay_serial": {}}
    exclusive_coms = sys_data.web_api.config["exclusive_coms"]
    msg = "010300500002c41a"
    is_kpr = False
    if sys_data.web_api.config["weight_module"] == 'kpr':
        is_kpr = True
        msg = "010300500002c41a"
    elif sys_data.web_api.config["weight_module"] == 'xy':
        msg = "010300000002c40b"
    port_list = list(serial.tools.list_ports.comports())
    # SerialOp = serial.Serial('COM10', 19200, timeout=0.05)
    # SerialOp.write(bytes.fromhex("010300500002c41a"))
    # response = SerialOp.readall()
    # result = ' '.join(map(lambda x: '%02x' % x, response))
    # SerialOp.write(bytes.fromhex("010300500002c41a"))
    # response = SerialOp.readall()
    # result = ' '.join(map(lambda x: '%02x' % x, response))
    # SerialOp.close()
    rcode_port = None
    for k, v in enumerate(port_list):
        try:
            portTmp = list(port_list[k])
            rcode_port = portTmp[0]
            if portTmp[0] in exclusive_coms:
                continue
            # 长宽
            SerialOp = serial.Serial(portTmp[0], 115200, timeout=0.05)
            result = data_parse.hexShow(SerialOp.read(1000))
            if len(result) > 100:
                serials_dict['length_width_serial'] = {"serial_port": portTmp[0], "baud_rate": 115200}
                SerialOp.close()
                continue
            else:
                SerialOp.close()
            # 继电器
            SerialOp = serial.Serial(portTmp[0], 9600, timeout=0.05)
            SerialOp.write(bytes.fromhex('FE0100000002A9C4'))
            result = data_parse.hexShow(SerialOp.readall())
            if len(result) == 18:
                serials_dict['relay_serial'] = {"serial_port": portTmp[0], "baud_rate": 9600}
                SerialOp.close()
                continue
            SerialOp.close()
            # 中大电机
            SerialOp = serial.Serial(portTmp[0],  19200, timeout=0.05)
            SerialOp.write(bytes.fromhex('0106200000054209'))
            result = data_parse.hexShow(SerialOp.readall()).replace(" ","")
            if result == "0106200000054209":
                print("电机串口:",portTmp[0])
                serials_dict['motor_serial'] = {"serial_port": portTmp[0], "baud_rate": 19200}
                SerialOp.close()
                continue
            SerialOp.close()
            # 称重
            # 19200
            SerialOp = serial.Serial(portTmp[0], 19200, timeout=0.1)
            result = ""
            for i in range(5):
                SerialOp.write(bytes.fromhex("010300500002c41a"))
                response = SerialOp.readall()
                result = ' '.join(map(lambda x: '%02x' % x, response))
            if len(result) > 0:
                serials_dict['weight_serial'] = {"serial_port": portTmp[0], "baud_rate": 19200}
                SerialOp.close()
                continue
            SerialOp.close()
            # 9600
            SerialOp = serial.Serial(portTmp[0], 9600, timeout=0.1)
            result = ""
            for i in range(5):
                SerialOp.write(bytes.fromhex("010300500002c41a"))
                response = SerialOp.readall()
                result = ' '.join(map(lambda x: '%02x' % x, response))
            if len(result) > 0:
                serials_dict['weight_serial'] = {"serial_port": portTmp[0], "baud_rate": 9600}
                SerialOp.close()
                continue
            SerialOp.close()
            # 长宽 -- 高
            SerialOp = serial.Serial(portTmp[0], 115200, timeout=0.05)
            result = data_parse.hexShow(SerialOp.read(1000))
            if len(result) > 100:
                serials_dict['length_width_serial'] = portTmp[0]
                SerialOp.close()
                continue
            SerialOp.write(data_parse.hex_decode('01030000000F05CE'))
            result = data_parse.hexShow(SerialOp.readall())
            if result.strip() == '':
                SerialOp.write(data_parse.hex_decode('02030000000F05FD'))
                result = data_parse.hexShow(SerialOp.readall())
                if result.strip() == '':
                    SerialOp.write(data_parse.hex_decode('03030000000F042C'))
                    result = data_parse.hexShow(SerialOp.readall())
            resultArr = result.split(" ")
            if resultArr[0] == "01":
                serials_dict['lightCurtainHeightPrefix'] = "01"
                serials_dict['height_serial'] = {"serial_port": portTmp[0], "baud_rate": 115200}
            elif resultArr[0] == "02":
                serials_dict['lightCurtainHeightPrefix'] = "02"
                serials_dict['height_serial'] = {"serial_port": portTmp[0], "baud_rate": 115200}
            elif resultArr[0] == "03":
                serials_dict['lightCurtainHeightPrefix'] = "03"
                serials_dict['height_serial'] = {"serial_port": portTmp[0], "baud_rate": 115200}
            SerialOp.close()
        except Exception as e:
            fn.logger(f"串口{rcode_port}发生错误： 错误原因：{str(e)}")
    if sys_data.web_api.config.get("given_weight_serial",""):
        serials_dict['weight_serial'] = {"serial_port": "", "baud_rate": 19200}
        serials_dict["weight_serial"]["serial_port"] = sys_data.web_api.config["given_weight_serial"]
        serials_dict["weight_serial"]["baud_rate"] = sys_data.web_api.config["given_weight_baud_rate"]
    if sys_data.web_api.config.get("given_height_serial",""):
        serials_dict["height_serial"]["serial_port"] = sys_data.web_api.config["given_height_serial"]

    serial_str = "重量:" + json.dumps(serials_dict['weight_serial'])
    serial_str += "\n长宽:" + json.dumps(serials_dict['length_width_serial'])
    serial_str += "\n高度:" + json.dumps(serials_dict['height_serial'])
    serial_str += "\n继电器:" + json.dumps(serials_dict['relay_serial'])
    if serials_dict.get("motor_serial",None):
        serial_str += "\n电机:" + json.dumps(serials_dict['motor_serial'])
    fn.dp(serial_str)

    Path(fn.format_path(sys_data.base_path+"/log/")).mkdir(parents=True, exist_ok=True)
    with open(fn.format_path(sys_data.base_path+"/log/serials_log.txt"),"w+") as f:
        f.write(serial_str)
    return serials_dict


if __name__ == '__main__':
    serials = load_serial()
    fn.dp(serials)
