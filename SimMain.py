#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  26 14:36:19 2019

@author: jonathan
"""
import time

from Simulation import Simulation

S1 = Simulation()

# Logging, STATE_LOGGING_VIDEO_MP4 records an .mp4 file. STATE_LOGGING_GENERIC_ROBOT can be replayed as a simulation (I think)
#p.startStateLogging(p.STATE_LOGGING_VIDEO_MP4, "Logging/Dai-Log-Recording-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".mp4")

for __ in range(50000): # __ is just a throwaway variable
    #max speed: slider = 600, wheel = 27.881634801
    S1.slider1.targetSpeed = 100
    S1.slider2.targetSpeed = 100
    S1.slider3.targetSpeed = 100
    S1.wheel1a.targetSpeed = 27
    S1.wheel2a.targetSpeed = 27
    S1.wheel3a.targetSpeed = 27
    
    if __ % 1000 == 0:
        Xpos = S1.inertiaMeter.position[0] * 1000
        Ypos = S1.inertiaMeter.position[1] * 1000
        Zpos = S1.inertiaMeter.position[2] * 1000
        
        RollAngle = S1.inertiaMeter.angularPosition[0] # around X
        PitchAngle = S1.inertiaMeter.angularPosition[1] # around Y
        YawAngle = S1.inertiaMeter.angularPosition[2] # around Z
        
        print("X: ", Xpos)
        print("Y: ", Ypos)
        print("Z: ", Zpos)
        
        print("Roll (around X):", RollAngle)
        print("Pitch (around Y):", PitchAngle)
        print("Yaw (around Z):", YawAngle)
        print("Slider 1 position : ", S1.slider1.sliderPosition)
        
        #S1.camera1.getCameraImage()
#        S1.camera2.getCameraImage()
        
    S1.stepSimulation()

for __ in range(50000): 
    S1.slider1.targetSpeed = -150
    S1.slider2.targetSpeed = -150
    S1.slider3.targetSpeed = -150
    S1.wheel1a.targetSpeed = -17
    S1.wheel2a.targetSpeed = -17
    S1.wheel3a.targetSpeed = -17
    S1.stepSimulation()

time.sleep(1) # a little pause before disconnect
S1.disconnect()