#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 18:07:51 2019

@author: sairam
"""
import numpy as np
from os.path import isfile, join
from os import listdir
import matplotlib.pyplot as plt
import pandas as pd

def getLinesList(filePath):
        linesList =[]
        with open(filePath,'r') as resultFile:
          linesList = list(resultFile)
        return linesList
def extractParametersNoxim(parameters,linesList):
       parameterValues={}
       for line in linesList:
           value = line.split(":")[-1]
           parameter = line.split(":")[0].replace("%","").strip()
           if(parameter in parameters):
#                 print("Value :",value)
#                 print("parameter :",parameter)
#       
#                value = re.search("\d*\.?\d+([eE][-+]?\d+)?",line).group(0)
                 parameterValues[parameter]= float(value.replace("\n",""))
       
       return parameterValues;

#def plotResultBarChart(modelresult,basebenchmarkresults,newbenchmarkresults,parameters):
def createExcel(modelresult,filename):
    with pd.ExcelWriter(filename+'.xlsx') as writer:
        for benchmark in  modelresult.keys():   
         df = pd.DataFrame.from_dict(modelresult[benchmark],orient='index')
         df.to_excel(writer,sheet_name=benchmark)
   
def plotResultBarChart(modelresult,parameters):
     
    normaliseresults=True
    if(not normaliseresults):
        ylabelvalues={}
        ylabelvalues['Total received packets']="Packets"
        ylabelvalues['Global average delay (cycles)']="cycles"
        ylabelvalues['Throughput (flits/cycle/IP)']="flits/cycle/IP"
        ylabelvalues['Energy per bit (J/bit)']="\u03BCJ"
        ylabelvalues['Average power dissipation (W)']="W"
        ylabelvalues['Max delay (cycles)']="Cycles"
       
    else:
        ylabelvalues={}
        ylabelvalues['Total received packets']="NORMALIZED TOTAL PACKETS RECIEVED"
        ylabelvalues['Global average delay (cycles)']="NORMALIZED AVERAGE LATENCY"
        ylabelvalues['Throughput (flits/cycle/IP)']="NORMALIZED AVERAGE THROUGHPUT"
        ylabelvalues['Energy per bit (J/bit)']="NORMALIZED AVERAGE ENERGY PER BIT"
        ylabelvalues['Average power dissipation (W)']="NORMALIZED AVERAGE POWER DISSIPATION"
        ylabelvalues['Max delay (cycles)']="NORMALIZED AVERAGE MAX DELAY"
       
    modelcolors={"CLOS-SOI":"#2ECC71"
                 ,"CLOS-SOS-I":"#3754F8"
                 ,"CLOS-SOS-II":"#E74C3C"
                 ,"CLOS-SOS-III":"#F39C12"}
    width=0.2
    
    normalisetomodel='CLOS-SOI'
    parameterunitnormalisefactor={'Global average delay (cycles)':1,'Throughput (flits/cycle/IP)':1,'Energy per bit (J/bit)':10e6}
    simulationtime=10000000
    warmuptime=10000
    cycletime =simulationtime-warmuptime
    nocclock= 0.2*10e-9
   
    fig, (ax1, ax2) = plt.subplots(1, 2)
    for parameter in parameters:
        offset=-0.75
        benchmarklist= list(modelresult['CLOS-SOI'].keys())
        noofbenchmarks= len(benchmarklist)
#        unitnoramlisefactor = 1
#        if(parameter=='Energy per bit (J/bit)'):  
#               unitnoramlisefactor= 10e5
#        print(benchmarklist)
        modellisttoplot={}
        staticvaluestobeadded=0
        staticenergyperbit={"CLOS-SOI":2.53+1.03
                 ,"CLOS-SOS-I":1.36+1.52
                 ,"CLOS-SOS-II":0.92+1.1
                 ,"CLOS-SOS-III":1.613+1.95}  
        for model in modelresult.keys():
            modelresultforparameterlist =[]
            
            totalofeachmodel=0       
            for benchmark in benchmarklist:
                value=0;
                if(parameter=='Energy per bit (J/bit)'):
                    staticvaluestobeadded=(staticenergyperbit[model])/(modelresult[model][benchmark]['Total received packets']*512)
                if(normaliseresults):
                    if(model==normalisetomodel):
                        value=1
                    else:
                        
                        value=(modelresult[model][benchmark][parameter]+staticvaluestobeadded)/(modelresult[normalisetomodel][benchmark][parameter])
                        if(parameter=='Throughput (flits/cycle/IP)'):
                           value=((modelresult[model][benchmark]['Total received packets']*512)/cycletime)/((modelresult[normalisetomodel][benchmark]['Total received packets']*512)/cycletime)
                    totalofeachmodel+=value
                else:
                    value=(modelresult[model][benchmark][parameter]*parameterunitnormalisefactor[parameter]+staticvaluestobeadded)
                    if(parameter=='Throughput (flits/cycle/IP)'):
                           value=(modelresult[model][benchmark]['Total received packets']*512)/cycletime
                    totalofeachmodel+=value
                modelresultforparameterlist.append(value)
            averageofeachmodel= totalofeachmodel/noofbenchmarks
            modelresultforparameterlist.append(averageofeachmodel)
#                print(modelresultforparameterlist)
#            print(modelresultforparameterlist)
#            print("=====================")
            modellisttoplot[model]=modelresultforparameterlist
        benchmarklist.append('Average')   
        x= np.arange(len(benchmarklist))
        fig,ax = plt.subplots()
        num=0
        for model in modellisttoplot:
            ax.bar(x+width*num,modellisttoplot[model],width,label=model,color=modelcolors[model])
            num=num+1
            offset = offset+0.5
        ax.set_ylabel(ylabelvalues[parameter],fontname="Times New Roman Bold",fontweight='bold')
        if(not normalisetomodel):
            ax.set_title(parameter,fontname="Times New Roman Bold",fontsize=15,fontweight='bold',y=1.2)
        ax.set_xticks(x+width+0.09)
        for tick in ax.yaxis.get_major_ticks():
#            tick.label1.set_fontsize(fontsize)
            tick.label1.set_fontweight('bold')
        ax.set_xticklabels(benchmarklist,fontname="Times New Roman",fontweight='bold')
       # ax.legend(loc='lower left', bbox_to_anchor= (-0.06, 1.0), ncol=4, frameon=False,handletextpad=0.1,prop={'weight':'bold'},labelspacing=0.0,columnspacing=0.7)
        #ax.legend(loc='lower left', bbox_to_anchor= (0, 1.0), ncol=4, frameon=False,handletextpad=0.1,prop={'weight':'bold'},labelspacing=0.0,columnspacing=6)
       
        fig.tight_layout()
        plt.xticks(rotation='90')
        plt.show()  
      

    
def comparediffofresults(basebenchmarkresults,newbenchmarkresults,parameters):
    diffofresult={}
    
    for benchmark in basebenchmarkresults.keys():
        diffofbenchmark={}
        basebenchmarkresult = basebenchmarkresults[benchmark]
        newbenchmarkresult = newbenchmarkresults[benchmark]
           
        for parameter in parameters:
            
            diffofbenchmark[parameter] =  newbenchmarkresult[parameter]-basebenchmarkresult[parameter]
        diffofresult[benchmark] = diffofbenchmark
    return diffofresult

newresultsfolder = "/home/sairam/Downloads/dp2results/output/"
baseresultsfolder ="/home/sairam/Desktop/SOS/Clos_Code_SOI/output/"
folderstoanalysis ={"CLOS-SOI":"/home/sairam/Desktop/sosresults/soi/",
                    "CLOS-SOS-I":"/home/sairam/Desktop/sosresults/dp2/"
                    ,"CLOS-SOS-II":"/home/sairam/Desktop/sosresults/dp3new/"
                    ,"CLOS-SOS-III":"/home/sairam/Desktop/sosresults/dp4new/"}
parameters=['Total received packets','Global average delay (cycles)','Throughput (flits/cycle/IP)','Energy per bit (J/bit)']
excelcreationlist ={}
resultsList={}
modelresult ={}

for model in folderstoanalysis.keys():
    modelbenchmarkresultsdict={}
    benckmarkfileinfolder = [f for f in listdir(folderstoanalysis[model]) if f.endswith(".txt") if isfile(join(folderstoanalysis[model], f))]
    for benckmarkfilename in benckmarkfileinfolder:
        benchmarkname = benckmarkfilename.replace("_modified.txt","")
        modelbenchmarkresultsdict[benchmarkname]=extractParametersNoxim(parameters,getLinesList(folderstoanalysis[model]+benckmarkfilename))
    modelresult[model]=modelbenchmarkresultsdict
for benckmarkfilename in benckmarkfileinfolder:
    benchmarkmodelresultdict={}
    benchmarkname = benckmarkfilename.replace("_modified.txt","")
    
    for model in folderstoanalysis.keys():
          benchmarkmodelresultdict[model]=extractParametersNoxim(parameters,getLinesList(folderstoanalysis[model]+benckmarkfilename))
    excelcreationlist[benchmarkname]=benchmarkmodelresultdict


#print(modelresult)

#baseresultfiles = [f for f in listdir(baseresultsfolder) if f.endswith(".txt") if isfile(join(baseresultsfolder, f))]
#newresultfiles =[f for f in listdir(newresultsfolder) if f.endswith(".txt") if isfile(join(newresultsfolder, f))] 
#benchmarkresults={}
#newbenchmarkresults={}
#
#for baseresultfile in baseresultfiles:
#    linesOfFile = getLinesList(baseresultsfolder+baseresultfile)
##    print(linesOfFile)
#    benchmarkname = baseresultfile.replace(".txt","")
#    benchmarkresults[benchmarkname] = extractParametersNoxim(parameters,linesOfFile)
#for newresultfile in newresultfiles:
#    linesOfFile = getLinesList(newresultsfolder+newresultfile)
##    print(linesOfFile)
#    benchmarkname = newresultfile.replace(".txt","")
#    newbenchmarkresults[benchmarkname] = extractParametersNoxim(parameters,linesOfFile)
#
# 
#print(comparediffofresults(benchmarkresults,newbenchmarkresults,parameters))   
#print(newbenchmarkresults)
#print(benchmarkresults)
createExcel(excelcreationlist,"Sos")
plotResultBarChart(modelresult,parameters)


