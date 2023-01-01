class LineString:
    def __init__(self):
        self.type = "Feature"
        self.geometryType = "LineString"
        self.coordinates = []

    def addCoordinate(self, coordinate):
        self.coordinates.append(coordinate)

    def toString(self):
        coords = ",\n\t\t\t\t\t".join(self.coordinates)
        result = "{\n\t\t\t\"type\": \"Feature\",\n\t\t\t\"geometry\": {\n\t\t\t\t\"type\": \"LineString\",\n\t\t\t\t\"coordinates\": [\n\t\t\t\t\t" + \
            coords + \
            "\n\t\t\t\t]\n\t\t\t},\n\t\t\t\"properties\":{\n\t\t\t\t\"style\": \"solid\",\n\t\t\t\t\"thickness\":1\n\t\t\t}\n\t\t}"
        self.coordinates.clear()
        return result
