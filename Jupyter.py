import os
from shutil import move
import hashlib
import pyminizip
from getpass import getpass
import json
import requests

#Globals
Samples = "Samples/"
Defanged = "Defanged/"

class Utils:

    def maliciousConfidence(vtResults):
        try:
            disposition = [r["result"] for r in vtResults["results"]["scans"].values()]
            malicious = list(filter(lambda d: d != None, disposition))
            return round(len(malicious) / len(disposition) * 100, 2)
        except KeyError:
            return None



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

    @staticmethod
    def downloadSamplesFromMalBazaar():
        answer = input("Would you like to download some additional samples from malware bazaar?")
        if answer == "yes" or "y":
            malwareBazaarAPI = getpass("Whats your API Key?")
            malwareBazaarTags = input("What Tags would you like to include:")
            apiHeader = { 'API-KEY': malwareBazaarAPI }
            querydata = {
                'query': 'get_taginfo',
                'tag': ''+malwareBazaarTags+'',
                'limit': '20'
            }
            queryresponse = requests.post('https://mb-api.abuse.ch/api/v1', data=querydata, timeout=15)
            shasums = json.load(queryresponse.text)
            for shasum in shasums:
                malware256shalist = shasum['sha256_hash']
                print(shasum['sha256_hash'])


        else:
            print("Continuing to next instruction...")


    @classmethod
    def moveAndDefang(cls, sampleName):
        suffix = ".Defanged"
        sha256sum = MalAnalyst.retrieveSha256HashSum(sampleName)
        defangedSampleName = sha256sum + suffix
        defangedSampleDirectory = Defanged + sha256sum + "/" + defangedSampleName
        liveSampleDirectory = sampleName
        move(liveSampleDirectory, defangedSampleDirectory)
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




