import os
import math
import argparse


class FileHandler:
    def __init__(self):
        self.localPath = os.getcwd()

    def checkDir(self, subdirPath):
        result = False
        dirPath = self.localPath + "/" + subdirPath
        os.makedirs(name=dirPath, exist_ok=True)
        if os.path.exists(dirPath):
            result = True
        return result

    def deleteAllInSubdir(self, fileType, subdirPath=None):
        # As it stands, this will only ever delete items in the named subfolder where this script runs.
        # Altering this function could cause it to delete the entire contents of other folders where you wouldn't want it to.
        # Alter this at your own risk.
        if subdirPath != None:
            deletePath = self.localPath + "/" + subdirPath
            for f in os.listdir(deletePath):
                if f.endswith(fileType):
                    os.remove(os.path.join(deletePath, f))

    def searchForType(self, fileType, subdirPath=None):
        result = []
        searchPath = self.localPath
        if subdirPath != None:
            searchPath += "/" + subdirPath
        for (dirpath, subdirs, files) in os.walk(searchPath):
            result.extend(os.path.join(dirpath, f)
                          for f in files if f.endswith(fileType))
        return result

    def splitFolderFile(self, fullPath, subdirPath=None):
        result = []
        split = os.path.split(fullPath)
        searchPath = self.localPath
        if subdirPath != None:
            searchPath += "/" + subdirPath
        result.append(split[0].replace(searchPath, ''))
        result.append(split[1])
        return result


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


class DAT:
    def __init__(self, sourceFolder, outputFolder, facFolder, fileName, limit=None, testFormat=False):
        self.fileName = "./" + sourceFolder + "/" + facFolder + "/" + fileName + ".dat"
        folderPrefix = ""
        if facFolder != "":
            folderPrefix = facFolder + "_"
        self.outputFileName = "./" + outputFolder + \
            "/" + folderPrefix + fileName + ".geojson"
        self.limit = limit
        self.testFormat = testFormat
        self.pot = None
        self.read()

    def lineToCoordinate(self, line):
        latD = int(line[3:5])
        latM = int(line[6:8])
        latS = float(line[9:16])
        lonD = int(line[18:21])
        lonM = int(line[22:24])
        lonS = float(line[25:32])
        result = Coordinate()
        result.fromDMS(latD, latM, latS, lonD, lonM, lonS)
        if self.pot != None:
            distance = result.haversineGreatCicleDistance(
                self.pot.lat, self.pot.lon)
            if self.limit != None:
                if distance == 0 or distance > self.limit:
                    result = -1
        return result

    def read(self):
        datFile = open(self.fileName, "r")
        geoJson = GeoJSON()
        lineString = LineString()
        for line in datFile:
            if self.pot == None:
                if line[:1] != "!" and line[:4] != "LINE":
                    self.pot = self.lineToCoordinate(line)
            else:
                if line[:1] != "!" and line[:4] == "LINE":
                    if len(lineString.coordinates) > 1:
                        geoJson.addFeature(lineString.toString())
                else:
                    coordinate = self.lineToCoordinate(line)
                    if coordinate != -1:
                        lineString.addCoordinate(
                            coordinate.toString(self.testFormat))

        data = geoJson.toString()
        if os.path.exists(self.outputFileName):
            os.remove(self.outputFileName)
        resultFile = open(self.outputFileName, "w")
        for line in data:
            resultFile.write(line)
        resultFile.close()
        datFile.close()


def main():
    DEFAULT_RADIUS_LIMIT = 40
    # Set up Argument Handling
    parser = argparse.ArgumentParser(description="DATtoGeoJSON Converter")
    parser.add_argument(
        "--radius", type=int, help="The limit radius from the center point declared in the file.")
    parser.add_argument(
        "--test", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    radiusLimit = DEFAULT_RADIUS_LIMIT
    if args.radius != None or args.test != None:
        print("\nOverriding Defaults")
        if args.radius != None:
            radiusLimit = args.radius
        testFormat = False
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
