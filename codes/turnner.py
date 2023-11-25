
class TurnController():
    def __init__(self):
        self.direction = "straight"

    def turn_left(self):
        self.direction = "left"
        print("Turning left")

    def turn_right(self):
        self.direction = "right"
        print("Turning right")

    def get_direction(self):
        return self.direction

# Example usage:
controller = TurnController()
print(controller.get_direction())  # Output: "straight"

controller.turn_left()
print(controller.get_direction())  # Output: "left"

controller.turn_right()
print(controller.get_direction())  # Output: "right"
