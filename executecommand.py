#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 10:05:23 2019

@author: sairam
"""
#os.system("cd /home/sairam/Desktop/assignment/cacti/ && ./cacti -infile sample_config_files/lpddr3_cache.cfg >32CacheSize.txt")
import os
class ExecuteCommand():
    def __init__(self):
        pass
    def executeCommand(self,command):
        os.system(command)
        print("command sucessfully executed: "+command)
    def constructCommand(self,toolCommand,commandpostfix,toolLocation,configFilePath,configFileName,resultFilePath,resultFileName): 
        command="cd "+toolLocation+" && "+toolCommand+" "+configFilePath+configFileName+" "+commandpostfix+" >"+resultFilePath+resultFileName
        print(command)
        return command