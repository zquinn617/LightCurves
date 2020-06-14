# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 12:02:25 2020

@author: Zach
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 
import sys

###############################################################################
#########################Preliminary variables#################################
#########################CHECK BEFORE RUNNING##################################
###############################################################################


#Where are Your files saved?
os.chdir(r'C:\Users\Zach\Desktop\Judits Lab\2003SS84')

#Dependends on how multi aperture photometry is done
Aperture = 5
Middle = 9
Outer = 14
Nsky = 2*np.pi*(Outer**2 - Middle**2)
Area = 2*np.pi*(Aperture**2)

#Magnitude offset
Zmag = 23

#Number of objects used for multiaperture photometry
Objects = 30

#What are the file names you would like to look at?
Backgroundstarfilename = str('2003_0928 Background Data.xlsx')
Targetfilename = str('2003_0928 Object Data.xlsx')

#What do you want the output file to be named?
Outputfilename = str('3003_0928 Proccessed Object')

#######################OPTIONAL GRAPHS#########################################
################CHANGE TO TRUE TO SEE GRAPHS###################################

#Plots all background stars
plotBackgroundStars = False #Change to true if you want to see graph

#plots the Avg of all background stars per frame and over all frames
plotAvgAllStars = False #Change to true if you want to see graph

#Graphs out Corrected values for Yuliya
plotCorrectedTarget = False #Change to true if you want to see graph



###############################################################################
###############################################################################
###############################################################################

#Converts Pixel count to Magnitude
def Count2Magnitude(x,Exp):
    return Zmag + (-2.5 * np.log10(x)) + (2.5 * np.log10(Exp))

#Calculates Error for Yuliya
def Error(SourceSky,SourceError):
    return round(1.087/SourceSky * np.sqrt(SourceSky + Area*SourceError**2 +(Area**2*SourceError**2/Nsky)),3)


###############################################################################
######################DATA FROM BACKGROUND STARS###############################
###############################################################################
 
DT = pd.read_excel (Backgroundstarfilename) #for an earlier version of Excel, you may need to use the file extension of 'xls'

time = DT['JD_UTC']
JDdate = np.floor(time[0]) + 0.5
Hours = time.sub(JDdate).multiply(24).round(5)

Source = list(map(Count2Magnitude,DT['Source-Sky_T1'],DT['EXPTIME']))##Converts photon count to magnitude
SourceError = list(map(Error,DT['Source-Sky_T1'],DT['Source_Error_T1']))##Calculates error

Data = pd.DataFrame(Source, columns =['Source 1'])
Err = pd.DataFrame(SourceError, columns =['Source Error 1'])

for i in range(1,Objects):
    i = str(i + 1)
    Data['Source '+ i] = list(map(Count2Magnitude,DT['Source-Sky_C' + i],DT['EXPTIME']))
    Err['Source Error '+ i] = list(map(Error,DT['Source-Sky_C'+i],DT['Source_Error_C'+i]))

###############################################################################
##########################DATA FROM TARGET#####################################
###############################################################################
Object = pd.read_excel (Targetfilename)

Targettime = Object['JD_UTC']

#check both data tables are for the same frames
if Targettime.equals(time) == False:
    sys.exit("Background star JD times are not equal to Yuliya JD times. Check both datatables include the same frames.")
    
Astrodata = Targettime.to_frame()
Astrodata['Julian Time (Hours)'] = Hours
Astrodata['Target'] = list(map(Count2Magnitude,Object['Source-Sky'],Object['EXPTIME']))
Astrodata['Target Error'] = list(map(Error,Object['Source-Sky'],Object['Source_Error']))
Astrodata['SNR'] = Object['Source_SNR'].round(1)

    
##############################################################################
##########################OPTIONAL GRAPH######################################
##############################################################################


if plotBackgroundStars == True:
    
    plt.figure(figsize= [10,8])
    plt.errorbar(time,Data['Source 1'],yerr = Err['Source Error 1'],label = 'T1', fmt = '',capsize = 5)
    for i in range(1,Objects):
        plt.errorbar(time,Data['Source ' + str(i+1)],yerr = Err['Source Error ' + str(i+1)], label = 'C' + str(i+1))
    plt.legend(loc="best")

    plt.title('All background stars vs time')
    plt.xlabel('Time UTC')
    plt.ylabel('Magnitude')
    

##############################################################################
########################AVERAGING OVER FRAMES##################################
############################################################################## 
    
#finding average source of all background stars for each frame
AVG = Data.mean(axis = 1) 

#finding average over all frames
AVGallframes = AVG.mean(axis = 0)

Astrodata['Avg of all Background stars'] = AVG
Astrodata['Avg all frames'] = AVGallframes

##############################################################################
###############################OPTIONAL GRAPH#################################
###############################################################################

if plotAvgAllStars == True:
    
    plt.figure(figsize = [10,8])
    plt.scatter(time,AVG)
    plt.hlines(AVGallframes,time[0],time.tail(1))

    plt.title('Average of all background stars vs. time (with average over all frames)')
    plt.xlabel('Time UTC')
    plt.ylabel('Magnitude')

###############################################################################
##################Correct for change in background#############################
###############################################################################
  
Astrodata = Astrodata.sub([0,0,AVG.sub(float(AVGallframes)),0,0,0,0],axis = 'columns')
Astrodata['File Name'] = Object['Label']
Astrodata = Astrodata[['File Name','JD_UTC','Julian Time (Hours)', 'Target', 'Target Error', 'SNR', 'Avg of all Background stars', 'Avg all frames']]

###############################################################################
############################OPTIONAL GRAPH#####################################
###############################################################################

if plotCorrectedTarget == True:
    
    plt.figure(figsize = [10,8])

    plt.errorbar(time.values,Astrodata.values, yerr=Astrodata['Target Error'], fmt = '',capsize = 5)
    plt.title('Target vs. time')
    plt.xlabel('Time UTC')
    plt.ylabel('Magnitude')

###############################################################################
###########################SAVES DATA TO CSV###################################
###############################################################################

Astrodata.to_csv(Outputfilename)