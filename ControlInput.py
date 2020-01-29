class ControlInput():

    state_dim = 15

    def __init__(self):
        self.Wheel1aTargetSpeed = 0.0
        self.Wheel1bTargetSpeed = 0.0
        self.Wheel2aTargetSpeed = 0.0
        self.Wheel2bTargetSpeed = 0.0
        self.Wheel3aTargetSpeed = 0.0
        self.Wheel3bTargetSpeed = 0.0

        self.Slider1Position = 0.0
        self.Slider2Position = 0.0
        self.Slider3Position = 0.0

        self.Slider1TargetSpeed = 0.0
        self.Slider2TargetSpeed = 0.0
        self.Slider3TargetSpeed = 0.0

        self.XPos = 0.0
        self.YPos = 0.0
        self.ZPos = 0.0
        self.YawAngle = 0.0
        self.PitchAngle = 0.0
        self.RollAngle = 0.0

        self.XSpeed = 0.0
        self.YSpeed = 0.0
        self.ZSpeed = 0.0
        self.YawSpeed = 0.0
        self.PitchSpeed = 0.0
        self.RollSpeed = 0.0

        self.XAccel = 0.0
        self.YAccel = 0.0
        self.ZAccel = 0.0
        self.YawAccel = 0.0
        self.PitchAccel = 0.0
        self.RollAccel = 0.0

        self.ObstacleDist_1a2a3a = 0.0
        self.ObstacleDist_1a2b3a = 0.0
        self.ObstacleDist_1a2b3b = 0.0
        self.ObstacleDist_1a2a3b = 0.0
        self.ObstacleDist_1b2a3a = 0.0
        self.ObstacleDist_1b2b3a = 0.0
        self.ObstacleDist_1b2b3b = 0.0
        self.ObstacleDist_1b2a3b = 0.0

        self.ObstacleDanger_1a2a3a = 0.0
        self.ObstacleDanger_1a2b3a = 0.0
        self.ObstacleDanger_1a2b3b = 0.0
        self.ObstacleDanger_1a2a3b = 0.0
        self.ObstacleDanger_1b2a3a = 0.0
        self.ObstacleDanger_1b2b3a = 0.0
        self.ObstacleDanger_1b2b3b = 0.0
        self.ObstacleDanger_1b2a3b = 0.0

        self.SpatialDangerXMin = 0.0
        self.SpatialDangerXMax = 0.0
        self.SpatialDangerYMin = 0.0
        self.SpatialDangerYMax = 0.0

    def get_states_array(self):
        return (self.XPos / 10, self.YPos / 10, self.ZPos / 10,
            self.Wheel1aTargetSpeed / 10, self.Wheel1bTargetSpeed / 10, self.Wheel2aTargetSpeed / 10,
            self.Wheel2bTargetSpeed / 10, self.Wheel3aTargetSpeed / 10, self.Wheel3bTargetSpeed / 10,
            self.Slider1Position / 10, self.Slider2Position / 10, self.Slider3Position / 10,
            self.Slider1TargetSpeed / 10, self.Slider2TargetSpeed / 10, self.Slider3TargetSpeed / 10)
