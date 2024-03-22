from __future__ import absolute_import
# from common import fn
from zdrv import Zdrv

import time

# 1 是滚筒 2 是大轮子(绿色) 3 是小轮子(黄色)
# 4 是滚筒 5 是大轮子 6 是小轮子
# Constants for motor
WHITE_ROLLER_MOTOR_ADDR = 1
GREEN_SWITCH_MOTOR_ADDR = 2
YELLOW_FORWARD_MOTOR_ADDR = 3


# Constants for orientation (左转还是右转)
SWITCH_MOTOR_LEFT = 1
SWITCH_MOTOR_RIGHT = 2

# Constants for reverse (是否反转)
NO_REVERSE = 1
YES_REVERSE = 2

# Load configuration
# from common import fn
# config = fn.get_local_config()

class TurnController():
    _instance = None
    # 单例模式
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TurnController, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, com="com8", baudrate=19200):
        self.direction = "straight"
        self.blockNo = 1
        self.com = com
        self.baudrate = baudrate
        self.rm = Zdrv(self.com, self.baudrate)

    # 分拣设备的初始状态：滚筒段和黄色小轮子，都是转动的，保证获取直走。
    def straight_forward(self, speed: int = 1630):
        # 所有滚筒段，都是往前走的。
        self.turn_roller_motor(1630)
        # 保证所有分拣卡口的，黄色小轮子都是向前走的。
        self.turn_forward_motor(1000)

    # 打开滚筒
    def turn_roller_motor(self, speed: int = 1630):
        self.rm.turn_on(WHITE_ROLLER_MOTOR_ADDR, NO_REVERSE)
        self.rm.set_rpm(speed, WHITE_ROLLER_MOTOR_ADDR)

    # 打开黄色小轮子
    def turn_forward_motor(self, speed: int = 1630):
        self.rm.turn_on(YELLOW_FORWARD_MOTOR_ADDR, NO_REVERSE)  # forward 黄色小轮子
        self.rm.set_rpm(speed, YELLOW_FORWARD_MOTOR_ADDR)  # 给黄色小轮子设置转速

    # 打开绿色大轮子：左转，3秒后停止
    def turn_left(self, speed: int = 1630, duration = 3):
        self.direction = "left"
        fn.logger("tunner: Turning left")
        self.rm.turn_on(GREEN_SWITCH_MOTOR_ADDR, YES_REVERSE)  # left or right 绿色大轮子
        self.rm.set_rpm(speed, GREEN_SWITCH_MOTOR_ADDR)  # 给大轮子设置转速
        time.sleep(duration)
        self.rm.turn_stop(GREEN_SWITCH_MOTOR_ADDR)

    # 打开绿色大轮子：右转，3秒后停止
    def turn_right(self, speed: int = 1630, duration = 3):
        self.direction = "right"
        fn.logger("tunner：Turning right")
        self.rm.turn_on(GREEN_SWITCH_MOTOR_ADDR, NO_REVERSE)  # left or right 绿色大轮子
        self.rm.set_rpm(speed, GREEN_SWITCH_MOTOR_ADDR)  # 给大轮子设置转速
        time.sleep(duration)
        self.rm.turn_stop(GREEN_SWITCH_MOTOR_ADDR)

    def get_direction(self):
        return self.direction

    # direction 整个分拣模块的动作
    # blockNo 分拣模块的区块号
    def run(self, direction: str, blockNo: int = 1, speed: int = 2500):
        self.blockNo = blockNo
        fn.logger("tunner run")
        if direction == "left":
            self.turn_left(speed)
        elif direction == "right":
            self.turn_right(speed)
        else:
            fn.logger(f"tunner Invalid direction:{direction}",level="error")

    def stop(self):
        self.rm.turn_stop()

if __name__ == "__main__":
    # Example usage:
    controller = TurnController("com5", 19200)
    fn.logger(controller.get_direction())  # Output: "straight"

    # controller.turn_left()
    # fn.logger(controller.get_direction())  # Output: "left"

    # controller.turn_right()
    # fn.logger(controller.get_direction())  # Output: "right"

    controller.run("left", 1)
    controller.run("right", 1)
