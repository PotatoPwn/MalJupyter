# MALJUPYTER

(This project was really built for linux due to its strings functions, but don't let this stop you)

MaJupyter is a jupyter-notebook based program used to perform initial triage of malware.

## Features
- Downloads malware samples from MalwareBazaar based on tags
- Defangs, and Zips the file with the password "infected"
- Extract unicode and encoded strings from sample
- Generates an automatic YaraRule (Cheers to ![Neo23x0](https://github.com/Neo23x0/yarGen) for YaraGen :D )
- Changes name of malware to sha256 hashsum

(Neo23x0 if you want me to take this down as I technically did just take your entire project and chucked it in mine, just shoot me an email and ill quickly take it down.

## Installation

#### Clone Directory
```
git clone https://github.com/Jpang9/MalJupyter
```

### Create a virtual Environment
```
python3 -m venv MalJupyter
```

### Change Directory into Repo
```
cd MalJupyter
```

### Change into Virtual Environment
##### Linux 
```
source bin/activate
```

### Install Requirements
```
pip install -r requirements.txt
```

### Setup YaraGen
```
python3 Tools/yarGen/yarGen.py --update
```

### Move Yargen DB to correct location
```
mv ./db Tools/yarGen/
```

### Start Notebook
```
jupyter notebook
```

## General Usage
Malicious Binaries go into "Samples" directory

Processed Binaries will end up in "Defanged" Directory
