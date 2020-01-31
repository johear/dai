#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  26 14:36:19 2019

@author: jonathan
"""
import pybullet as p
import numpy as np

import time
import sys
#some python interpreters need '.' added
sys.path.append(".")
import math

import pybullet_data
from Slider2 import Slider2
from Wheel import Wheel
from InertiaMeter import InertiaMeter
from Camera import Camera


class Simulation:
    
    def __init__(self, start_pos = [0, 0, 0.8], start_orientation = [-0.8923991008299614, 0.09904576054312739, 0.23911761839446172, 0.36964381061999463], urdfRootPath = '/urdf'):
        self.startPos = start_pos
        self.startOrientation = start_orientation
        self.urdfRootPath = urdfRootPath
        self.connect()
        self.reset()
        


    def buildJointNameToIdDict(self):
        nJoints = p.getNumJoints(self.robot)
        self.jointNameToId = {}
        for i in range(nJoints):
            jointInfo = p.getJointInfo(self.robot, i)
            self.jointNameToId[jointInfo[1].decode('UTF-8')] = jointInfo[0]


    def reset(self):   
        #self.startOrientation = p.getQuaternionFromEuler([-2.3561944901795866, 0.5235987755999999, 0])       
        self.robot = p.loadURDF("%s/dai.urdf" % self.urdfRootPath, self.startPos, self.startOrientation)
        self.buildJointNameToIdDict()
        
        self.slider1 = Slider2(self.jointNameToId["SliderMotor1"], self.robot)    
        self.slider2 = Slider2(self.jointNameToId["SliderMotor2"], self.robot)
        self.slider3 = Slider2(self.jointNameToId["SliderMotor3"], self.robot)
        
        self.wheel1a = Wheel(self.jointNameToId["WheelMotor1a"], self.robot)
        self.wheel2a = Wheel(self.jointNameToId["WheelMotor2a"], self.robot)
        self.wheel3a = Wheel(self.jointNameToId["WheelMotor3a"], self.robot)
        self.wheel1b = Wheel(self.jointNameToId["WheelMotor1b"], self.robot)
        self.wheel2b = Wheel(self.jointNameToId["WheelMotor2b"], self.robot)
        self.wheel3b = Wheel(self.jointNameToId["WheelMotor3b"], self.robot)

        self.inertiaMeter = InertiaMeter(self.robot)
        
        self.camera1 = Camera()
        self.camera2 = Camera(((0,0,10), (0,0,0), (0,1,0)), (45.0, 1.0, 0.1, 10.1), 224, 224)


    def stepSimulation(self):
        p.stepSimulation()


    def connect(self):
        self.physicsClient = p.connect(p.DIRECT)# p.DIRECT for non-GUI // p.GUI for GUI
        p.resetSimulation()
        #p.setTimeStep(0.1)
        p.setRealTimeSimulation(1) #0 is off
        p.setAdditionalSearchPath(pybullet_data.getDataPath()) #sets path to use examples from bullet3/data
        planeId = p.loadURDF("%s/J-Plane.urdf" % self.urdfRootPath)
        p.setGravity(0,0,-9.80665)
       
    def disconnect(self):
        p.disconnect()
