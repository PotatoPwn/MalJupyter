# MALJUPYTER # placeholder name

(This project was really built for linux due to its strings functions, but don't let this stop you)

MaJupyter is a jupyter-notebook based program used to perform initial triage of malware.

## Features
- Downloads malware samples from MalwareBazaar based on tags
- Defangs, and Zips the file with the password "infected"
- Extract unicode and encoded strings from sample
- Generates an automatic YaraRule (Cheers to Neo23x0 for YaraGen :D )
- Changes name of malware to sha256 hashsum

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
#### Linux 
```
source bin/activate
```
#### Windows
```
script/activate.ps1
```

### Install Requirements
```
pip install -r requirements.txt
```

### Setup YaraGen
```
python Tools/yarGen/yarGen.py --update
```

### Start Notebook
```
jupyter notebook
```

## General Usage
Malicious Binaries go into "Samples" directory

Processed Binaries will end up in "Defanged" Directory
