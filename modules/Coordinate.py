import math


class Coordinate:
    DEG_TO_MIN = 60

    def __init__(self, lat=0.0, lon=0.0):
        self.lat = lat
        self.lon = lon

    def fromDMS(self, latD, latM, latS, lonD, lonM, lonS):
        self.lat = latD + (latM / 60) + (latS / (60*60))
        self.lon = -lonD - (lonM / 60) - (lonS / (60*60))

    def haversineGreatCircleDistance(self, lat, lon):
        # Earth's radius in nautical miles
        earth_radius_nm = 3440.065
        
        # Convert degrees to radians
        lat1 = math.radians(self.lat)
        lon1 = math.radians(self.lon)
        lat2 = math.radians(lat)
        lon2 = math.radians(lon)
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = earth_radius_nm * c
        return distance

    def toString(self):
        result = "[" + str(self.lon) + ", " + str(self.lat) + "]"
        return result
