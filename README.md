# Searchlist

Simple tool to retreive wordlists quickly

## Install

1. Clone the repository and go inside
```bash
$ cd searchlist
```

2. Install dependencies
```bash
$ python3 -m pip install -r requirements.txt
```

3. Edit the configuration file (`searchlist.cfg`)
```cfg
[Extensions]
# Files extension white list:
; .ext
.txt
.lst

[Directories]
# Full paths of your wordlists directories:
; /path/to/wordlists/directory
; /another/path/to/wordlists/directory
```

4. Make an alias
```bash
$ alias searchlist="python3 /path/to/searchlist/searchlist.py"
```

## Usage

```bash
$ searchlist -h
```

## Features
- [x] Search wordlists in several directories
- [x] Configuration file
- [x] Count Lines
- [ ] Option to search query in files
