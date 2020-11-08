# PNoCSystemLevelSimulation
This repo contains code snippets for processing results of various simulators like Cacti, NVmain, Noxim, Dsent and NVsim 
1. Processresult.py - this script parses the output files of the simulators and extracts the required parameters which can be set by the user. The extracted parameters are stored in a csv.
2. Basecoderun.py - this script is used to execute a command on the console with various parameters for example: each benchmarkfile the command changes. This script basically automates he manual effort of running the command. Given the folder of the benchmarkfiles, script constructs commands for each benchmark and stores result in the specific location  

