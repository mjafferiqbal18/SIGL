# SIG Generator

This script collects logs using SPADE. Make sure to setup [SPADE](https://github.com/zeerakb1/SPADE.git) first
Switch to branch 'version-process'

## Usage

Run the script in the following format:

```bash
./test-spade-script.sh [Number of Graphs] [Software] [Exec path]
```

Number of logs:  Specify the number of logs you want to collect
Software: Specify the software for which you want to collect the log
Exec path:  Specify the executable path of the software

This script will collect Linux Audit Logs and convert them into SIGs in the SPADE JSON format

## Options
-h, --help    Display this help message and exit
-l   List the available softwares



