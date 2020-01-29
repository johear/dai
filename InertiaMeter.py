# -*- coding: utf-8 -*-

import pybullet as p


class InertiaMeter:
    
    def __init__(self, robot):  
        
        self._robot = robot
        
        
    @property    
    def position(self):        
            self._agentPosition = p.getBasePositionAndOrientation(self._robot)[0]     
            self._position = self._agentPosition
                   
            return self._position

     
    @property           
    def angularPosition(self): #angularPosition         
            self._agentOrientation = p.getBasePositionAndOrientation(self._robot)[1]          
            self._angularPosition = p.getEulerFromQuaternion(self._agentOrientation)
            
            return self._angularPosition


  

