# -*- coding: utf-8 -*-
"""
Created on Thu Sep  26 14:36:19 2019

@author: jonathan
"""
import pybullet as p


class Slider2:

    def __init__(self, slider_id, robot):      
        self._slider_id = slider_id
        self._robot = robot
        self._max_speed = 600 # mm/s
        self._max_force = 300
        self._slider_position = 0
        self._current_target_speed = 0
   
    
    @property
    def targetSpeed(self):
        try:
            return self._target_speed
        except:
            raise Exception("target_speed not defined")  
   
    
    @targetSpeed.setter
    def targetSpeed(self, target_speed_mm_s):
        self._target_speed = target_speed_mm_s / 1000     
        self._current_target_speed = target_speed_mm_s 
        
        if -self._max_speed <= target_speed_mm_s <= self._max_speed:
            self.setSliderVelocityById(self._slider_id, self._target_speed)              
        else:
            print("problem: Slider target_speed is: ", target_speed_mm_s, "\nShould be (+ or -): ", self._max_speed)
    
    
    def setSliderVelocityById(self, sliderMotorId, desiredVelocity):
        p.setJointMotorControl2(bodyIndex=self._robot,
                                jointIndex=sliderMotorId,
                                controlMode=p.VELOCITY_CONTROL,
                                targetVelocity=desiredVelocity,                               
                                force=self._max_force)


    @property
    def sliderPosition(self):
        try:          
            self._slider_position = p.getJointState(self._robot, self._slider_id)[0] * 1000
            return self._slider_position
        except:
            print("Error retrieving slider position: ", self._slider_position)
    
    
    @property
    def stopperProximityLevel(self):
        try:
            if self._slider_position > 289:
                return (300 - self._slider_position)/10
            elif self._slider_position < -289:
                return (-300 - self._slider_position)/10
            else:
                return 1
        except:
            raise Exception("Slider position is not defined")

    def closeSerial(self): #empty function, for the close serial calls
        print ("Attempted to close serial in the simulation...no harm done")
        