import os
from typing import Optional

from modules.Coordinate import Coordinate
from modules.GeoJSON import GeoJSON
from modules.LineString import LineString


class DAT:
    DEFAULT_RADIUS_LIMIT = 140
    fileName: str
    outputFileName: str
    limit: Optional[float]
    pot: Optional[Coordinate]

    def __init__(
        self,
        sourceFolder,
        outputFolder,
        facFolder,
        fileName,
        limit=None,
        destFileName=None,
        centerpoint=None,
    ) -> None:
        self.fileName = "./" + sourceFolder + "/" + facFolder + "/" + fileName + ".dat"
        folderPrefix = ""
        if facFolder != "":
            folderPrefix = facFolder + "_"
        outputFileName = fileName
        if destFileName != None:
            outputFileName = destFileName
        self.outputFileName = (
            "./" + outputFolder + "/" + folderPrefix + outputFileName + ".geojson"
        )
        self.limit = limit
        if limit == None:
            self.limit = self.DEFAULT_RADIUS_LIMIT
        self.pot = None
        if centerpoint != None:
            self.pot = centerpoint
        self.read()

    def lineToCoordinate(self, line) -> Optional[Coordinate]:
        latD = int(line[3:5])
        latM = int(line[6:8])
        latS = float(line[9:16])
        lonD = int(line[18:21])
        lonM = int(line[22:24])
        lonS = float(line[25:32])
        result = Coordinate()
        result.fromDMS(latD, latM, latS, lonD, lonM, lonS)
        if self.pot != None and self.pot.lat and self.pot.lon:
            distance = result.haversineGreatCircleDistance(self.pot.lat, self.pot.lon)
            if self.limit != None:
                if distance == 0 or distance > self.limit:
                    result = None
        return result

    def read(self) -> None:
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
                    lineString = LineString()
                else:
                    coordinate = self.lineToCoordinate(line)
                    if coordinate is not None:
                        lineString.addCoordinate(coordinate.toString())

        if len(lineString.coordinates) > 1:
            geoJson.addFeature(lineString.toString())

        data = geoJson.toString()
        if os.path.exists(self.outputFileName):
            os.remove(self.outputFileName)
        resultFile = open(self.outputFileName, "w")
        for line in data:
            resultFile.write(line)
        resultFile.close()
        datFile.close()
