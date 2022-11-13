import os
import sys
from datetime import datetime
from shutil import copyfile
import hashlib

#Globals
Samples = "Samples/"
Defanged = "Defanged/"
time = datetime.now()
modified_time = time.strftime("%M-%H-%d-%B-%Y")


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
    def moveAndDefang(cls, sample_name):
        suffix = ".Defanged"
        sha256sum = MalAnalyst.retrieveSha256HashSum(Samples + sample_name)
        defangedSampleName = sha256sum + suffix
        defangedSampleDirectory = Defanged + defangedSampleName
        liveSampleDirectory = Samples + sample_name
        copyfile(liveSampleDirectory, defangedSampleDirectory)
        return defangedSampleDirectory


    def retrieveSha256HashSum(sample_name):
        with open(sample_name, "rb") as f:
            bytes = f.read()
            readable_hash = hashlib.sha256(bytes).hexdigest();
            return readable_hash




MalAnalyst.moveAndDefang("bruhtest.txt", )