#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 16:42:30 2019

@author: jonathan
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Sep  26 14:36:19 2019

@author: jonathan
"""
import pybullet as p


class Camera:

    def __init__(self, viewMatrixList=((0,0,3), (0,0,0), (0,1,0)), projectionMatrixList=(45.0, 1.0, 0.1, 3.1), width=224, height=224):         
        
        self._viewMatrixList = viewMatrixList
        self._projectionMatrixList = projectionMatrixList  
        self._width = width
        self._height = height
        
        self._viewMatrix = p.computeViewMatrix(self._viewMatrixList[0], self._viewMatrixList[1],self._viewMatrixList[2],) # cameraEyePosition=[0, 0, 3], cameraTargetPosition=[0, 0, 0], cameraUpVector=[0, 1, 0]           
        #self._projectionMatrix = p.computeProjectionMatrixFOV(self._projectionMatrixList[0], self._projectionMatrixList[1], self._projectionMatrixList[2], self._projectionMatrixList[3]) # fov=45.0,aspect=1.0, nearVal=0.1, farVal=3.1
        self._projectionMatrix = p.computeProjectionMatrix(-0.5,0.5,-0.5,0.5,0.1,40.0) # Screen left, right, bottom, top, near plane distance, far plane distance // Screen LRTB is for image size from origin (ie. -x,+x,-y,+y)
        
        
    def getCameraImage(self):
        cameraImage = p.getCameraImage(self._width, self._height, viewMatrix=self._viewMatrix, projectionMatrix=self._projectionMatrix)
        
        return cameraImage