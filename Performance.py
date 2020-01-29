from pypozyx import Coordinates


class Performance:

    def __init__(self, inertiaMeterBeacons: list, xLength: float, yLength: float, duration: float):    
        self._inertiaMeterBeacon1 = inertiaMeterBeacons[0]
        self._inertiaMeterBeacon2 = inertiaMeterBeacons[1]
        self._inertiaMeterBeacon3 = inertiaMeterBeacons[2]
        self._inertiaMeterBeacon4 = inertiaMeterBeacons[3]
        # self._inertiaMeterBeacon5 = inertiaMeterBeacons[4]
        # self._inertiaMeterBeacon6 = inertiaMeterBeacons[5]
        # self._inertiaMeterBeacon7 = inertiaMeterBeacons[6]
        # self._inertiaMeterBeacon8 = inertiaMeterBeacons[7]
        self._xLength = xLength
        self._yLength = yLength
        self._duration = duration

    @property
    def inertiaMeterBeacon1(self) -> Coordinates:
        return self._inertiaMeterBeacon1

    @property
    def inertiaMeterBeacon2(self) -> Coordinates:
        return self._inertiaMeterBeacon2

    @property
    def inertiaMeterBeacon3(self) -> Coordinates:
        return self._inertiaMeterBeacon3

    @property
    def inertiaMeterBeacon4(self) -> Coordinates:
        return self._inertiaMeterBeacon4
        
    # @property
    # def inertiaMeterBeacon5(self) -> Coordinates:
        # return self._inertiaMeterBeacon5

    # @property
    # def inertiaMeterBeacon6(self) -> Coordinates:
        # return self._inertiaMeterBeacon6
        
    # @property
    # def inertiaMeterBeacon7(self) -> Coordinates:
        # return self._inertiaMeterBeacon7

    # @property
    # def inertiaMeterBeacon8(self) -> Coordinates:
        # return self._inertiaMeterBeacon8

    @property
    def xLength(self) -> float:
        return self._xLength

    @property
    def yLength(self) -> float:
        return self._yLength

    @property
    def duration(self) -> float:
        return self._duration
