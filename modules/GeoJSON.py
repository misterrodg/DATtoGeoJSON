class GeoJSON:
    def __init__(self):
        self.type = "FeatureCollection"
        self.features = []

    def addFeature(self, feature):
        self.features.append(feature)

    def toString(self):
        features = ",\n\t\t".join(self.features)
        return "{\n\t\"type\": \"FeatureCollection\",\n\t\"features\": [\n\t\t" + features + "\n\t]\n}"
