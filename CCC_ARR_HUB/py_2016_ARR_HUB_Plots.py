"""
                    PYTHON 3.xx



py_2016_ARR_HUB_Plots.py

This will take a HUB File and then Search for the Associated Zone pattern Files
There are routines to Plot the Rain Pattern Singularly, ALL in Duration (30)
Plot of the Accumulation for the 10 Patterns applied for a Duration Frequency Combo

Plot the IFD of Pattern ???

There are 720 Lines of DATA which are for 10 Patterns for each of [Frequent, Intermediate , Rare] Frequencies
As in:
Frq_EYear =  [12.000,6.0000,4.0000,3.0000,2.0000,1.0000,0.6900,0.5000,0.2200,0.2000,0.1100,0.0500,0.0200,0.0100,0.0050,0.0020,0.0010,0.0005,0.0002]
Frq_AEPpct = [99.999,99.752,98.168,95.021,86.466,63.212,50.000,39.347,20.000,18.127,10.000,5.0000,2.0000,1.0000,0.5000,0.2000,0.1000,0.0500,0.0200]
Frq_AEP_1x = [1.0001,1.0020,1.0200,1.0500,1.1600,1.5800,2.0000,2.5400,5.0000,5.5200,10.000,20.000,50.000,100.00,200.00,500.00,1000.0,2000.0,5000.0]
Frq_ARI    = [0.0830,0.1700,0.2500,0.3300,0.5000,1.0000,1.4400,2.0000,4.4800,5.0000,9.4900,20.000,50.000,100.00,200.00,500.00,1000.0,2000.0,5000.0]
Frq_Cat    = ['freq','freq','freq','freq','freq','freq','freq','freq','freq','freq','intt','intt','intt','rare','rare','rare','rare','rare','rare']

And 24 Durations:
Durations = [10,15,20,25,30,45,60,90,120,180,270,360,540,720,1080,1440,1800,2160,2880,4320,5760,7200,8640,10080]

Hence 3x10x24 = 720

for POINT & Areal Temporal Patterns
Input Data Information
[INPUTDATA]
Latitude,-33.035717
Longitude,151.265069
[END_INPUTDATA]

River Region
[RIVREG]
Division,South East Coast (NSW)
River Number,10
River Name,Hunter River
[RIVREG_META]
Time Accessed,17 September 2019 02:43PM
Version,2016_v1
[END_RIVREG]

ARF Parameters
[LONGARF]
Zone,SE Coast
a,0.06
b,0.361
c,0.0
d,0.317
e,8.11e-05
f,0.651
g,0.0
h,0.0
i,0.0
[LONGARF_META]
Time Accessed,17 September 2019 02:43PM
Version,2016_v1
[END_LONGARF]

Storm Losses
[LOSSES]
ID,14379.0
Storm Initial Losses (mm),57.0
Storm Continuing Losses (mm/h),4.1
[LOSSES_META]
Time Accessed,17 September 2019 02:43PM
Version,2016_v1
[END_LOSSES]

Temporal Patterns
[TP]
code,ECsouth
Label,East Coast South
[TP_META]
Time Accessed,17 September 2019 02:43PM
Version,2016_v2
[END_TP]

Areal Temporal Patterns
[ATP]
code,ECsouth
arealabel,East Coast South
[ATP_META]
Time Accessed,17 September 2019 02:43PM
Version,2016_v2
[END_ATP]

etc, etc......

"""
import zipfile
import glob
import os
debug = 1
#-----------------------------------------------------------------------
def plot_ARR2016_FRQ_Patterns(PatternType,Dur_Incs,Tstep,Tstps,Zone,Ev_dur):
    """
    Create Plot of Multiple Patterns on Single Screen
    
    Such as all 10 Patterns
    
    
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    #-------------------------- PLOTS ----------------------------------
    fig = plt.figure(figsize=(12, 8))
    Ev_dep = 100.0   #---------------------- REPLACE THS WITH IFD TOTAL RAIN FROM IFD DATA
    # iterate over the function list and add a subplot for each function
    if len(Dur_Incs) == 30:
        v = 6
        h = 5
    else:
        v = 2
        h = 5
    for i, d in enumerate(Dur_Incs, start=1):  
        ax = fig.add_subplot(v, 5, i) # plot with 2 rows and 2 columns
        Rplot = []
        Tplot = []
        tcount = 0
        print (i,d)
        print(i,Tstps)
        Ev_ID = d[0]
        Frq = d[4]
        for t in range(Tstps):
            #print(d[5+tcount])
            R = float(d[5+tcount])*Ev_dep/-100.0
            Rplot.append(R)
            tcount +=1
            T = Tstep*tcount
            Tplot.append(T)
        #---------------------------------------------------------------
        inv_Rplot = np.array(Rplot)*-1.0
        cum_pmp = np.cumsum(inv_Rplot) 
        #print(Tplot,Rplot)
        ax.set_title(Ev_ID+':'+Frq,fontsize = 10)
        ax.bar(Tplot, Rplot, Tstep,edgecolor='blue', color='None') # Plot Rainfall Bar Chart  
        ax2 = ax.twinx()     
        ax2.plot(Tplot, cum_pmp, color="red") #,label = 'Accum. All') # Add Cumulative Rain Line Plot
        ax2.yaxis.label.set_color('red')
        ax2.set_ylabel('Tot Rain pct',fontsize = 8)
        ax2.tick_params(axis='y', colors='red')
        ax.set_xlabel('Time Steps (min)',fontsize = 8)
        #max_pre = int(max(inv_Rplot))
        #y_ticks = np.linspace(0, max_pre, max_pre+1)
        #y_ticklabels = [str(i) for i in y_ticks]
        #ax.set_yticks(-1 * y_ticks)
        #ax.set_yticklabels(y_ticklabels)
        ax.tick_params(axis='y', colors='green')
        ax.set_ylabel('Rain pct')
        ax.yaxis.label.set_color('green')
    # add spacing between subplots
    fig.tight_layout()    
    plt.subplots_adjust(top=0.9)
    stitle = '%s, %s  Rain Proportion Patterns for %sminute Duration' %(PatternType,Zone,Ev_dur)
    fig.suptitle(stitle,fontsize = 16,color = 'red')
    plt.show()
    #--------------- PLOT ACCUMULATED RAIN FOR ALL PATTERNS ------------
    return()



#-----------------------------------------------------------------------
def plot_ARR2016_All_Patterns_4Dur(PatternType,STATS_Labels,INCS_Labels,Dur_Astat,Dur_Incs,debug):
    """
    There are 30 Data sets passed here:
     - 10 Frequent Patterns
     - 10 Intermediate Patterns
     - 10 Rare patterns
    These can be plotted as 3 x 10, or 5 x 2 x 3 (5,6)
    
    There is also Value in Plottng just the Patterns associated with the Particular Frequency on its own (10 Patterns)
    
    """

    if debug >0:print('IN ...plot_All_Dur_Patterns.....')
    """
    Ev_ID = bitsAS[0]
    Ev_dur = int(bitsAS[3])
    Ev_dep = float(bitsAS[5])
    Tstep = int(bitsInc[2])
    Tstps = int(Ev_dur/Tstep)
    print('Event ID: %s' %(Ev_ID))
    print('Event Dur: %i min' %(Ev_dur))
    print('TimeStep: %i min' %(Tstep))
    print('TimeSteps: %i' %(Tstps))
    tcount = 0
    Tplot = []
    Rplot = []
    Tplot.append(0.0)
    Rplot.append(0.0)
    """
    #print(Dur_Incs[0])
    Ev_dur = int(Dur_Incs[0][1])
    Tstep = int(Dur_Incs[0][2])
    Tstps = int(Ev_dur/Tstep)
    Zone = Dur_Incs[0][3]
    print('E_Dur: %i, TStep: %i TSteps: %i' %(Ev_dur,Tstep,Tstps))
    start = 1
    end = 30
    #plot_ARR2016_FRQ_Patterns(Dur_Incs,Tstep,Tstps,Zone,Ev_dur)
    St = [0,10,20]
    End = [10,20,30]
    for i ,frq in enumerate(['Frequent','Intermediate','Rare']):
        print(frq)
        plot_ARR2016_FRQ_Patterns(PatternType,Dur_Incs[St[i]:End[i]],Tstep,Tstps,Zone,Ev_dur)
    return()
#-----------------------------------------------------------------------
def plot_single_ARR2016pattern(bitsAS,bitsInc,STATS_Labels,INCS_Labels,debug):
    """
    Plots just one Rainfall Pattern
    
    
    
    """
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.ticker as ticker

    #ax = plt.axes()
    if debug >0:print('IN ...plot_single_ARR2016pattern.....')
    Ev_ID = bitsAS[0]
    Ev_dur = int(bitsAS[3])
    Ev_dep = float(bitsAS[5])
    Ev_Int = bitsInc[4]
    Ev_Zone = bitsInc[3]
    Tstep = int(bitsInc[2])
    Tstps = int(Ev_dur/Tstep)
    print('Event ID: %s' %(Ev_ID))
    print('Event Dur: %i min' %(Ev_dur))
    print('TimeStep: %i min' %(Tstep))
    print('TimeSteps: %i' %(Tstps))
    tcount = 0
    Tplot = []
    Rplot = []
    Tplot.append(0.0)
    Rplot.append(0.0)
    #-------------------------------------------------------------------
    for t in range(Tstps):
        print(float(bitsInc[5+tcount]))
        R = float(bitsInc[5+tcount])*Ev_dep/-100.0
        Rplot.append(R)
        tcount +=1
        T = Tstep*tcount
        Tplot.append(T)
    #------------------- PLOTS -----------------------------------------
    fig, ax = plt.subplots()
    inv_Rplot = np.array(Rplot)*-1.0
    cum_pmp = np.cumsum(inv_Rplot) 
    #Tstep = Pat_Time[1]
        # Create second axes, in order to get the bars from the top you can multiply 
    # by -1
    #inv_pmp = np.array(PMP_ARR_PAT)*-1.0
    ax.bar(Tplot, Rplot, Tstep,edgecolor='blue', color='None',label = 'Rain')
    ax2 = ax.twinx()
    ax2.plot(Tplot, cum_pmp, color="red") #,label = 'Accum. All')
    ax2.yaxis.label.set_color('red')
    ax2.set_ylabel('Total Rain mm')
    ax2.tick_params(axis='y', colors='red')
    ax.set_xlabel('Time Steps (min)')
    
    # Now need to fix the axis labels
    max_pre = int(max(inv_Rplot))
    y_ticks = np.linspace(0, max_pre, max_pre+1)
    y_ticklabels = [str(i) for i in y_ticks]
    ax.set_yticks(-1 * y_ticks)
    ax.set_yticklabels(y_ticklabels)
    ax.tick_params(axis='y', colors='green')
    ax.set_ylabel('Rainfall per Time Step mm')
    ax.yaxis.label.set_color('green')
    
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5)) # set BIG ticks
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(1)) # set small ticks
    headerline = '2016 ARR Rainfall Pattern & Accumulation plot for %s %imin Event' % (Ev_Int,Ev_dur)
    title = 'Event Zone: %s and Event Rain Pattern ID %s' %(Ev_Zone,Ev_ID)
    plt.suptitle(headerline,fontsize=18)
    plt.title(title,fontsize=12)
    plt.grid(True, which="both", c='gray',ls="--")
    plt.legend()
    plt.show()
    if debug >0:print('OUT ...plot_single_ARR2016pattern.....')
    return()
#-----------------------------------------------------------------------   
def decode(l):
    """
    .decode('utf-8').strip('\r\n').split(',')
    """
    if isinstance(l, list):
        return [decode(x) for x in l]
    else:
        return l.decode('utf-8').strip('\r\n').split(',')
#-----------------------------------------------------------------------
def getARR2016_ARF(a,b,c,d,e,f,g,h,i,Area,Dur,AEP):
    """
    Areal Reduction Factor (ARF) 2016 Method
    
    """
    #p3LogAEP = (0.3+log10*AEP)
    #ARF_LongDur = min(1,(1-a*(Area**b-c*log10*Dur)*Dur**-d+e*Area**f*Duration**g*p3LogAEP+h*10**(i*Area*(Dur/1440.0)*p3LogAEP)))
    #ARF_ShortDur= min(1,(1-0.287*(Area**0.265-0.439*log10*(Dur))*Dur**-0.36+ 2.26x10**-3*Area**0.226*Dur**0.125*p3LogAEP
    #                    	+ 0.0141*Area**0.213*10**(-0.021*(Dur-180)**2/1440.0*p3LogAEP)))
    return()
#-----------------------------------------------------------------------
#           MAIN LINE CODE HERE
#-----------------------------------------------------------------------    
# def get_HUB_BASIC_data():
#----------------- Monsoonal North -------------------------------------
Hub_Dir = 'Monsoonal_North'
HubFilename = os.path.join(Hub_Dir,'ARR_HUB_Monsoonal_North.txt')
#---------------- East Coast South -------------------------------------
Hub_Dir = 'East_Coast_South'
HubFilename = os.path.join(Hub_Dir,'CCC_ARRHUB_ECSouth_Download.txt')
#------ Pattern Type Point or Areal if Catchment > 75km2 Areal
Patterns_list = ['Point','Areal']
patterns = 'Areal'


lcount = 0
Hfile = open(HubFilename,'r')
lines = Hfile.readlines()
for line in lines:
    if debug > 1:print(line)
    if line.startswith('[INPUTDATA]'):
        Loc_Lat = lines[lcount+1].split(',')[1].strip() #,-33.035717
        Loc_Lon = lines[lcount+2].split(',')[1].strip() #,151.265069
    elif line.startswith('[RIVREG]'):
        Divis = lines[lcount+1].split(',')[1].strip() #,South East Coast (NSW)
        RivNum = lines[lcount+2].split(',')[1].strip() # ,10
        RivName = lines[lcount+3].split(',')[1].strip() # ,Hunter River
    elif line.startswith('[RIVREG_META]'):
        TimeAccessed = lines[lcount+1].split(',')[1].strip()  #,17 September 2019 02:43PM
        Version      = lines[lcount+2].split(',')[1].strip()  #,2016_v1
    elif line.startswith('[LONGARF]'):
        ARF_a = lines[lcount+2].split(',')[1].strip() 
        ARF_b = lines[lcount+3].split(',')[1].strip() 
        ARF_c = lines[lcount+4].split(',')[1].strip() 
        ARF_d = lines[lcount+5].split(',')[1].strip() 
        ARF_e = lines[lcount+6].split(',')[1].strip() 
        ARF_f = lines[lcount+7].split(',')[1].strip() 
        ARF_g = lines[lcount+8].split(',')[1].strip() 
        ARF_h = lines[lcount+9].split(',')[1].strip() 
        ARF_i = lines[lcount+10].split(',')[1].strip() 
    elif line.startswith('[LOSSES]'):    
        ARR_IL = lines[lcount+2].split(',')[1].strip() 
        ARR_CL = lines[lcount+3].split(',')[1].strip() 
    elif line.startswith('[TP]'):
        Tpat_code = lines[lcount+1].split(',')[1].strip()  #,17 September 2019 02:43PM
        Tpatlabel = lines[lcount+2].split(',')[1].strip() 
    elif line.startswith('[ATP]'):
        ATpat_code = lines[lcount+1].split(',')[1].strip()  #,17 September 2019 02:43PM
        ATpatlabel = lines[lcount+2].split(',')[1].strip() 

    lcount+=1
Hfile.close()
# Other Data to get:
"""
Median Preburst Depths and Ratios        [PREBURST]
10% Preburst Depths                      [PREBURST10]
25% Preburst Depths                      [PREBURST25]
75% Preburst Depths                      [PREBURST75]
90% Preburst Depths                      [PREBURST90]
Interim Climate Change Factors           [CCF]
Probability Neutral Burst Initial Loss   [BURSTIL]
Transformational Pre-burst Rainfall      [PREBURST_TRANS]
"""
if debug > 0:
    print(Loc_Lat,Loc_Lon,Divis,RivNum,RivName)
    print(TimeAccessed,Version)
    print(Tpat_code,Tpatlabel)
    print(ATpat_code,ATpatlabel)
# Go and Try to Open the Temporal Pattern ZIP Files
#The Zip file will be
# and Contains Tpat_code+'_
# ECsouth.zip contains: ECsouth_AllStats.zip & ECsouth_Increments.zip

#-------------------------------------------------------------------
#    SELECT POINT PATTERNS   or    AREAL PATTERNS
#-------------------------------------------------------------------
if patterns == 'Point':
    Tpat_code = Tpat_code
    PatternType = 'Point Rain'
elif patterns == 'Areal':
    Tpat_code = ATpat_code
    PatternType = 'Areal'

#--------------- POINT RAINFALL PATTERNS--------------------
Zip_file = os.path.join(Hub_Dir, Tpat_code+'.zip')
print('TRY OPEN ZIP: %s' %(Zip_file))
#-----------------------------------------------------------------------
try:# Try to open the Zip File and open the 2 zips inside the HUB zip file
    zip = zipfile.ZipFile(Zip_file)
    print('Files found in the zip file:')
    print (zip.namelist())   # available files in the zip container
    files_inzip_list = zip.namelist()
except:
    print('PROBLEM FINDING THE MAIN ZIP FILE.... Is it present ?')
print(Tpat_code+'_AllStats.csv')
findfile = Tpat_code+'_AllStats.csv'
print('Look for: %s' %(findfile))
#-----------------------------------------------------------------------
try:
    if findfile in files_inzip_list:
        AllStat_index = files_inzip_list.index(findfile) # The STATS for the RAINFALL DATA
        fAStat=zip.open(files_inzip_list[AllStat_index],'r')
        linesAStat = fAStat.readlines()
except:
    print('Problem finding AllStats ZIP part...')
findfile = Tpat_code+'_Increments.csv'
print('Look for: %s' %(findfile))
#-----------------------------------------------------------------------
try:
    if findfile in files_inzip_list:
        Incr_index = files_inzip_list.index(findfile)# THIS IS THE RAINFALL INCREMENTS (PATTERN)
        fInc=zip.open(files_inzip_list[Incr_index],'r')
        linesInc = fInc.readlines()
except:
    print('Problem finding Increments ZIP part...')
#-----------------------------------------------------------------------   
STATS_Labels =  linesAStat[0].decode('utf-8').strip('\r\n').split(',')
INCS_Labels =  linesInc[0].decode('utf-8').strip('\r\n').split(',')

# SELECT 1 or more of the 720 patterns 
# Create TABLES ????
print(STATS_Labels)
for l in [1,2,719,720]:
    bitsAS = linesAStat[l].decode('utf-8').strip('\r\n').split(',')
    print(bitsAS)
print(INCS_Labels)
for l in [1,2,719,720]:    
    bitsInc = linesInc[l].decode('utf-8').strip('\r\n').split(',')
    print(bitsInc)
#-------------- CREATE SINGLE PLOTS -------------------------------------------
#Select the Duration, Frequency and Pattern Number (1-10)
for l in [1,2,719,720]:    
    bitsAS = linesAStat[l].decode('utf-8').strip('\r\n').split(',')
    bitsInc = linesInc[l].decode('utf-8').strip('\r\n').split(',')
    print('Bits AS')
    print(bitsAS)
    print('bits INC')
    print(bitsInc)
    plot_single_ARR2016pattern(bitsAS,bitsInc,STATS_Labels,INCS_Labels,debug) # <----------- PLOT the Single Pattern here
#------------------ Create PLOTS of ALL Patterns per Duration ----------
# for each of the 24 Durations; Plot 30 Patterns 10 Freq, 10 Int, and 10 Rare    

Durations = [10,15,20,25,30,45,60,90,120,180,270,360,540,720,1080,1440,1800,2160,2880,4320,5760,7200,8640,10080]
plot_dur_list = [120,1440,7200]
plot_dur_list = [540]
for i, dur in enumerate(Durations):
    print(i,dur,(i*30+1),i*30+31)
    Dur_Astat = linesAStat[i*30+1:i*30+31]   # [i+endcount:30*(i+1)+1+i]
    Dur_Incs = linesInc[i*30+1:i*30+31]
    bitsAS = linesAStat[l].decode('utf-8').strip('\r\n').split(',')
    bitsInc = linesInc[l].decode('utf-8').strip('\r\n').split(',')
    Dur_Astat = decode(Dur_Astat)
    Dur_Incs  = decode(Dur_Incs)
    #print(Dur_Astat,len(Dur_Astat))
    print(len(Dur_Astat))
    print(dur,plot_dur_list)
    #print(Dur_Astat.count('rare'))
    if dur in plot_dur_list:
        plot_ARR2016_All_Patterns_4Dur(PatternType,STATS_Labels,INCS_Labels,Dur_Astat,Dur_Incs,debug)
    input('Check...')
    
print('++++++++++++++++++++++++++++++++++++++++++++++')

"""
ALLStats DATA:(15 Fields)
Event ID,Region,Region (source),Burst Duration (min),Burst Loading,Original Burst Depth (mm),AEP Window,AEP (source) (%),
Burst Start Date,Burst End Date,DB Event Reference No.,DB Pluviograph Reference No.,Offical Gauge,Lat,Long     
INCREMENTS DATA: (61 fields)
EventID, Duration, TimeStep, Region, AEP, Increments,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,          
"""

