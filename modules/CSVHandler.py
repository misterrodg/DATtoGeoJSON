import csv


class CSVHandler:
    def __init__(self, filePath):
        self.filePath = filePath

    def toDict(self):
        result = []
        with open(self.filePath, 'r') as csvFile:
            data = csv.DictReader(csvFile)
            for d in data:
                result.append(d)
        return result
