import os
import argparse


class GeoJSON:
    def __init__(self):
        self.type = "FeatureCollection"
        self.features = []

    def addFeature(self, feature):
        self.features.append(feature)

    def toString(self):
        features = ",\n\t\t".join(self.features)
        return "{\n\t\"type\": \"FeatureCollection\",\n\t\"features\": [\n\t\t" + features + "\n\t]\n}"


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




def main():
    DEFAULT_RADIUS_LIMIT = 140
    # Set up Argument Handling
    parser = argparse.ArgumentParser(description="DATtoGeoJSON Converter")
    parser.add_argument(
        "--radius", type=int, help="The limit radius from the center point declared in the file.")
    parser.add_argument(
        "--test", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    radiusLimit = DEFAULT_RADIUS_LIMIT
    testFormat = False
    if args.radius != None or args.test != None:
        print("\nOverriding Defaults")
        if args.radius != None:
            radiusLimit = args.radius
            print(">>> Using radius " + str(radiusLimit))
        if args.test != None:
            testFormat = True
            print(">>> Using Lon/Lat formatting.")

    # Set up Script
    fileHandler = FileHandler()
    sourceDir = "dat_source"
    outputDir = "output"
    print("\nInitializing GeoJSON Converter")
    fileHandler.checkDir(outputDir)
    fileHandler.deleteAllInSubdir(".geojson", outputDir)
    fileList = fileHandler.searchForType(".dat", sourceDir)
    numFiles = str(len(fileList))
    print("Found " + numFiles + " .dat files in ./" + sourceDir)
    fileCount = 0
    for f in fileList:
        fileData = fileHandler.splitFolderFile(f, sourceDir)
        folder = fileData[0]
        fileName = fileData[1].replace(".dat", "")
        print("[" + str(fileCount + 1) + "/" + numFiles + "] " +
              "Processing " + fileName + ".dat")
        DAT(sourceDir, outputDir, folder, fileName, radiusLimit, testFormat)
        fileCount += 1
    print("\n>>>>> Conversion complete. Files located in ./" + outputDir + " <<<<<\n")


if __name__ == "__main__":
    main()
