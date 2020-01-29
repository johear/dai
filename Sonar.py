#!/usr/bin/env python

import time
#import pigpio # http://abyz.co.uk/rpi/pigpio/python.html

#pins for pi


class Sonar:
    def __init__(self, sonar_id):
        
        self._sonar_id = sonar_id
        self._is_activated = 1
              
        # if self._sonar_id == "1a2b3b":
            # self._trigger_pin = 4
            # self._PWM_pin = 17
        # else:
            # self._trigger_pin = 27
            # self._PWM_pin = 22
        
        # # self._hostname = {"1a2b3a": "192.168.1.104","1b2b3a": "192.168.1.101", "1b2a3a": "192.168.1.105","1a2a3a": "192.168.1.102", "1b2b3b": "192.168.1.100","1a2b3b": "192.168.1.100", "1b2a3b": "192.168.1.106","1a2a3b": "192.168.1.103"}
        # self._hostname = {"1a2b3a": "192.168.1.100","1b2b3a": "192.168.1.100", "1b2a3a": "192.168.1.100","1a2a3a": "192.168.1.100", "1b2b3b": "192.168.1.100","1a2b3b": "192.168.1.100", "1b2a3b": "192.168.1.100","1a2a3b": "192.168.1.100"}
       
               
        # self._pi = pigpio.pi(self._hostname[self._sonar_id],8888)
        # self._high_tick = None
        # self._p = None
        # self._high_pulse_length = None
        
        # self._obstacle_distance = 0
        # self._pi.set_pull_up_down(self._trigger_pin, pigpio.PUD_DOWN)
        
        # self._cb = self._pi.callback(self._PWM_pin, pigpio.EITHER_EDGE, self._cbf) #waiting for pulse

    # def _cbf(self,gpio, level, tick):
        # if level == 1:
            # self._high_tick = tick
        # elif level == 0:
            # if self._high_tick is not None:
                # self._high_pulse_length = pigpio.tickDiff(self._high_tick, tick)
                
               
                # if 300 <= self._high_pulse_length <= 5000 and self._is_activated == 1:
                    # self._obstacle_distance = self._high_pulse_length #distance in mm == high pulse length in micros
                # else:
                    # self._obstacle_distance = 0

    # def _cancel(self): #probably don't need this, unless waiting for callback uses too many resources
        # self._cb.cancel()
        
    # @property
    # def triggerSonar(self):
        # #to trigger the sonar, send a HIGH pulse between 0.02mS and 97mS
        # self._pi.gpio_trigger(self._trigger_pin, 50, 1) #pin, length in uS, level
        # #self._pi.set_pull_up_down(self._trigger_pin, pigpio.PUD_UP)
    @property
    def obstacleDistance(self):
        return 10000
        # try:
            # return self._obstacle_distance
        # except:
            # raise Exception("obstacle_distance not defined")
    
    @property
    def activateSonar(self):
    
        try:
            return self._is_activated
        except:
            raise Exception("activation is not defined")
    
    @activateSonar.setter
    def activateSonar(self, activation_state):
        if activation_state == 1:
            # self._pi.set_pull_up_down(self._trigger_pin, pigpio.PUD_UP)
            self._is_activated = activation_state
        elif activation_state == 0:
            # self._pi.set_pull_up_down(self._trigger_pin, pigpio.PUD_DOWN)
            self._is_activated = activation_state
    
    
       
        
# S1_1 = Sonar("1a2a3a") #102 (D2)
# S1_1.activateSonar = 1
# D1_2 = Sonar("1a2b3a") #104 (S1)
# D1_2.activateSonar = 1
# S2_3 = Sonar("1a2b3b") #100 (DB)
# S2_3.activateSonar = 1
# D2_4 = Sonar("1a2a3b") #103 (D3)
# D2_4.activateSonar = 1
# B3a_5 = Sonar("1b2a3a") #105 (S2)
# B3a_5.activateSonar = 1
# B3b_6 = Sonar("1b2b3a") #101 (D1)
# B3b_6.activateSonar = 1
# S4_7 = Sonar("1b2b3b") #100 (DB)
# S4_7.activateSonar = 1
# D4_8 = Sonar("1b2a3b") #106 (S3)
# D4_8.activateSonar = 1

# while True:
    # print("---1---")
    # print(S1_1.obstacleDistance)
    # print("---2---")    
    # print(D1_2.obstacleDistance)
    # print("---3---")
    # print(S2_3.obstacleDistance)
    # print("---4---")
    # print(D2_4.obstacleDistance)    
    # print("---5---")
    # print(B3a_5.obstacleDistance)
    # print("---6---")
    # print(B3b_6.obstacleDistance)
    # print("---7---")
    # print(S4_7.obstacleDistance)
    # print("---8---")
    # print(D4_8.obstacleDistance)
    # time.sleep(1)

# DS1.cancel()
# pi.stop()#!/usr/bin/env python

