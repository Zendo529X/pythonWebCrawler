
import os
import shutil



class DownloadUtil():

    def createOrDelDir(self, dirName):
        if (os.path.exists(dirName)):
            shutil.rmtree(dirName)
            os.mkdir(dirName)
        else:
            os.mkdir(dirName)
