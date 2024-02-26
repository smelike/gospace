from zdrv import Zdrv

# 1 是 滚筒 2 是大轮子 3 是小轮子
# 4 是滚筒 5 是大轮子 6 是小轮子
# Constants for motor
PLATEN_ROLLER_MOTOR = 0x01
FORWARD_MOTOR = 0x02
SWITCH_MOTOR = 0x03

# Constants for orientation
SWITCH_MOTOR_LEFT = 0x01
SWITCH_MOTOR_RIGHT= 0x02

class TurnController():
    def __init__(self):
        self.direction = "straight"
        self.blockNo = 1

    def turn_left(self, speed:int = 1630):
        self.direction = "left"
        print("Turning left")
        print(speed)
        print(format(0x01, '02x'))
        maddr = format(FORWARD_MOTOR, '02x')
        oriet = format(SWITCH_MOTOR_LEFT, '02x')
        cmd = f"{maddr} 06 20 00 {oriet}"
        print(cmd)


        rm = Zdrv("COM19", 19200)
        rm.turn_on(3, 1) # forward 黄色小轮子
        # rm.set_rpm(800, 3) # 会有报错，待测试
        rm.set_rpm(1200, 3) # 给黄色小轮子设置转速  
       
        rm.turn_on(2) # left or right 绿色大轮子
        rm.set_rpm(1000, 2) # 给大轮子设置转速

    def turn_right(self, speed:int = 1630):
        self.direction = "right"
        print("Turning right")
        rm = Zdrv("COM19", 19200)
        rm.turn_on(3, 1) # forward 黄色小轮子
        # rm.set_rpm(800, 3) # 会有报错，待测试
        rm.set_rpm(1200, 3) # 给黄色小轮子设置转速  
       
        rm.turn_on(2 , 2) # left or right 绿色大轮子
        rm.set_rpm(1000, 2) # 给大轮子设置转速

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
