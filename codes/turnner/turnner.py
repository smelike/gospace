from zdrv import Zdrv
import time

# 1 是 滚筒 2 是大轮子 3 是小轮子
# 4 是滚筒 5 是大轮子 6 是小轮子
# Constants for motor
PLATEN_ROLLER_MOTOR = 0x01
FORWARD_MOTOR = 0x02
SWITCH_MOTOR = 0x03

# Constants for orientation
SWITCH_MOTOR_LEFT = 0x01
SWITCH_MOTOR_RIGHT= 0x02

# Load configuration
# from common import fn
# config = fn.get_local_config()

class TurnController():
    def __init__(self, com = "com8", baudrate = 19200):
        self.direction = "straight"
        self.blockNo = 1
        self.com = com
        self.baudrate = baudrate
        self.rm = Zdrv(self.com, self.baudrate)

    def straight_forward(self):
        # 所有滚筒段，都是往前走的。
        self.turn_roller_motor(1630)
        # 保证所有分拣卡口的，黄色小轮子都是向前走的。
        self.turn_forward_motor(1630)

    # 打开滚筒
    def turn_roller_motor(self, speed: int = 1630):
        self.rm.turn_on(1, 1)
        self.rm.set_rpm(speed, 1) 

    # 打开黄色小轮子
    def turn_forward_motor(self, speed:int = 1630):
        # rm = Zdrv("COM19", 19200)
        self.rm.turn_on(3, 1) # forward 黄色小轮子
        self.rm.set_rpm(speed, 3) # 给黄色小轮子设置转速  
       

    # 打开绿色大轮子：左转
    def turn_left(self, speed:int = 1630):
        self.direction = "left"
        # rm = Zdrv(self.com, self.baudrate)
        print("Turning left")
        self.rm.turn_on(2) # left or right 绿色大轮子
        self.rm.set_rpm(speed, 2) # 给大轮子设置转速
        time.sleep(3)
        self.rm.set_rpm(0, 2)

    # 打开绿色大轮子：右转
    def turn_right(self, speed:int = 1630):
        self.direction = "right"
        print("Turning right")
        self.rm.turn_on(2 , 2) # left or right 绿色大轮子
        self.rm.set_rpm(speed, 2) # 给大轮子设置转速
        time.sleep(3)
        self.rm.set_rpm(0, 2)

    def get_direction(self):
        return self.direction

    # direction 整个分拣模块的动作
    # blockNo 分拣模块的区块号
    def run(self, direction: str, blockNo: int = 1):
        self.blockNo = blockNo
        print("run")
        if direction == "left":
            self.turn_left()
        elif direction == "right":
            self.turn_right()
        else:
            print("Invalid direction")

    def stop(self):
        rm = Zdrv("COM19", 19200)
        rm.turn_stop()


if __name__ == "__main__":
    # Example usage:
    controller = TurnController()
    print(controller.get_direction())  # Output: "straight"

    # controller.turn_left()
    # print(controller.get_direction())  # Output: "left"

    # controller.turn_right()
    # print(controller.get_direction())  # Output: "right"

    controller.run("left", 1)
    controller.run("right", 1)
