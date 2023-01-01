import math


class Coordinate:
    DEG_TO_MIN = 60

    def __init__(self, lat=0.0, lon=0.0):
        self.lat = lat
        self.lon = lon

    def fromDMS(self, latD, latM, latS, lonD, lonM, lonS):
        self.lat = latD + (latM / 60) + (latS / (60*60))
        self.lon = -lonD - (lonM / 60) - (lonS / (60*60))

    def haversineGreatCicleDistance(self, lat, lon):
        theta = self.lon - lon
        arc = math.degrees(math.acos((math.sin(math.radians(self.lat)) * math.sin(math.radians(lat))) + (
            math.cos(math.radians(self.lat)) * math.cos(math.radians(lat)) * math.cos(math.radians(theta)))))
        distance = arc * self.DEG_TO_MIN
        return distance

    def toString(self, testFormat=False):
        result = "[" + str(self.lat) + ", " + str(self.lon) + "]"
        if (testFormat):
            result = "[" + str(self.lon) + ", " + str(self.lat) + "]"
        return result
