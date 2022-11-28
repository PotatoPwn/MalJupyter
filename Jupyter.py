import os
from shutil import move
import hashlib
import pyminizip
import json
import requests
import pyzipper

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
    def querySamplesFromMalBazaar():
        sumarray = []
        malwareBazaarTags = input("What Tags would you like to include: ")
        if len(malwareBazaarTags) == 0:
            malwareBazaarTags = ""
        print("searching for " + malwareBazaarTags)
        querydata = {
            'query': 'get_taginfo',
            'tag': '' + malwareBazaarTags + '',
            'limit': '10'
        }
        queryresponse = requests.post('https://mb-api.abuse.ch/api/v1', data=querydata, timeout=30)
        query_json = json.loads(queryresponse.content)
        if query_json and 'data' in query_json:
            for shasum in query_json['data']:
                sha256sum = shasum.get('sha256_hash')
                sumarray.append(sha256sum)
            return sumarray


    @staticmethod
    def downloadSamplesFromMalBazaar():
        zipPassword = b'infected'
        for sha256sum in MalAnalyst.querySamplesFromMalBazaar():
            headers = {
                "name": sha256sum
            }
            queryData = {
                'query': 'get_file',
                'sha256_hash': sha256sum,
            }
            downloadFiles = requests.post('https://mb-api.abuse.ch/api/v1', data=queryData, timeout=60, headers=headers, allow_redirects=True)
            if 'file_not_found' in downloadFiles.text:
                print(sha256sum + " wasn't found")
            else:
                open(sha256sum + '.zip', 'wb').write(downloadFiles.content)
                print(sha256sum + ".zip has been downloaded")
                move(sha256sum + ".zip", Samples)
                with pyzipper.AESZipFile(Samples + sha256sum + ".zip") as zf:
                    zf.pwd = zipPassword
                    my_secrets = zf.extractall(Samples)
                    print(sha256sum + ".zip" + " has been extracted...")
                    os.remove(Samples + sha256sum + ".zip")
                    print(sha256sum + ".zip has been removed...")



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
        os.system("python3 Tools/yarGen/yarGen.py -m " + pathOfExtraction + " -o " + fileRule)
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




