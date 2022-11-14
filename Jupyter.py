import os
import sys
from shutil import copyfile
import hashlib
import pyminizip

#Globals
Samples = "Samples/"
Defanged = "Defanged/"


class MalAnalyst:

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
        savedSampleDirName = Defanged + sampleName
        os.mkdir(savedSampleDirName)
        return savedSampleDirName


    @classmethod
    def moveAndDefang(cls, sampleName):
        suffix = ".Defanged"
        sha256sum = MalAnalyst.retrieveSha256HashSum(Samples + sampleName)
        defangedSampleName = sha256sum + suffix
        defangedSampleDirectory = Defanged + defangedSampleName
        liveSampleDirectory = Samples + sampleName
        copyfile(liveSampleDirectory, defangedSampleDirectory)
        return defangedSampleDirectory # this returns the directory + defanged sample name...


    def retrieveSha256HashSum(sample_name):
        with open(sample_name, "rb") as f:
            bytes = f.read()
            readable_hash = hashlib.sha256(bytes).hexdigest();
            return readable_hash


    @classmethod
    def retrieveStringsFromYarGen(cls, newSampleName):
        sampleFile = Defanged + newSampleName + "/" + newSampleName
        extractedStringsFile = Defanged + newSampleName + "/" + newSampleName + ".txt"
        os.system("python3 Tools/yarGen/yarGen.py -a Potatech -m " + sampleFile + " -o " + extractedStringsFile) # Fix, not writing properly lol
        return extractedStringsFile

    @classmethod
    def zipMaliciousSample(cls, newSampleName): # gonna try and use pyzipmini... :/
        Samplename = Defanged + newSampleName + "/" + newSampleName
        zipFileName = Defanged + newSampleName + "/" + newSampleName + ".zip"
        password = "infected"
        compressLevel = 5
        pyminizip.compress(Samplename, None, zipFileName, password, compressLevel)
        return zipFileName





MalAnalyst.retrieveStringsFromYarGen("8ce845ca0111835d9258432709d61ac932146c02f1baab8bbe605f7522ef1c4d")
MalAnalyst.retrieveStringsFromYarGen("test.exe")