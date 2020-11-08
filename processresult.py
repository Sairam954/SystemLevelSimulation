#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 13:25:09 2019

@author: sairam
"""
from readconfig import ReadInputConfig
import csv
import matplotlib.pyplot as plt
import pandas as pd
from os import listdir
from os.path import isfile, join
import re

class processResult():
    def __init__(self):
        pass
    def resultLinesList(self,filePath):
        linesList =[]
        with open(filePath,'r') as resultFile:
          linesList = list(resultFile)
        return linesList
 #NvSim   
    def extractParametersNVSIM(self,parameters,linesList,regex,fileName):
       parameterValues={}
       is_data_array = False
       is_tag_array = False
       is_read_latency = False
       is_write_latency = False
       
       for line in linesList:
           line = re.sub("\|*\-+","",line)
           keyValueSplit = line.split("=")
           print(keyValueSplit)
           parameter = keyValueSplit[0].strip()
           if(parameter=="CACHE DATA ARRAY"):
               is_data_array=True
               is_tag_array=False
           if(parameter=="CACHE TAG ARRAY"):
               is_tag_array=True
               is_data_array=False
           if(parameter=="Read Latency"):
               is_read_latency=True
               is_write_latency=False
           if(parameter=="Write Latency"):
               is_write_latency=True
               is_read_latency=False
              
           print("parameter",parameter)
          
           if(parameter in parameters):
                  
                value =re.findall("\d+\.\d+", str(keyValueSplit[-1]))[0]
                if((parameter not in parameterValues)):

                     if(is_data_array):
                         if(is_read_latency):
                             parameterValues[parameter+'_DA_Rd_lat']= value
                         if(is_write_latency):
                             parameterValues[parameter+'_DA_Wrt_lat']= value
                     elif(is_tag_array):
                         if(is_read_latency):
                             parameterValues[parameter+'_TA_Rd_lat']= value
                         if(is_write_latency):
                             parameterValues[parameter+'_TA_Wrt_lat']= value
                     else:
                        parameterValues[parameter]= value 
                    
                   
            
       parameterValues["filename"] =fileName
        
       return parameterValues
    def extractParametersDsent(self,parameters,linesList,regex,fileName):
                   parameterValues={}
                     
                   for line in linesList:
                       keyValueSplit = line.split(":")
                       parameter = keyValueSplit[0].strip()
                      
                       if(parameter in parameters):
                            print("Paramter",parameter)
                            value = keyValueSplit[1]
                            if((parameter not in parameterValues)):
                                 parameterValues[parameter] = float(value)
                            else:
                                 print(value)
                                 print("Coverted value",float(value))
                            
                   for parameter in parameters:
                       
                       if(parameterValues.get(parameter)==None):
                           parameterValues[parameter] = "NA"
                        
                   parameterValues["filename"] =fileName
                    
                   print(parameterValues)
                   return parameterValues
             
    def extractParametersNoxim(self,parameters,linesList,regex,fileName):
                   parameterValues={}
         
                   
                   for line in linesList:
                       keyValueSplit = line.split(":")
                       parameter = keyValueSplit[0].replace("%","").strip()
                       print(parameter)
                      
                       if(parameter in parameters):
                            print("Paramter",parameter)
                            value = keyValueSplit[1]
        
                            if((parameter not in parameterValues)):
         
                                 parameterValues[parameter] = float(value)
                            else:
                                 print(value)
                                 print("Coverted value",float(value))
                            
        
                                 parameterValues[parameter] += float(value)
                   for parameter in parameters:
                       
                       if(parameterValues.get(parameter)==None):
                           parameterValues[parameter] = "NA"
                        
                   parameterValues["filename"] =fileName
                   parameterValues["pir"] = re.search("\d.\d+",fileName).group(0)
                   
                  
                    
                   print(parameterValues)
                   return parameterValues
               
       #  NVMain
    def extractParametersNVMain(self,parameters,linesList,regex,fileName):
               parameterValues={}
               
               for line in linesList:
                   keyValueSplit = line.split(" ")
                   parameter = keyValueSplit[0].split(".")[-1].strip()
                   if(parameter in parameters):
                        value = keyValueSplit[-1].replace("\n","").replace("W","")
                        if((parameter not in parameterValues)):
                             parameterValues[parameter] = float(value)
                        else:
                             print(value)
                             print("Coverted value",float(value))
                        
                        parameterValues[parameter] += float(value)
               for parameter in parameters:
                   
                   if(parameterValues.get(parameter)==None):
                       parameterValues[parameter] = "NA"
                    
               parameterValues["filename"] =fileName
                
               print(parameterValues)
               return parameterValues
    #   Cacti
    def extractParametersCacti(self,parameters,linesList,regex):
       parameterValues={}
       for line in linesList:
           lineWithActualParameter = line.split(".")[-1]
          
           splitedLine = re.compile(regex).split(lineWithActualParameter)
           parameter = splitedLine[0].strip()
           
           if(parameter in parameters):
                value = re.search("\d*\.?\d+([eE][-+]?\d+)?",line).group(0)
                if(parameter not in parameterValues):
                    parameterValues[parameter]= value
                else:
                    if(parameter!='Associativity'):
                      parameterValues[parameter+'_tagarray'] = value
       energyDelayProduct = float(parameterValues['Access time (ns)'])*float(parameterValues['Total dynamic read energy per access (nJ)'])                     
       print(parameterValues["Area efficiency (Memory cell area/Total area)"])
       perAreaEffieciency = float(energyDelayProduct)/float(parameterValues["Area efficiency (Memory cell area/Total area)"])
       parameterValues['energyDelayProduct']=energyDelayProduct
       parameterValues['perAreaEffieciency']=perAreaEffieciency
      
       print(len(parameterValues.keys()))
       return parameterValues
    @staticmethod
    def createResultCsv(parameterValuesList,csvResultFileName):
            headers = parameterValuesList[0].keys()
            print(len(headers))
            with open(csvResultFileName,'w') as csvResult:
                parameterWriter= csv.DictWriter(csvResult,headers)
                parameterWriter.writeheader()
                print(parameterValuesList)
                parameterWriter.writerows(parameterValuesList)
                print("Sucessfully created csv")
    @staticmethod   
    def plotResultCsvAsBar(xCordinateName,yCortinateName,csvPath):
        data = pd.read_csv(csvPath)
        data.set_index(xCordinateName)[yCortinateName].plot.bar()
        plt.ylabel("Energy Delay Product")
        plt.xlabel("Associativity")
        plt.show()
    #        data.head()
        #        sns.set()
        #        sns.countplot(x="Block size (bytes)",y="energyDelayProduct",data=data)
        #
        
        
            
            
                
                


processConfigFilePath ="hw4/se2/se2process.txt"
parameters=[]
resultFileNames=[]
resultFilePath=""
parameterValuesList=[]
outputCsvFilePath=""
outputCsvFileName=""

readConfig= ReadInputConfig()
processConfigData =readConfig.getInputConfig(processConfigFilePath) 
parameters = processConfigData['parameters']

resultFilePath = processConfigData['resultfilepath']
outputCsvFilePath = processConfigData['outputcsvpath']
outputCsvFileName = processConfigData['outputcsvname']

resultFileNames = [f for f in listdir(resultFilePath) if isfile(join(resultFilePath, f))]


for file in resultFileNames:
     procResult = processResult()
     print(file)
     resultLines = procResult.resultLinesList(resultFilePath+file)
     parameterValuesList.append(procResult.extractParametersNoxim(parameters,resultLines,"\-|\:\s+\d+",file))
     
     
processResult().createResultCsv(parameterValuesList,outputCsvFilePath+outputCsvFileName) 
#processResult().plotResultCsvAsBar("Associativity","energyDelayProduct",outputCsvFilePath+outputCsvFileName)  
#     
     
     
     