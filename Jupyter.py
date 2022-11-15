import os
import sys
from shutil import copyfile
import hashlib
import pyminizip
import string

#Globals
Samples = "Samples/"
Defanged = "Defanged/"


class MalAnalyst:

    def __init__(self, sampleName):
        self.sampleName = sampleName
        self.newSampleName = ""

    @staticmethod
    def checkFolder(dir):
        if not os.path.exists(dir):
            print(dir + " doesn't exist, making file now")
            os.mkdir(dir)
            return True

    @staticmethod
    def checkSamples(dir):
        sample_list = os.listdir(dir)
        if len(sample_list) == 0:
            print("Need Samples to continue")

    @classmethod
    def createSubDirectoryForMalwareSample(cls, sampleName):
        subDirHash = MalAnalyst.retrieveSha256HashSum(sampleName)
        subDirLoc = Defanged + subDirHash
        os.mkdir(subDirLoc)
        return subDirLoc


    @classmethod
    def moveAndDefang(cls, sampleName):
        suffix = ".Defanged"
        sha256sum = MalAnalyst.retrieveSha256HashSum(sampleName)
        defangedSampleName = sha256sum + suffix
        defangedSampleDirectory = Defanged + sha256sum + "/" + defangedSampleName
        liveSampleDirectory = sampleName
        copyfile(liveSampleDirectory, defangedSampleDirectory)
        return defangedSampleDirectory # this returns the directory + defanged sample name...


    def retrieveSha256HashSum(sampleName):
        with open(sampleName, "rb") as f:
            bytes = f.read()
            readable_hash = hashlib.sha256(bytes).hexdigest();
            return readable_hash

    @classmethod
    def retrieveStringsFromYarGen(cls, newFilePath, fileHash):
        pathOfExtraction = newFilePath
        yaraLocation = Defanged + fileHash + "/"
        fileRule = yaraLocation + fileHash + ".yara"
        print(fileHash)
        os.system("python3 Tools/yarGen/yarGen.py -a Potatech -m " + pathOfExtraction + " -o " + fileRule)
        return fileRule

    @classmethod
    def zipMaliciousSample(cls, newSampleName, fileHash, newFilePath): # gonna try and use pyzipmini... :/
        zipFileName = newFilePath + "/" + fileHash + ".zip"
        password = "infected"
        compressLevel = 5
        pyminizip.compress(newSampleName, None, zipFileName, password, compressLevel)
        os.system("rm " + newFilePath + "/*.Defanged")
        return zipFileName

    @classmethod
    def pullStringsEncodedAndUnicode(cls, sampleName, newFilePath):
        encodedStrings = newFilePath + "/" + "ASCII_ENCODED.txt"
        unicodeStrings = newFilePath + "/" + "UNICODE_ENCODED.txt"
        os.system("strings -e b " + sampleName + " > " + encodedStrings)
        os.system("strings -U h " + sampleName + " > " + unicodeStrings)




