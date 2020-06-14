# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 15:21:13 2020

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
os.chdir(r'C:\Users\Zach\Desktop\Judits Lab\Yuliya')

#Dependends on how multi aperture photometry is done
Aperture = 9
Middle = 14
Outer = 20
Nsky = 2*np.pi*(Outer**2 - Middle**2)
Area = 2*np.pi*(Aperture**2)

#Magnitude offset
Zmag = 0

#Number of objects used for multiaperture photometry
Objects = 9

#What are the file names you would like to look at?
Patchfilename = str('Common stars.xlsx')
night1filename = str('MultiAperture-CommonStars(0-33).xlsx')
night2filename = str('MultiAperture-CommonStars(36-68).xlsx')
target_night1_filename = str('Corrected Yuliya Data 1-33')
target_night2_filename = str('Corrected Yuliya Data 35-68')

#What do you want the output file to be named?
Outputfilename = str('Patched Yuliya Data')

###############################################################################
###############################################################################

#Converts Pixel count to Magnitude
def Count2Magnitude(x,Exp):
    return Zmag -2.5 * np.log(x) + 2.5*np.log(Exp)

#need to add soure Error to Yuliya
Nsky = 2*np.pi*(Outer**2 - Middle**2)
Area = 2*np.pi*(Aperture**2)
def Error(SourceSky,SourceError):
    return 1.087/SourceSky * np.sqrt(SourceSky + Area*SourceError**2 +(Area**2*SourceError**2/Nsky))

###############################################################################
#########################FOR PATCH AREA########################################
###############################################################################
    
#Imports multiaperture data as a dataframe
DT = pd.read_excel(Patchfilename) #for an earlier version of Excel, you may need to use the file extension of 'xls'

patch_time = DT['JD_UTC']
patch_hours = patch_time.sub(2458277.5).multiply(24).round(5)

Source = list(map(Count2Magnitude,DT['Source-Sky_T1'],DT['EXPTIME']))##Converts photon count to magnitude
SourceError = list(map(Error,DT['Source-Sky_T1'],DT['Source_Error_T1']))##Calculates error

patch_data = pd.DataFrame(Source, columns =['Source 1'])
patch_err = pd.DataFrame(SourceError, columns =['Source Error 1'])

for i in range(1,Objects):
    i = str(i + 1)
    patch_data['Source '+ i] = list(map(Count2Magnitude,DT['Source-Sky_C' + i],DT['EXPTIME']))
    patch_err['Source Error '+ i] = list(map(Error,DT['Source-Sky_C'+i],DT['Source_Error_C'+i]))

#finding average source of all background stars for each frame
patch_avg = patch_data.mean(axis = 1) 

#finding average over all frames
avg_patchframes = patch_avg.mean(axis = 0)


###############################################################################
##########################OPTIONAL GRAPH 1#####################################
###############################################################################

#Plots all background stars
plotgraph = False#Change to true if you want to see graph
if plotgraph == True:
    
    plt.figure(figsize= [10,8])
    plt.errorbar(patch_time,patch_data['Source 1'],yerr = patch_err['Source Error 1'],label = 'T1', fmt = '',capsize = 5)
    for i in range(1,Objects):
        plt.errorbar(patch_time,patch_data['Source ' + str(i+1)],yerr = patch_err['Source Error ' + str(i+1)], label = 'C' + str(i+1))
    plt.legend(loc="best")

    plt.title('All Background Stars Patched Area')
    plt.xlabel('Time UTC')
    plt.ylabel('Magnitude')
    
##############################################################################
########################AVERAGING OVER FRAMES##################################
############################################################################## 

#finding average source of all background stars for each frame
patch_avg = patch_data.mean(axis = 1) 

#finding average over all frames
avg_patchframes = patch_avg.mean(axis = 0)

###############################################################################
############################OPTIONAL GRAPH 2###################################
###############################################################################

#plots the Avg of all stars per frame and over all frames
plotgraph = False#Change to true if you want to see graph
if plotgraph == True:
    
    plt.figure(figsize = [10,8])
    plt.scatter(patch_time,patch_avg)
    plt.hlines(avg_patchframes,patch_time[0],patch_time.tail(1))

    plt.title('Average of all Background Stars w/ Average Over All Frames for Patched Frames')
    plt.xlabel('Time UTC')
    plt.ylabel('Magnitude')



###############################################################################
#########################FOR NIGHT ONE#########################################
###############################################################################
    
#Imports multiaperture data as a dataframe
N1 = pd.read_excel(night1filename) #for an earlier version of Excel, you may need to use the file extension of 'xls'

night1_time = N1['JD_UTC']
night1_hours = night1_time.sub(2458277.5).multiply(24).round(5)


Source = list(map(Count2Magnitude,N1['Source-Sky_T1'],N1['EXPTIME']))##Converts photon count to magnitude
SourceError = list(map(Error,N1['Source-Sky_T1'],N1['Source_Error_T1']))##Calculates error

night1_data = pd.DataFrame(Source, columns =['Source 1'])
night1_err = pd.DataFrame(SourceError, columns =['Source Error 1'])

for i in range(1,Objects):
    i = str(i + 1)
    night1_data['Source '+ i] = list(map(Count2Magnitude,N1['Source-Sky_C' + i],N1['EXPTIME']))
    night1_err['Source Error '+ i] = list(map(Error,N1['Source-Sky_C'+i],N1['Source_Error_C'+i]))



##############################################################################
##########################OPTIONAL GRAPH 3#####################################
##############################################################################

#Plots all background stars
plotgraph = False#Change to true if you want to see graph
if plotgraph == True:
    
    plt.figure(figsize= [10,8])
    plt.errorbar(night1_time,night1_data['Source 1'],yerr = night1_err['Source Error 1'],label = 'T1', fmt = '',capsize = 5)
    for i in range(1,Objects):
        plt.errorbar(night1_time,night1_data['Source ' + str(i+1)],yerr = night1_err['Source Error ' + str(i+1)], label = 'C' + str(i+1))
    plt.legend(loc="best")

    plt.title('All background stars Night 1')
    plt.xlabel('Time UTC')
    plt.ylabel('Magnitude')
    
##############################################################################
########################AVERAGING OVER FRAMES##################################
############################################################################## 

#finding average source of all background stars for each frame
night1_avg = night1_data.mean(axis = 1) 

#finding average over all frames
avg_night1frames = night1_avg.mean(axis = 0)



#PlotsNight 1 and average of Night 1
plotgraph = False#Change to true if you want to see graph
if plotgraph == True:

    plt.figure(figsize = [8,8])
    plt.scatter(night1_time,night1_avg)
    plt.hlines(avg_night1frames,night1_time[0],night1_time.tail(1))

    plt.title('Average of all background stars w/ avg over all frames night 1')
    plt.xlabel('Time UTC')
    plt.ylabel('Magnitude')


###############################################################################
#########################FOR NIGHT TWO#########################################
###############################################################################
    
#Imports multiaperture data as a dataframe
N2 = pd.read_excel(night2filename) #for an earlier version of Excel, you may need to use the file extension of 'xls'

night2_time = N2['JD_UTC']
night2_hours = night2_time.sub(2458277.5).multiply(24).round(5)


Source = list(map(Count2Magnitude,N2['Source-Sky_T1'],N2['EXPTIME']))##Converts photon count to magnitude
SourceError = list(map(Error,N2['Source-Sky_T1'],N2['Source_Error_T1']))##Calculates error

night2_data = pd.DataFrame(Source, columns =['Source 1'])
night2_err = pd.DataFrame(SourceError, columns =['Source Error 1'])

for i in range(1,Objects):
    i = str(i + 1)
    night2_data['Source '+ i] = list(map(Count2Magnitude,N2['Source-Sky_C' + i],N2['EXPTIME']))
    night2_err['Source Error '+ i] = list(map(Error,N2['Source-Sky_C'+i],N2['Source_Error_C'+i]))



##############################################################################
##########################OPTIONAL GRAPH 3#####################################
##############################################################################

#Plots all background stars
plotgraph = False#Change to true if you want to see graph
if plotgraph == True:
    
    plt.figure(figsize= [10,8])
    plt.errorbar(night1_time,night2_data['Source 1'],yerr = night2_err['Source Error 1'],label = 'T1', fmt = '',capsize = 5)
    for i in range(1,Objects):
        plt.errorbar(night1_time,night2_data['Source ' + str(i+1)],yerr = night2_err['Source Error ' + str(i+1)], label = 'C' + str(i+1))
    plt.legend(loc="best")

    plt.title('All background stars Night 1')
    plt.xlabel('Time UTC')
    plt.ylabel('Magnitude')
    
##############################################################################
########################AVERAGING OVER FRAMES##################################
############################################################################## 

#finding average source of all background stars for each frame
night2_avg = night2_data.mean(axis = 1) 

#finding average over all frames
avg_night2frames = night2_avg.mean(axis = 0)



#PlotsNight 1 and average of Night 1
plotgraph = False#Change to true if you want to see graph
if plotgraph == True:

    plt.figure(figsize = [8,8])
    plt.scatter(night2_time,night2_avg)
    plt.hlines(avg_night2frames,night2_time[0],night2_time.tail(1))

    plt.title('Average of all background stars w/ avg over all frames night 1')
    plt.xlabel('Time UTC')
    plt.ylabel('Magnitude')




###############################################################################
#######################Adjust to match Average#################################
###############################################################################

#Correct for change in background
target_night1 = pd.read_csv(target_night1_filename)
target_night2 = pd.read_csv(target_night2_filename)


shifted_target_night1 = target_night1['Target'].sub(avg_night1frames - avg_patchframes)
shifted_target_night2 = target_night2['Target'].sub(avg_night2frames - avg_patchframes)

target_night1['Target'] = shifted_target_night1
target_night2['Target'] = shifted_target_night2


#shows shift in Yuliya data done by patching
plotgraph = False#Change to true if you want to see graph
if plotgraph == True:
    plt.figure(figsize = [8,8])
    plt.plot(target_night1['JD_UTC'],target_night1['Target'].add(avg_night1frames - avg_patchframes), label = 'unshifted')
    plt.plot(target_night1['JD_UTC'],target_night1['Target'], label = 'shifted')
    plt.plot(target_night2['JD_UTC'],target_night2['Target'].add(avg_night2frames - avg_patchframes),label = 'unshifted')
    plt.plot(target_night2['JD_UTC'],target_night2['Target'], label = 'shifted')
#    plt.hlines(avg_patchframes,patch_time[0],patch_time.tail(1), label = 'background during patch')
#    plt.hlines(avg_night1frames,night1_time[0],night1_time.tail(1), label = 'background night one')
#    plt.hlines(avg_night2frames,night2_time[0],night2_time.tail(1), label = 'background night two')
    plt.legend(loc = 'best')
    plt.xlabel('Time (Hours)')
    plt.ylabel('Magnitude')

#Saves data to csv file
frames = [target_night1,target_night2]
patched_target = pd.concat(frames,sort=False)
patched_target = patched_target.reset_index().drop(columns = ['Unnamed: 0','index','Avg of all Background stars','Avg all frames'])
patched_target.to_csv('Patched Yuliya data.txt')