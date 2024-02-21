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

    def turn_left(self, speed:int = 1630):
        self.direction = "left"
        print("Turning left")
        print(speed)
        print(format(0x01, '02x'))
        maddr = format(FORWARD_MOTOR, '02x')
        oriet = format(SWITCH_MOTOR_LEFT, '02x')
        cmd = f"{maddr} 06 20 00 {oriet}"
        print(cmd)
    def turn_right(self):
        self.direction = "right"
        print("Turning right")

    def get_direction(self):
        return self.direction

    # direction 整个分拣模块的动作
    # blockNo 分拣模块的区块号
    def run(self, direction: str, blockNo: int = 1):
        if direction == "left":
            self.turn_left()
        elif direction == "right":
            self.turn_right()
        else:
            print("Invalid direction")

# Example usage:
controller = TurnController()
print(controller.get_direction())  # Output: "straight"

controller.turn_left()
print(controller.get_direction())  # Output: "left"

controller.turn_right()
print(controller.get_direction())  # Output: "right"
