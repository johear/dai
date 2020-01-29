from Performance import Performance
from ControlInput import ControlInput
from ControlOutput import ControlOutput
from copy import copy
import math
import random
from enum import Enum

class WheelLayout(Enum):
    w_unknown = 0
    w_1a_2a_3a = 1
    w_1b_2a_3a = 2
    w_1a_2b_3a = 3
    w_1b_2b_3a = 4
    w_1a_2a_3b = 5
    w_1b_2a_3b = 6
    w_1a_2b_3b = 7
    w_1b_2b_3b = 8


class SafetyControlModule:

    _safety_margin = 1.5
    _previous_input = None
    _previous_output = None
    _positional_punishment = 0

    def __init__(self, performance: Performance):
       self.xMax = performance.xLength / 2
       self.xMin = -1 * self.xMax
       self.yMax = performance.yLength / 2
       self.yMin = -1 * self.yMax


    def check_xMax_bounds(self, currentXPos: float) -> float:
        if currentXPos >= 0 :
            if self.xMax - self._safety_margin > currentXPos :
                return 0 # no danger
            elif self.xMax <= currentXPos :
                return 1 # maximum danger
            else :
                return (currentXPos - (self.xMax - self._safety_margin)) / self._safety_margin # grows from 0 to 1
        else :
            return 0 # no danger


    def check_xMin_bounds(self, currentXPos: float) -> float:
        if currentXPos < 0:
            if self.xMin + self._safety_margin < currentXPos :
                return 0 # no danger
            elif self.xMin >= currentXPos :
                return 1 # maximum danger
            else :
                return ((self.xMin + self._safety_margin) - currentXPos) / self._safety_margin # grows from 0 to 1
        else :
            return 0 # no danger


    def check_yMax_bounds(self, currentYPos: float) -> float:
        if currentYPos >= 0:
            if self.yMax - self._safety_margin > currentYPos :
                return 0 # no danger
            elif self.yMax <= currentYPos :
                return 1 # maximum danger
            else :
                return (currentYPos - (self.yMax - self._safety_margin)) / self._safety_margin # grows from 0 to 1
        else :
            return 0 # no danger

  
    def check_yMin_bounds(self, currentYPos: float) -> float:
        if currentYPos < 0:
            if self.yMin + self._safety_margin < currentYPos :
                return 0 # no danger
            elif self.yMin >= currentYPos :
                return 1 # maximum danger
            else :
                return ((self.yMin + self._safety_margin) - currentYPos) / self._safety_margin # grows from 0 to 1                
        else :
            return 0 # no danger

    def get_positional_safety_punishment(self):
        return self._positional_punishment


    def sanitize_output(self, controlInput: ControlInput, controlOutput: ControlOutput) -> ControlOutput:
        safeOutput = copy(controlOutput)
        
        self._positional_punishment = 0

        x_min_bounds = self.check_xMin_bounds(controlInput.XPos)
        x_max_bounds = self.check_xMax_bounds(controlInput.XPos)
        y_min_bounds = self.check_yMin_bounds(controlInput.YPos)
        y_max_bounds = self.check_yMax_bounds(controlInput.YPos)

        print("IMT Pos:", controlInput.XPos, controlInput.YPos, flush = True)
        if ((x_min_bounds >= 1.0 or x_max_bounds >= 1.0 )
             or (y_min_bounds >= 1.0 or y_max_bounds >= 1.0)
             or (controlInput.XPos == 0.0 and controlInput.YPos == 0.0 and controlInput.ZPos == 0.0)):
                    print("SAFETY ACTIVATED", flush = True)
                    safeOutput.Wheel1aTargetSpeed = 0.0
                    safeOutput.Wheel1bTargetSpeed = 0.0
                    safeOutput.Wheel2aTargetSpeed = 0.0
                    safeOutput.Wheel2bTargetSpeed = 0.0
                    safeOutput.Wheel3aTargetSpeed = 0.0
                    safeOutput.Wheel3bTargetSpeed = 0.0

                    #safeOutput.Slider1TargetSpeed = 0.0
                    #safeOutput.Slider2TargetSpeed = 0.0
                    #safeOutput.Slider3TargetSpeed = 0.0
                    self._positional_punishment = -200

        elif ((x_min_bounds > 0 or x_max_bounds > 0 )
              or (y_min_bounds > 0 or y_max_bounds > 0)):

                    print("PREEMPTIVE SAFETY ACTIVATED", flush = True)

                    self._positional_punishment = (-100 * 
                        ( x_min_bounds + x_max_bounds 
                        + y_min_bounds + y_max_bounds))

                    cur_in = controlInput


                    if cur_in is not None:

                        wheelLayout = WheelLayout.w_unknown

                        if cur_in.RollAngle < 0.0 and cur_in.PitchAngle < -90.0:
                            print("Wheel configuration 1a-2a-3a")
                            wheelLayout = WheelLayout.w_1a_2a_3a
                        elif cur_in.RollAngle < 0.0 and cur_in.PitchAngle > 90.0:
                            print("Wheel configuration 1b-2a-3a")
                            wheelLayout = WheelLayout.w_1b_2a_3a
                        elif cur_in.RollAngle > 0.0 and cur_in.PitchAngle < -90.0:
                            print("Wheel configuration 1a-2b-3a")
                            wheelLayout = WheelLayout.w_1a_2b_3a
                        elif cur_in.RollAngle > 0.0 and cur_in.PitchAngle > 90.0:
                            print("Wheel configuration 1b-2b-3a")
                            wheelLayout = WheelLayout.w_1b_2b_3a
                        elif cur_in.RollAngle < 0.0 and cur_in.PitchAngle < 0.0:
                            print("Wheel configuration 1a-2a-3b")
                            wheelLayout = WheelLayout.w_1a_2a_3b
                        elif cur_in.RollAngle < 0.0 and cur_in.PitchAngle > 0.0:
                            print("Wheel configuration 1b-2a-3b")
                            wheelLayout = WheelLayout.w_1b_2a_3b
                        elif cur_in.RollAngle > 0.0 and cur_in.PitchAngle < 0.0:
                            print("Wheel configuration 1a-2b-3b")
                            wheelLayout = WheelLayout.w_1a_2b_3b
                        elif cur_in.RollAngle > 0.0 and cur_in.PitchAngle > 0.0:
                            print("Wheel configuration 1b-2b-3b")
                            wheelLayout = WheelLayout.w_1b_2b_3b


                        yaw = math.radians(cur_in.YawAngle)
                        angle1 = 0
                        angle2 = 0
                        angle3 = 0

                        if wheelLayout == WheelLayout.w_1a_2a_3a:
                            angle1 = yaw
                            angle2 = angle1 + math.radians(120)
                            angle3 = angle1 + math.radians(-120)
                        elif wheelLayout == WheelLayout.w_1b_2a_3a:
                            angle1 = yaw
                            angle2 = angle1 + math.radians(-120)
                            angle3 = angle1 + math.radians(120)
                        elif wheelLayout == WheelLayout.w_1a_2b_3a:
                            angle1 = yaw - math.radians(230)
                            angle2 = angle1 + math.radians(-120)
                            angle3 = angle1 + math.radians(120)
                        elif wheelLayout == WheelLayout.w_1b_2b_3a:
                            angle1 = yaw - math.radians(225)
                            angle2 = angle1 + math.radians(120)
                            angle3 = angle1 + math.radians(-120)
                        elif wheelLayout == WheelLayout.w_1a_2a_3b:
                            angle1 = yaw - math.radians(105)
                            angle2 = angle1 + math.radians(-120)
                            angle3 = angle1 + math.radians(120)
                        elif wheelLayout == WheelLayout.w_1b_2a_3b:
                            angle1 = yaw - math.radians(325)
                            angle2 = angle1 + math.radians(120)
                            angle3 = angle1 + math.radians(-120)
                        elif wheelLayout == WheelLayout.w_1a_2b_3b:
                            angle1 = yaw - math.radians(130)
                            angle2 = angle1 + math.radians(120)
                            angle3 = angle1 + math.radians(-120)
                        elif wheelLayout == WheelLayout.w_1b_2b_3b:
                            angle1 = yaw - math.radians(290)
                            angle2 = angle1 + math.radians(-120)
                            angle3 = angle1 + math.radians(120)



                        # total_x_bounds = x_min_bounds + x_max_bounds
                        # total_y_bounds = y_min_bounds + y_max_bounds

                        refSpeed = 10
                        # if total_x_bounds > total_y_bounds:
                        #     refSpeed += (total_x_bounds - 1) * 5
                        # else:
                        #     refSpeed += (total_y_bounds - 1) * 5

                        #print("RefSpeed: ", refSpeed, total_x_bounds, total_y_bounds, flush = True)
                        print("RefSpeed: ", refSpeed, flush = True)

                        wheel1Speed = 0
                        wheel2Speed = 0
                        wheel3Speed = 0

                        if x_min_bounds > 0:
                            wheel1Speed = -1 * math.sin(angle1) * refSpeed
                            wheel2Speed = -1 * math.sin(angle2) * refSpeed
                            wheel3Speed = -1 * math.sin(angle3) * refSpeed
                        elif x_max_bounds > 0:   
                            wheel1Speed = math.sin(angle1) * refSpeed
                            wheel2Speed = math.sin(angle2) * refSpeed
                            wheel3Speed = math.sin(angle3) * refSpeed

                        if y_min_bounds > 0:
                            wheel1Speed += math.cos(angle1) * refSpeed
                            wheel2Speed += math.cos(angle2) * refSpeed
                            wheel3Speed += math.cos(angle3) * refSpeed
                        elif y_max_bounds > 0:   
                            wheel1Speed += -1 * math.cos(angle1) * refSpeed
                            wheel2Speed += -1 * math.cos(angle2) * refSpeed
                            wheel3Speed += -1 * math.cos(angle3) * refSpeed



                        safeOutput.Wheel1aTargetSpeed = 0
                        safeOutput.Wheel1bTargetSpeed = 0
                        safeOutput.Wheel2aTargetSpeed = 0
                        safeOutput.Wheel2bTargetSpeed = 0
                        safeOutput.Wheel3aTargetSpeed = 0
                        safeOutput.Wheel3bTargetSpeed = 0

                        if wheelLayout == WheelLayout.w_1a_2a_3a:
                            safeOutput.Wheel1aTargetSpeed = wheel1Speed
                            safeOutput.Wheel2aTargetSpeed = wheel2Speed
                            safeOutput.Wheel3aTargetSpeed = wheel3Speed
                        elif wheelLayout == WheelLayout.w_1b_2a_3a:
                            safeOutput.Wheel1bTargetSpeed = wheel1Speed
                            safeOutput.Wheel2aTargetSpeed = wheel2Speed
                            safeOutput.Wheel3aTargetSpeed = wheel3Speed
                        elif wheelLayout == WheelLayout.w_1a_2b_3a:
                            safeOutput.Wheel1aTargetSpeed = wheel1Speed
                            safeOutput.Wheel2bTargetSpeed = wheel2Speed
                            safeOutput.Wheel3aTargetSpeed = wheel3Speed
                        elif wheelLayout == WheelLayout.w_1b_2b_3a:
                            safeOutput.Wheel1bTargetSpeed = wheel1Speed
                            safeOutput.Wheel2bTargetSpeed = wheel2Speed
                            safeOutput.Wheel3aTargetSpeed = wheel3Speed
                        elif wheelLayout == WheelLayout.w_1a_2a_3b:
                            safeOutput.Wheel1aTargetSpeed = wheel1Speed
                            safeOutput.Wheel2aTargetSpeed = wheel2Speed
                            safeOutput.Wheel3bTargetSpeed = wheel3Speed
                        elif wheelLayout == WheelLayout.w_1b_2a_3b:
                            safeOutput.Wheel1bTargetSpeed = wheel1Speed
                            safeOutput.Wheel2aTargetSpeed = wheel2Speed
                            safeOutput.Wheel3bTargetSpeed = wheel3Speed
                        elif wheelLayout == WheelLayout.w_1a_2b_3b:
                            safeOutput.Wheel1aTargetSpeed = wheel1Speed
                            safeOutput.Wheel2bTargetSpeed = wheel2Speed
                            safeOutput.Wheel3bTargetSpeed = wheel3Speed
                        elif wheelLayout == WheelLayout.w_1b_2b_3b:
                            safeOutput.Wheel1bTargetSpeed = wheel1Speed
                            safeOutput.Wheel2bTargetSpeed = wheel2Speed
                            safeOutput.Wheel3bTargetSpeed = wheel3Speed
 

        safeStart = 1500 #must be more than slider length
        safeEnd = 1000 #deactivated when safeEnd < safeStart
        if ((controlInput.ObstacleDist_1a2a3a > safeStart and  controlInput.ObstacleDist_1a2a3a < safeEnd)
            or (controlInput.ObstacleDist_1a2a3b > safeStart  and  controlInput.ObstacleDist_1a2a3b < safeEnd)
            or (controlInput.ObstacleDist_1a2b3a > safeStart and  controlInput.ObstacleDist_1a2b3a < safeEnd)
            or (controlInput.ObstacleDist_1a2b3b > safeStart and  controlInput.ObstacleDist_1a2b3b < safeEnd)
            or (controlInput.ObstacleDist_1b2a3a > safeStart and  controlInput.ObstacleDist_1b2a3a < safeEnd)
            or (controlInput.ObstacleDist_1b2a3b > safeStart and  controlInput.ObstacleDist_1b2a3b < safeEnd)
            or (controlInput.ObstacleDist_1b2b3a > safeStart and  controlInput.ObstacleDist_1b2b3a < safeEnd)
            or (controlInput.ObstacleDist_1b2b3b > safeStart and  controlInput.ObstacleDist_1b2b3b < safeEnd)
              ):
                    print("OBSTACLE SAFETY ACTIVATED", flush = True)
                    # prev_in = self._previous_input
                    # prev_out = self._previous_output
                    # cur_in = controlInput
                    # if prev_in is not None and prev_out is not None and cur_in is not None:
                        # if ((cur_in.XPos**2 + cur_in.YPos**2) > 
                            # (prev_in.XPos**2 + prev_in.YPos**2)):
                            # # Moving further from center, need to correct so we invert the wheel
                            # # speeds that got us here
                            # sonar_corr = -1.0
                            # safeOutput.Wheel1aTargetSpeed = sonar_corr * prev_out.Wheel1aTargetSpeed #0.0
                            # safeOutput.Wheel1bTargetSpeed = sonar_corr * prev_out.Wheel1aTargetSpeed #0.0
                            # safeOutput.Wheel2aTargetSpeed = sonar_corr * prev_out.Wheel1aTargetSpeed #0.0
                            # safeOutput.Wheel2bTargetSpeed = sonar_corr * prev_out.Wheel1aTargetSpeed #0.0
                            # safeOutput.Wheel3aTargetSpeed = sonar_corr * prev_out.Wheel1aTargetSpeed #0.0
                            # safeOutput.Wheel3bTargetSpeed = sonar_corr * prev_out.Wheel1aTargetSpeed #0.0
                            
                    safeOutput.Wheel1aTargetSpeed = 0.0
                    safeOutput.Wheel1bTargetSpeed = 0.0
                    safeOutput.Wheel2aTargetSpeed = 0.0
                    safeOutput.Wheel2bTargetSpeed = 0.0
                    safeOutput.Wheel3aTargetSpeed = 0.0
                    safeOutput.Wheel3bTargetSpeed = 0.0

        if ((controlInput.Slider1Position > 290 and controlOutput.Slider1TargetSpeed > 0) or
            (controlInput.Slider1Position < -290 and controlOutput.Slider1TargetSpeed < 0)):
            safeOutput.Slider1TargetSpeed = 0
            print("SLIDER PROTECTION ACTIVATED ON #1", controlInput.Slider1Position, controlOutput.Slider1TargetSpeed, flush = True)

        if ((controlInput.Slider2Position > 290 and controlOutput.Slider2TargetSpeed > 0) or
            (controlInput.Slider2Position < -290 and controlOutput.Slider2TargetSpeed < 0)):
            safeOutput.Slider2TargetSpeed = 0
            print("SLIDER PROTECTION ACTIVATED ON #2", controlInput.Slider2Position, controlOutput.Slider2TargetSpeed, flush = True)

        if ((controlInput.Slider3Position > 290 and controlOutput.Slider3TargetSpeed > 0) or
            (controlInput.Slider3Position < -290 and controlOutput.Slider3TargetSpeed < 0)):
            safeOutput.Slider3TargetSpeed = 0
            print("SLIDER PROTECTION ACTIVATED ON #3", controlInput.Slider3Position, controlOutput.Slider3TargetSpeed, flush = True)


        self._previous_input = controlInput
        self._previous_output = controlOutput
        return safeOutput
