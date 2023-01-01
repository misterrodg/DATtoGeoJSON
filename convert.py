import argparse
import os

from modules.Coordinate import Coordinate
from modules.CSVHandler import CSVHandler
from modules.DAT import DAT
from modules.FileHandler import FileHandler




def tryIntParse(value):
    result = None
    try:
        intParse = int(value)
    except ValueError as verr:
        pass
    if isinstance(intParse, int):
        result = intParse
    return result


def tryFloatParse(value):
    result = None
    try:
        floatParse = float(value)
    except ValueError as verr:
        pass
    if isinstance(floatParse, float):
        result = floatParse
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
