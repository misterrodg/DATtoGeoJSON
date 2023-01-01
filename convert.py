import argparse
import os

from modules.Coordinate import Coordinate
from modules.CSVHandler import CSVHandler
from modules.DAT import DAT
from modules.FileHandler import FileHandler


def processFiles(sourceDir, outputDir, radiusLimit=None, testFormat=False):
    fileHandler = FileHandler()
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


def checkRange(rangeValue):
    result = None
    if rangeValue != None and rangeValue != '':
        result = tryIntParse(rangeValue)
    return result


def checkCenterpoint(latValue, lonValue):
    result = None
    if latValue != None and latValue != '' and lonValue != None and lonValue != '':
        lat = tryFloatParse(latValue)
        lon = tryFloatParse(lonValue)
        result = Coordinate(lat, lon)
    return result


def readFileList(sourceDir, outputDir, fileListFileName, testFormat=False):
    fileHandler = FileHandler()
    print("\nReading File List")
    fileHandler.checkDir(outputDir)
    fileHandler.deleteAllInSubdir(".geojson", outputDir)
    if not (os.path.exists(sourceDir + "/" + fileListFileName)):
        print("!!! Unable to find FileList.csv")
        print("!!! Check that the file has been generated via switch '--filelist' and is in ./output")
    else:
        csvFile = CSVHandler(sourceDir + "/" + fileListFileName)
        fileList = csvFile.toDict()
        numFiles = str(len(fileList))
        print("Found " + numFiles + " .dat files in " + fileListFileName)
        fileCount = 0
        for f in fileList:
            fileData = fileHandler.splitFolderFile(f['SourcePath'], sourceDir)
            folder = fileData[0]
            fileName = fileData[1].replace(".dat", "")
            radiusLimit = None
            destFileName = None
            centerpoint = None
            if 'Range' in f:
                radiusLimit = checkRange(f['Range'])
            if 'OutputFileName' in f:
                destFileName = f['OutputFileName']
            if 'CenterpointLat' in f and 'CenterpointLon' in f:
                centerpoint = checkCenterpoint(
                    f['CenterpointLat'], f['CenterpointLon'])
            print("[" + str(fileCount + 1) + "/" + numFiles + "] " +
                  "Processing " + fileName + ".dat")
            DAT(sourceDir, outputDir, folder, fileName,
                radiusLimit, testFormat, destFileName, centerpoint)
            fileCount += 1


def buildFileList(sourceDir, fileListFileName):
    fileHandler = FileHandler()
    print("\nFinding Source Files")
    fileHandler.deleteAllInSubdir(".csv", sourceDir)
    fileList = fileHandler.searchForType(".dat", sourceDir)
    numFiles = str(len(fileList))
    print("Found " + numFiles + " .dat files in ./" + sourceDir)
    fileListFile = open(sourceDir + "/" + fileListFileName, "a")
    fileListFile.write(
        "SourcePath,Range,OutputFileName,CenterpointLat,CenterpointLon\n")
    for f in fileList:
        fileListFile.write(f + "\n")
    fileListFile.close()
    print("\n>>>>> File List complete. List located at ./" +
          fileListFileName + " <<<<<\n")


def main():
    # Set up Defaults
    SOURCE_DIR = "dat_source"
    OUTPUT_DIR = "output"
    FILE_LIST_NAME = "FileList.csv"
    # Set up Argument Handling
    parser = argparse.ArgumentParser(description="DATtoGeoJSON Converter")
    parser.add_argument(
        "--radius", type=int, help="The limit radius from the center point declared in the file.")
    parser.add_argument(
        "--test", action=argparse.BooleanOptionalAction)
    parser.add_argument(
        "--filelist", action=argparse.BooleanOptionalAction)
    parser.add_argument(
        "--readlist", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    radiusLimit = None
    testFormat = False
    fileList = False
    readList = False
    if args.radius != None or args.test != None or args.filelist != None or args.readlist != None:
        print("\nOverriding Defaults")
        if args.radius != None:
            radiusLimit = args.radius
            print(">>> Using radius " + str(radiusLimit))
        if args.test != None:
            testFormat = True
            print(">>> Using Lon/Lat formatting.")
        if args.filelist != None:
            fileList = True
            print(">>> Building File List")
        if args.readlist != None and args.filelist == None:
            readList = True
            print(">>> Building From File List")

    if fileList:
        buildFileList(SOURCE_DIR, FILE_LIST_NAME)
    if readList:
        readFileList(SOURCE_DIR, OUTPUT_DIR, FILE_LIST_NAME, testFormat)
    else:
        processFiles(SOURCE_DIR, OUTPUT_DIR, radiusLimit, testFormat)


if __name__ == "__main__":
    main()
