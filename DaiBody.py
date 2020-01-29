from Wheel import Wheel
from Slider2 import Slider2
from Sonar import Sonar
from InertiaMeter import InertiaMeter
from ControlInput import ControlInput
from ControlOutput import ControlOutput
from SafetyControlModule import SafetyControlModule
from Performance import Performance
from Simulation import Simulation

import numpy as np
from collections import deque
import itertools
import time
from pypozyx import Coordinates, EulerAngles, AngularVelocity, Acceleration

class DaiBody():

    def __init__(self, performance: Performance, safety_module: SafetyControlModule, simulation: Simulation):
        self._performance = performance
        self._safety_module = safety_module

        self._Sim = simulation

        self.wheel1a = self._Sim.wheel1a
        self.wheel2a = self._Sim.wheel2a
        self.wheel3a = self._Sim.wheel3a
        self.wheel1b = self._Sim.wheel1b
        self.wheel2b = self._Sim.wheel2b
        self.wheel3b = self._Sim.wheel3b

        self.slider1 = self._Sim.slider1
        #time.sleep(6)
        self.slider2 = self._Sim.slider2
        #time.sleep(6)
        self.slider3 = self._Sim.slider3
        #time.sleep(6)

        self.sonar1a2a3a = Sonar("1a2a3a")
        self.sonar1a2b3a = Sonar("1a2b3a")
        self.sonar1a2b3b = Sonar("1a2b3b")
        self.sonar1a2a3b = Sonar("1a2a3b")
        self.sonar1b2a3a = Sonar("1b2a3a")
        self.sonar1b2b3a = Sonar("1b2b3a")
        self.sonar1b2b3b = Sonar("1b2b3b")
        self.sonar1b2a3b = Sonar("1b2a3b") 

        self.inertiaMeter = self._Sim.inertiaMeter

        self._experience_memory = deque()



    def initialize(self):
        self.sonar1a2a3a.activateSonar = 1
        self.sonar1a2b3a.activateSonar = 1
        self.sonar1a2b3b.activateSonar = 1
        self.sonar1a2a3b.activateSonar = 1
        self.sonar1b2a3a.activateSonar = 1
        self.sonar1b2b3a.activateSonar = 1
        self.sonar1b2b3b.activateSonar = 1
        self.sonar1b2a3b.activateSonar = 1

        self.slider1.targetSpeed = 0
        self.slider2.targetSpeed = 0
        self.slider3.targetSpeed = 0
        self.wheel1a.targetSpeed = 0
        self.wheel1b.targetSpeed = 0
        self.wheel2a.targetSpeed = 0
        self.wheel2b.targetSpeed = 0
        self.wheel3a.targetSpeed = 0
        self.wheel3b.targetSpeed = 0

        


    def finalize(self):
        self.slider1.targetSpeed = 0
        self.slider2.targetSpeed = 0
        self.slider3.targetSpeed = 0
        self.wheel1a.targetSpeed = 0
        self.wheel1b.targetSpeed = 0
        self.wheel2a.targetSpeed = 0
        self.wheel2b.targetSpeed = 0
        self.wheel3a.targetSpeed = 0
        self.wheel3b.targetSpeed = 0
        self.slider1.closeSerial()
        self.slider2.closeSerial()
        self.slider3.closeSerial()
        self.wheel1a.closeSerial()
        self.wheel2a.closeSerial()
        self.wheel3a.closeSerial()
        self.wheel1b.closeSerial()
        self.wheel2b.closeSerial()
        self.wheel3b.closeSerial()

        self._experience_memory = None

    def observe_control_inputs(self) -> ControlInput:
        controlInput = ControlInput()
        
        start_time=time.time()
        
        controlInput.Wheel1aTargetSpeed = self.wheel1a.targetSpeed
        controlInput.Wheel2aTargetSpeed = self.wheel2a.targetSpeed
        controlInput.Wheel3aTargetSpeed = self.wheel3a.targetSpeed
        controlInput.Wheel1bTargetSpeed = self.wheel1b.targetSpeed
        controlInput.Wheel2bTargetSpeed = self.wheel2b.targetSpeed
        controlInput.Wheel3bTargetSpeed = self.wheel3b.targetSpeed
       
        end_time = time.time()
        print("CTRL INPUT wheels:", end_time-start_time)
        start_time=time.time()
       
        # Don't store values beyond stop limit
        slider1_position = self.slider1.sliderPosition
        if slider1_position <= 300 and slider1_position >= -300:
            controlInput.Slider1Position = slider1_position
        elif slider1_position >= 300:
            controlInput.Slider1Position = 300
        else:
            controlInput.Slider1Position = -300
            
        slider2_position = self.slider2.sliderPosition
        if slider2_position <= 300 and slider2_position >= -300:
            controlInput.Slider2Position = slider2_position
        elif slider2_position >= 300:
            controlInput.Slider2Position = 300
        else:
            controlInput.Slider2Position = -300

        slider3_position = self.slider3.sliderPosition
        if slider3_position <= 300 and slider3_position >= -300:
            controlInput.Slider3Position = slider3_position
        elif slider3_position >= 300:
            controlInput.Slider3Position = 300
        else:
            controlInput.Slider3Position = -300

        controlInput.Slider1TargetSpeed = self.slider1.targetSpeed
        controlInput.Slider2TargetSpeed = self.slider2.targetSpeed
        controlInput.Slider3TargetSpeed = self.slider3.targetSpeed
        
        end_time = time.time()
        print("CTRL INPUT sliders:", end_time-start_time)
        start_time=time.time()

        
        
        position = Coordinates()

        # it seems that sampling the pozyx multiple times in quick succession
        # leads to better results >> moved to Inertiameter.py
        # for i in range(10):
            # new_position = self.inertiaMeter.position
            # # position.x = new_position.x if abs(new_position.x) > abs(position.x) else position.x
            # # position.y = new_position.y if abs(new_position.y) > abs(position.y) else position.y
            # # position.z = new_position.z if abs(new_position.z) > abs(position.z) else position.z
            # position.x += new_position.x / 10.0
            # position.y += new_position.y / 10.0
            # position.z += new_position.z / 10.0
            # linear_acceleration = 0 # self.inertiaMeter.linearAcceleration
            # angular_position = self.inertiaMeter.angularPosition
            # angular_velocity = 0 # self.inertiaMeter.angularVelocity
            
        new_position = self.inertiaMeter.position
        position.x += new_position[0]
        position.y += new_position[1]
        position.z += new_position[2]
        linear_acceleration = 0 # self.inertiaMeter.linearAcceleration
        angular_position = self.inertiaMeter.angularPosition
        angular_velocity = 0 # self.inertiaMeter.angularVelocity

        if position is not None:
            controlInput.XPos = position.x 
            controlInput.YPos = position.y 
            controlInput.ZPos = position.z 
        if angular_position is not None:
            controlInput.PitchAngle = angular_position[1]
            controlInput.RollAngle = angular_position[0]
            controlInput.YawAngle = angular_position[2]

        controlInput.XSpeed = 0.0
        controlInput.YSpeed = 0.0
        controlInput.ZSpeed = 0.0
        controlInput.YawSpeed = 0.0 #angular_velocity.x
        controlInput.PitchSpeed = 0.0 #angular_velocity.y
        controlInput.RollSpeed = 0.0 #angular_velocity.z

        controlInput.XAccel = 0.0 #linear_acceleration.x / 1000
        controlInput.YAccel = 0.0 #linear_acceleration.y / 1000
        controlInput.ZAccel = 0.0 #linear_acceleration.z / 1000
        controlInput.YawAccel = 0.0
        controlInput.PitchAccel = 0.0
        controlInput.RollAccel = 0.0

        controlInput.ObstacleDist_1a2a3a = self.sonar1a2a3a.obstacleDistance
        controlInput.ObstacleDist_1a2b3a = self.sonar1a2b3a.obstacleDistance
        controlInput.ObstacleDist_1a2b3b = self.sonar1a2b3b.obstacleDistance
        controlInput.ObstacleDist_1a2a3b = self.sonar1a2a3b.obstacleDistance
        controlInput.ObstacleDist_1b2a3a = self.sonar1b2a3a.obstacleDistance
        controlInput.ObstacleDist_1b2b3a = self.sonar1b2b3a.obstacleDistance
        controlInput.ObstacleDist_1b2b3b = self.sonar1b2b3b.obstacleDistance
        controlInput.ObstacleDist_1b2a3b = self.sonar1b2a3b.obstacleDistance

        controlInput.ObstacleDanger_1a2a3a = 0.0
        controlInput.ObstacleDanger_1a2b3a = 0.0
        controlInput.ObstacleDanger_1a2b3b = 0.0
        controlInput.ObstacleDanger_1a2a3b = 0.0
        controlInput.ObstacleDanger_1b2a3a = 0.0
        controlInput.ObstacleDanger_1b2b3a = 0.0
        controlInput.ObstacleDanger_1b2b3b = 0.0
        controlInput.ObstacleDanger_1b2a3b = 0.0

        controlInput.SpatialDangerXMin = self._safety_module.check_xMin_bounds(controlInput.XPos)
        controlInput.SpatialDangerXMax = self._safety_module.check_xMax_bounds(controlInput.XPos)
        controlInput.SpatialDangerYMin = self._safety_module.check_yMin_bounds(controlInput.YPos)
        controlInput.SpatialDangerYMax = self._safety_module.check_yMax_bounds(controlInput.YPos)
        end_time = time.time()
        print("CTRL INPUT pozyx:", end_time-start_time)
        start_time=time.time()

        removed_input = ControlInput()
        if (len(self._experience_memory) > 1000) :
            removed_input = self._experience_memory.popleft()
        self._experience_memory.append(controlInput)
        self._update_averages(removed_input, controlInput, len(self._experience_memory))
        
        end_time = time.time()
        print("CTRL INPUT final bit:", end_time-start_time)
        
        
        return controlInput

    def _update_averages(self, rem_input: ControlInput, new_input: ControlInput, count:int):
        self.average_wheel1a_speed += (new_input.Wheel1aTargetSpeed - rem_input.Wheel1aTargetSpeed - self.average_wheel1a_speed) / count
        self.average_wheel1b_speed += (new_input.Wheel1bTargetSpeed - rem_input.Wheel1bTargetSpeed - self.average_wheel1b_speed) / count
        self.average_wheel2a_speed += (new_input.Wheel2aTargetSpeed - rem_input.Wheel2aTargetSpeed - self.average_wheel2a_speed) / count
        self.average_wheel2b_speed += (new_input.Wheel2bTargetSpeed - rem_input.Wheel2bTargetSpeed - self.average_wheel2b_speed) / count
        self.average_wheel3a_speed += (new_input.Wheel3aTargetSpeed - rem_input.Wheel3aTargetSpeed - self.average_wheel3a_speed) / count
        self.average_wheel3b_speed += (new_input.Wheel3bTargetSpeed - rem_input.Wheel3bTargetSpeed - self.average_wheel3b_speed) / count
        self.average_slider1_speed += (new_input.Slider1TargetSpeed - rem_input.Slider1TargetSpeed - self.average_slider1_speed) / count
        self.average_slider2_speed += (new_input.Slider2TargetSpeed - rem_input.Slider2TargetSpeed - self.average_slider3_speed) / count
        self.average_slider3_speed += (new_input.Slider3TargetSpeed - rem_input.Slider3TargetSpeed - self.average_slider3_speed) / count
        self.average_slider1_position += (new_input.Slider1Position - rem_input.Slider1Position - self.average_slider1_position) / count
        self.average_slider2_position += (new_input.Slider2Position - rem_input.Slider2Position - self.average_slider2_position) / count
        self.average_slider3_position += (new_input.Slider3Position - rem_input.Slider3Position - self.average_slider3_position) / count
        self.average_yaw += (new_input.YawAngle - rem_input.YawAngle - self.average_yaw) / count
        self.average_pitch += (new_input.PitchAngle - rem_input.PitchAngle - self.average_pitch) / count
        self.average_roll += (new_input.RollAngle - rem_input.RollAngle - self.average_roll) / count
        self.average_x += (new_input.XPos - rem_input.XPos - self.average_x) / count
        self.average_y += (new_input.YPos - rem_input.YPos - self.average_y) / count
        
        # self.locations_visited[int(rem_input.XPos)][int(rem_input.YPos)] -= 1
        location_x = new_input.XPos + self._performance.xLength/2
        location_x = location_x if location_x >= 0 else 0
        location_x = location_x if location_x <= self._performance.xLength - 1 else self._performance.xLength - 1
        location_y = new_input.YPos + self._performance.yLength/2
        location_y = location_y if location_y >= 0 else 0
        location_y = location_y if location_y <= self._performance.yLength - 1 else self._performance.yLength - 1
        self.locations_visited[int(location_x)][int(location_y)] = 1


    def apply_control_outputs(self, control_output: ControlOutput, time_step: float):
        #safeControlOutput = self._safety_module.sanitize_output(controlInput, controlOutput)
        safeControlOutput = control_output
        self.wheel1a.targetSpeed = safeControlOutput.Wheel1aTargetSpeed
        self.wheel2a.targetSpeed = safeControlOutput.Wheel2aTargetSpeed
        self.wheel3a.targetSpeed = safeControlOutput.Wheel3aTargetSpeed
        self.wheel1b.targetSpeed = safeControlOutput.Wheel1bTargetSpeed
        self.wheel2b.targetSpeed = safeControlOutput.Wheel2bTargetSpeed
        self.wheel3b.targetSpeed = safeControlOutput.Wheel3bTargetSpeed

        self.slider1.targetSpeed = safeControlOutput.Slider1TargetSpeed
        self.slider2.targetSpeed = safeControlOutput.Slider2TargetSpeed
        self.slider3.targetSpeed = safeControlOutput.Slider3TargetSpeed

    def reset(self):
        self._experience_memory = deque()

        self.average_wheel1a_speed = 0
        self.average_wheel1b_speed = 0
        self.average_wheel2a_speed = 0
        self.average_wheel2b_speed = 0
        self.average_wheel3a_speed = 0
        self.average_wheel3b_speed = 0
        self.average_slider1_speed = 0
        self.average_slider2_speed = 0
        self.average_slider3_speed = 0
        self.average_slider1_position = 0
        self.average_slider2_position = 0
        self.average_slider3_position = 0
        self.average_yaw = 0
        self.average_pitch = 0
        self.average_roll = 0
        self.average_x = 0
        self.average_y = 0
        self.locations_visited = np.zeros((int(self._performance.xLength), int(self._performance.yLength)), dtype=np.int)

        self.remaining_energy = 0
        print("reset")


    yaw_reward = False
    pitch_reward = False
    roll_reward = False

    def get_angular_reward(self, elapsed_time) -> (float, bool):
        count = len(self._experience_memory)
        event = self._experience_memory[count-1]
        print("Angualar pos:", event.YawAngle, event.PitchAngle, event.RollAngle, flush = True )

        s1_reward = 0 if event.Slider1Position < 290 and event.Slider1Position > -290 else -1
        s2_reward = 0 if event.Slider2Position < 290 and event.Slider2Position > -290 else -1
        s3_reward = 0 if event.Slider3Position < 290 and event.Slider3Position > -290 else -1

        if count > 20 :
            old_batch = list(itertools.islice(self._experience_memory, count-20, count-11))
            new_batch = list(itertools.islice(self._experience_memory, count-10, count-1))
            old_yaw = np.average(np.asarray([e.YawAngle for e in old_batch]))
            new_yaw = np.average(np.asarray([e.YawAngle for e in new_batch]))
            old_pitch = np.average(np.asarray([e.PitchAngle for e in old_batch]))
            new_pitch = np.average(np.asarray([e.PitchAngle for e in new_batch]))
            old_roll = np.average(np.asarray([e.RollAngle for e in old_batch]))
            new_roll = np.average(np.asarray([e.RollAngle for e in new_batch]))

            # Reward should vary between 0 and 4
            # Reward is reduced to 0.8 until all angles are rotated
            
            y_reward = 0
            p_reward = 0
            r_reward = 0

            if not self.yaw_reward:
                y_reward =  np.absolute(old_yaw - new_yaw) / 45
                if y_reward >= 1:
                    self.yaw_reward = False # True
            else:
                y_reward = np.absolute(old_yaw - new_yaw) / (45 * 5)

            if not self.pitch_reward:
                p_reward =  np.absolute(old_pitch - new_pitch) / 45
                if p_reward >= 1:
                    self.pitch_reward = False # True
            else:
                p_reward = np.absolute(old_pitch - new_pitch) / (45 * 5)

            if not self.roll_reward:
                r_reward =  np.absolute(old_roll - new_roll) / 45
                if r_reward >= 1:
                    self.roll_reward = False # True
            else:
                r_reward = np.absolute(old_roll - new_roll) / (45 * 5)
            
            if self.yaw_reward and self.pitch_reward and self.roll_reward:
                    self.yaw_reward = False
                    self.pitch_reward = False
                    self.roll_reward = False            

            return y_reward + p_reward + r_reward + s1_reward + s2_reward + s3_reward, False

        else :
            return self.get_circular_reward(elapsed_time)[0] + s1_reward + s2_reward + s3_reward, False
            # return s1_reward + s2_reward + s3_reward, False

    slider1_reward = False
    slider2_reward = False
    slider3_reward = False

    def get_slider_reward(self, elapsed_time)->(float, bool):
        count = len(self._experience_memory)
        if count > 20 :
            old_batch = list(itertools.islice(self._experience_memory, count-20, count-11))
            new_batch = list(itertools.islice(self._experience_memory, count-10, count-1))
            event = self._experience_memory[count-1]
            # old_slider1 = np.average(np.asarray([e.Slider1TargetSpeed for e in old_batch]))
            # new_slider1 = np.average(np.asarray([e.Slider1TargetSpeed for e in new_batch]))
            # old_slider2 = np.average(np.asarray([e.Slider2TargetSpeed for e in old_batch]))
            # new_slider2 = np.average(np.asarray([e.Slider2TargetSpeed for e in new_batch]))
            # old_slider3 = np.average(np.asarray([e.Slider3TargetSpeed for e in old_batch]))
            # new_slider3 = np.average(np.asarray([e.Slider3TargetSpeed for e in new_batch]))
            old_slider1 = np.average(np.asarray([e.Slider1Position for e in old_batch]))
            new_slider1 = np.average(np.asarray([e.Slider1Position for e in new_batch]))
            old_slider2 = np.average(np.asarray([e.Slider2Position for e in old_batch]))
            new_slider2 = np.average(np.asarray([e.Slider2Position for e in new_batch]))
            old_slider3 = np.average(np.asarray([e.Slider3Position for e in old_batch]))
            new_slider3 = np.average(np.asarray([e.Slider3Position for e in new_batch]))
            
            print("Slider pos:", event.Slider1Position, event.Slider2Position, event.Slider3Position, flush = True)
            print("Slider 1 old / new:", old_slider1, "/", new_slider1, flush = True)
            print("Slider 2 old / new:", old_slider2, "/", new_slider2, flush = True)
            print("Slider 3 old / new:", old_slider3, "/", new_slider3, flush = True)

            s1_reward = 0
            s2_reward = 0
            s3_reward = 0

            # Reward should vary between 0 and +1 per slider (so 0 to 3 total)
            # Reward is reduced to 0.2 until or sliders are moving
            # Reward is -1 when end reached

            if not self.slider1_reward:
                s1_reward = (np.absolute(old_slider1 - new_slider1) / 50)**2
                if s1_reward >= 10000:
                    self.slider1_reward = True
            else:
                s1_reward = np.absolute(old_slider1 - new_slider1) / (50*5)
            s1_reward = s1_reward if event.Slider1Position < 290 and event.Slider1Position > -290 else -1

            if not self.slider2_reward:
                s2_reward = (np.absolute(old_slider2 - new_slider2) / 50)**2
                if s2_reward >= 10000:
                    self.slider2_reward = True
            else:
                s2_reward = np.absolute(old_slider2 - new_slider2) /  (50*5)
            s2_reward = s2_reward if event.Slider2Position < 290 and event.Slider2Position > -290 else -1
 
            if not self.slider3_reward:
                s3_reward = (np.absolute(old_slider3 - new_slider3) / 50)**2
                if s3_reward >= 10000:
                    self.slider3_reward = True
            else:
                s3_reward = np.absolute(old_slider3 - new_slider3) /  (50*5)
            s3_reward = s3_reward if event.Slider3Position < 290 and event.Slider3Position > -290 else -1
            
            if self.slider1_reward and self.slider2_reward and self.slider3_reward:
                    self.slider1_reward = False
                    self.slider2_reward = False
                    self.slider3_reward = False
            s_reward = s1_reward + s2_reward + s3_reward
            print("Slider reward:", s1_reward, "+", s2_reward, "+", s3_reward, "=",  s_reward, flush = True)
            return s_reward, False

        else :
            return self.get_slider_reward_simple(elapsed_time)

    def get_slider_reward_simple(self, elapsed_time: float) -> (float, bool):
        # Reward should vary between 0 and +1 per slider (so 0 to 3 total)
        # Reward is -1 when end reached
        event = self._experience_memory[len(self._experience_memory)-1]
        reward = np.absolute(event.Slider1TargetSpeed) / 30 if event.Slider1Position < 290 and event.Slider1Position > -290 else -1
        reward += np.absolute(event.Slider2TargetSpeed) / 30 if event.Slider2Position < 290 and event.Slider2Position > -290 else -1
        reward += np.absolute(event.Slider3TargetSpeed) / 30 if event.Slider3Position < 290 and event.Slider3Position > -290 else -1
        print("Slider reward:", reward, flush = True)
        print("Positions:", event.Slider1Position, event.Slider2Position, event.Slider3Position, flush = True)
        return reward, False

    def get_energy_conservation(self, elapsed_time: float) -> (float, bool):
        # Reward should vary between -3 and +1.5
        # Missing absolute values!!!
        event = self._experience_memory[len(self._experience_memory)-1]
        reward = (40 - (event.Slider1TargetSpeed/3 + event.Slider2TargetSpeed/3 + event.Slider3TargetSpeed/3 +
            event.Wheel1aTargetSpeed*10 + event.Wheel2aTargetSpeed*10 + event.Wheel3aTargetSpeed*10 +
            event.Wheel1bTargetSpeed*10 + event.Wheel2bTargetSpeed*10 + event.Wheel3bTargetSpeed*10))
        reward = reward / 20
        print("Energy reward:", reward, flush = True)
        return reward, False


    def get_geometric_reward(self, elapsed_time: float) -> (float, bool):
        reward = 0
        if (len(self._experience_memory) >= 2):
            now = self._experience_memory[len(self._experience_memory)-1]
            before = self._experience_memory[len(self._experience_memory)-2]
            xn = now.XPos
            yn = now.YPos
            xb = before.XPos
            yb = before.YPos
            
            # Take a 1m safety margin
            xL = self._performance.xLength - 2 * self._safety_module._safety_margin - 1
            yL = self._performance.yLength - 2 * self._safety_module._safety_margin - 1

            # Nice big circle radius
            R = xL/2.0 if xL < yL else yL/2.0
            R2 = R**2

            # Distances from center squared
            dn2 = xn**2 + yn**2
            db2 = xb**2 + yb**2
            # Distance between the 2 points
            dnb2 = (xn-xb)**2 + (yn-yb)**2

            
            # if a reasonable amount of movement and both points are close to the radius give a reward
            if dnb2 > 0.1*R2 and (dn2 < 1.10*R2 and dn2 > 0.90*R2) and (db2 < 1.10*R2 and db2 > 0.90*R2):
                reward = dnb2/(0.1*R2)

            print("Geometric reward:", reward, " for diameter:", R, flush = True)
        return reward, False

    def get_location_reward(self, elapsed_time: float) -> (float, bool):
        # Reward should vary between -1 and +1
        percentage_of_time = elapsed_time / self._performance.duration
        target_visits = int(self._performance.duration / 10 * percentage_of_time)
        target_visits = target_visits if target_visits > 0 else 1.0
        visit_count = sum(map(sum, self.locations_visited))
        reward = 1 + (target_visits - visit_count)/target_visits if visit_count > target_visits else 1 + (visit_count - target_visits)/target_visits
        print("Location reward:", reward, "Target:", target_visits, "Visited:", visit_count, flush = True)
        return reward, False

    def get_energy_management_reward(self, elapsed_time: float) -> (float, bool):
        percentage_of_time = elapsed_time / self._performance.duration
        event = self._experience_memory[len(self._experience_memory)-1]

        # Accumulate energy by default
        self.remaining_energy += 10

        # Full power on 3 wheels depletes energy reserve in 5s, 20 units per iteration
        wheelEnergy = (
            np.absolute(event.Wheel1aTargetSpeed) + np.absolute(event.Wheel2aTargetSpeed) + np.absolute(event.Wheel3aTargetSpeed) +
            np.absolute(event.Wheel1bTargetSpeed) + np.absolute(event.Wheel2bTargetSpeed) + np.absolute(event.Wheel3bTargetSpeed)) / 1.5

        # Full power on 3 sliders depletes energy reserve in 6.5s, 15 units per iteration
        sliderEnergy = (np.absolute(event.Slider1TargetSpeed) + np.absolute(event.Slider2TargetSpeed) + np.absolute(event.Slider3TargetSpeed)) / 6

        self.remaining_energy -= (wheelEnergy + sliderEnergy)

        reward = 0
        # negative reward if not doing enough
        if self.remaining_energy > 100:
            reward = (100 - self.remaining_energy) / 100
        # negative reward if doing too much
        elif self.remaining_energy < -100:
            reward = (100 + self.remaining_energy) / 100
        # reward for taking the time to recuperate
        elif self.remaining_energy > 50:
            reward = 2 * (100 - self.remaining_energy) / 100
        # reward for using bursts of energy
        elif self.remaining_energy < -50:
            reward = 2 * (100 + self.remaining_energy) / 100

        print("Energy management reward:", reward, "Wheel energy:", wheelEnergy, "Slider energy:", sliderEnergy, flush = True)
        return reward, False


    def get_status(self, elapsed_time: float)-> (float, bool):
        # return self.get_slider_reward(elapsed_time)[0],False
        # return self.get_location_reward(elapsed_time)
        # return self.get_energy_management_reward(elapsed_time)

        #return self.get_geometric_reward(elapsed_time)
        return self.get_slider_reward(elapsed_time)[0] + self.get_location_reward(elapsed_time)[0] + self.get_angular_reward(elapsed_time)[0] + self.get_energy_management_reward (elapsed_time)[0], False
        
        # return (4 * self.get_slider_reward_simple(elapsed_time)[0]) + self.get_angular_reward(elapsed_time)[0] + self.get_energy_conservation(elapsed_time)[0], False
        # return self.get_slider_reward_simple(elapsed_time)[0] + self.get_angular_reward(elapsed_time)[0] + self.get_energy_conservation(elapsed_time)[0], False
        
        # return self.get_circular_reward(elapsed_time)
        # return self.get_slider_reward(elapsed_time)
        # return self.get_angular_reward(elapsed_time)[0] + self.get_energy_conservation(elapsed_time)[0], False
        # return self.get_angular_reward(elapsed_time)
        # return self.get_slider_reward_simple(elapsed_time)
        # reward = 0.0*self.get_circular_reward(elapsed_time)[0] + 1.0*self.get_slider_reward(elapsed_time)[0] + 0.0*self.get_angular_reward(elapsed_time)[0]
        # return reward, self.get_circular_reward(elapsed_time)[1]
        # return reward, False

    default_speed = 0.1
    circle_diameter = 4.0
    circle_circumference = circle_diameter * np.pi
    lap_time = circle_circumference / default_speed

    def get_circular_reward(self, elapsed_time: float) -> (float, bool):
        # Reward is a maximum of 2 and a minimum of -2
        state = self.observe_control_inputs()
        laps = elapsed_time / self.lap_time
        self.expected_position = self._get_reference_position(laps - np.trunc(laps))
        error = self._get_error(Coordinate(state.XPos, state.YPos), self.expected_position).get_distance()
        print("Expected:", self.expected_position.x, ",", self.expected_position.y, " / Current:", state.XPos, ",", state.YPos, flush = True)
        reward = (self.circle_diameter/2 - error)
        run_terminate = False
        if error > self.circle_diameter:
            run_terminate = True
            print("Terminating on error", error)
        return reward, run_terminate


    def _get_error(self, position, expectedPosition):
        return Coordinate(expectedPosition.x - position.x, expectedPosition.y - position.y)

    def _get_reference_position(self, lapPercentage):
        radians = 2 * np.pi * lapPercentage
        return Coordinate(np.sin(radians) * self.circle_diameter / 2, np.cos(radians) * self.circle_diameter / 2)



class Coordinate:

    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value

    def get_squared(self):
        return self._x**2 + self._y**2

    def get_distance(self):
        return self.get_squared()**0.5