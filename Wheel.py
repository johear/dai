# -*- coding: utf-8 -*-
"""
Created on Thu Sep  26 14:36:19 2019

@author: jonathan
"""
import pybullet as p
import math


class Wheel:
    
    def __init__(self, wheel_id, robot):  
        self._wheel_id = wheel_id
        self._robot = robot
        self._target_speed = 0
        self._freewheel_mode = 0
            
        self._max_rpm = 17040/64 #motor peak rpm / gear ratio
        self._max_speed = self._max_rpm * (math.pi/30) #max speed in radians per second 27.881634801
        self._max_force = 100


    @property
    def targetSpeed(self):
        try:
            return self._target_speed
        except:
            raise Exception("target_speed not defined")
            

    @targetSpeed.setter
    def targetSpeed(self, target_speed_rad):
        self._target_speed = target_speed_rad
        if -self._max_speed <= self._target_speed <= self._max_speed:
            self.setWheelVelocityById(self._wheel_id, target_speed_rad)
        else:
            print("problem: Wheel target_speed is: ", target_speed_rad, "\nShould be (+ or -): ", self._max_speed)
            

    # targetVelocity in radians/second (2pi() = 1 revolution), PeakRS775 = 27.88 rad/s = 1.74 m/s // 1m/s = 16 rad/s// 0.5 m/s = 8 rad/s
    def setWheelVelocityById(self, wheelMotorId, desiredVelocity):
        p.setJointMotorControl2(bodyIndex=self._robot,
                                jointIndex=wheelMotorId,
                                controlMode=p.VELOCITY_CONTROL,
                                targetVelocity=desiredVelocity,
                                force=self._max_force)

    def closeSerial(self): #empty function, for the close serial calls
        print ("Attempted to close serial in the simulation...no harm done")
        