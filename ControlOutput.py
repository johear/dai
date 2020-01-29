import numpy as np

class ControlOutput():

    action_dim = 9

    def __init__(self):
        self.Wheel1aTargetSpeed = 0.0
        self.Wheel1bTargetSpeed = 0.0
        self.Wheel2aTargetSpeed = 0.0
        self.Wheel2bTargetSpeed = 0.0
        self.Wheel3aTargetSpeed = 0.0
        self.Wheel3bTargetSpeed = 0.0

        self.Slider1TargetSpeed = 0.0
        self.Slider2TargetSpeed = 0.0
        self.Slider3TargetSpeed = 0.0

    def set_actions_array(self, actions):
        self.Wheel1aTargetSpeed = actions[0][0] * 10
        self.Wheel1bTargetSpeed = actions[0][1] * 10
        self.Wheel2aTargetSpeed = actions[0][2] * 10
        self.Wheel2bTargetSpeed = actions[0][3] * 10
        self.Wheel3aTargetSpeed = actions[0][4] * 10
        self.Wheel3bTargetSpeed = actions[0][5] * 10

        self.Slider1TargetSpeed = actions[0][6] * 250
        self.Slider2TargetSpeed = actions[0][7] * 250
        self.Slider3TargetSpeed = actions[0][8] * 250

    def get_actions_array(self):
        actions = np.zeros([1, self.action_dim])
        actions[0][0] = self.Wheel1aTargetSpeed / 10
        actions[0][1] = self.Wheel1bTargetSpeed / 10
        actions[0][2] = self.Wheel2aTargetSpeed / 10
        actions[0][3] = self.Wheel2bTargetSpeed / 10
        actions[0][4] = self.Wheel3aTargetSpeed / 10
        actions[0][5] = self.Wheel3bTargetSpeed / 10
        actions[0][6] = self.Slider1TargetSpeed / 250
        actions[0][7] = self.Slider2TargetSpeed / 250
        actions[0][8] = self.Slider3TargetSpeed / 250
        return actions
