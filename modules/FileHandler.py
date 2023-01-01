import os


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
