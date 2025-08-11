"""
                PYTHON 3.xx
                
                Routines to calculate ARF ARR 2019 & provide Plot 
                
Area = 125 # Sqkm
#Duration is in minutes 
#AEP is a fraction (between 0.5 and 0.0005).(1/2 yr to 1/2000yr)                

"""


Frq_EYear =  [12.000,6.0000,4.0000,3.0000,2.0000,1.0000,0.6900,0.5000,0.2200,0.2000,0.1100,0.0500,0.0200,0.0100,0.0050,0.0020,0.0010,0.0005,0.0002]
Frq_AEPpct = [99.999,99.752,98.168,95.021,86.466,63.212,50.000,39.347,20.000,18.127,10.000,5.0000,2.0000,1.0000,0.5000,0.2000,0.1000,0.0500,0.0200]
Frq_AEP_1x = [1.0001,1.0020,1.0200,1.0500,1.1600,1.5800,2.0000,2.5400,5.0000,5.5200,10.000,20.000,50.000,100.00,200.00,500.00,1000.0,2000.0,5000.0]
Frq_ARI    = [0.0830,0.1700,0.2500,0.3300,0.5000,1.0000,1.4400,2.0000,4.4800,5.0000,9.4900,20.000,50.000,100.00,200.00,500.00,1000.0,2000.0,5000.0]
Frq_Cat    = ['freq','freq','freq','freq','freq','freq','freq','freq','freq','freq','intt','intt','intt','rare','rare','rare','rare','rare','rare']

Dur_list = [10,15,20,25,30,45,60,90,120,180,270,360,540,720,1080,1440,1800,2160,2880,4320,5760,7200,8640,10080]
#-----------------------------------------------------------------------
def get2019ARF(la,lb,lc,ld,le,lf,lg,lh,li,Area,Dur,AEP):
    """
    These equations are meant to Blend the Long Duraton and Short Duration ARF's (But looks troublesome !!)
    This Routine CURRENTLY is NOT USED !!!!
    
    """
    if Area >= 1 and Area <= 10:
        # ARF Eqn for Areas > 1Sqkm < 10 Sqkm
        if Dur >= 1080:
            ARF10 = get2019ARF_Long(la,lb,lc,ld,le,lf,lg,lh,li,10,Dur,AEP)
        elif Dur < 1080:
            ARF10 = get2019ARF_Shrt(10,Dur,AEP)
        ARF = 1-(0.6614*(1-ARF10)*((Area**0.4)-1))
    elif Area > 10 < 30000:
        ARF = get2019ARF_Long(la,lb,lc,ld,le,lf,lg,lh,li,10,Dur,AEP)
    if Dur > 720 and Dur < 1440:
        # Interpolation Eqn for Dur > 12 < 24hrs
        ARF12L = get2019ARF_Long(la,lb,lc,ld,le,lf,lg,lh,li,Area,720,AEP) # get 12 hr ARF for this Area
        ARF12S = get2019ARF_Shrt(Area,720,AEP)
        ARF24 = get2019ARF_Long(la,lb,lc,ld,le,lf,lg,lh,li,Area,1440,AEP)
        ARFL = ARF12L + ARF24 - (ARF12L)*(Dur-720)/720
        ARFS = ARF12S + ARF24 - (ARF12S)*(Dur-720)/720
        print(ARFS,ARFL)
        ARF = ARFS
    #--- End If
    print(Area,Dur,AEP,ARF)
    return(ARF)
#-----------------------------------------------------------------------
def get2019ARF_Shrt(Area,Dur,AEP):
    """
    SHORT Duration Areal Reduction Factor (ARF) 2019 ARR
    Durations < 18 hours (1080 Minutes)
    Takes the ARRHUB Coefficients, Catchment Area Sqkm, Duration (Minutes) and AEP as 1/years
    From ARR2019 Book 2 Chapter 4
    
    """
    from math import log10
    sa=0.287
    sb=0.265
    sc=0.439
    sd=0.360
    se=2.26e-03
    sf=0.226
    sg=0.125
    sh=0.0141
    si=0.213
    p3LogAEP = (0.3+log10(AEP))
    ARF_ShortDur = min(1,(1-sa*(Area**sb-sc*log10(Dur))*Dur**-sd+(se*Area**sf*Dur**sg*p3LogAEP)+(sh*Area**si*10**(-0.021)*(Dur-180)**2/1440.0*p3LogAEP)))
    return(ARF_ShortDur)
#-----------------------------------------------------------------------
def get2019ARF_Long(la,lb,lc,ld,le,lf,lg,lh,li,Area,Dur,AEP):
    """
    LONG Duration Areal Reduction Factor (ARF) 2019 ARR
    Durations > 18 hours (1080 Minutes)
    Takes the ARRHUB Coefficients, Catchment Area Sqkm, Duration (Minutes) and AEP as 1/years
    From ARR2019 Book 2 Chapter 4
    """
    from math import log10
    p3LogAEP = (0.3+log10(AEP))
    ARF_LongDur  = min(1,(1-la*(Area**lb-lc*log10(Dur))*Dur**-ld+(le*Area**lf *Dur**lg *p3LogAEP)+(lh*10**(li*Area*(Dur/1440.0)*p3LogAEP))))
    return(ARF_LongDur)
#-----------------------------------------------------------------------
def get_list_of_ARF2019(la,lb,lc,ld,le,lf,lg,lh,li,AEP):
    """
    AEP here is 1/Yr
    Produces the list to be plotted
    
    
    """
    Area_list = [1,2,5,8,10,100,500,1000,2000,4000,6000,8000,10000]
    Frq_AEP_1x = [1.0001,5.0000,50.000,500.00,2000.0,5000.0]
    Dur_list = [60,120,180,360,720,1080,1440,1800,2160,2880,4320,5760,7200,8640,10080]
    
    AllARF_Long_List = []
    AllARF_Shrt_List = []
    for Dur in Dur_list:
        ARF_Long_List = []
        ARF_Shrt_List = []
    
        AEP = 1.0/10
        for Area in Area_list:
            # For Long Durations 24 - 168 hours
            ARF_LongDur  = get2019ARF_Long(la,lb,lc,ld,le,lf,lg,lh,li,Area,Dur,AEP)
            #ARF_LongDur  = get2019ARF(la,lb,lc,ld,le,lf,lg,lh,li,Area,Dur,AEP)
            # For Short Durations 1 - 18 hours
            if Dur < 720:
                ARF_ShortDur = get2019ARF_Shrt(Area,Dur,AEP)
            else:
                ARF_ShortDur = 1.0
            ARF_Long_List.append(ARF_LongDur)
            ARF_Shrt_List.append(ARF_ShortDur)
        AllARF_Long_List.append(ARF_Long_List)
        AllARF_Shrt_List.append(ARF_Shrt_List)
    print('+'*80)    
    print(AllARF_Long_List)
    return(AllARF_Long_List,Area_list, Dur_list)
#-----------------------------------------------------------------------
def plot_ARF2019_Dur_Area(la,lb,lc,ld,le,lf,lg,lh,li,AEP):
    """
    Plots the Entire Set of ARF for Durations & Area Range 1 - 10000Sqkm
    
    """
    import matplotlib.pyplot as plt
    
    # Get the Lists of ARF for Durations
    AllARF_Long_List,Area_list, Dur_list =  get_list_of_ARF2019(la,lb,lc,ld,le,lf,lg,lh,li,AEP)
    #------ PLOT LONG ARF -----------------------
    Col_list = ['b','g','r','y','c','m','k','tan','teal','pink','gold','aqua','navy','lime','plum']
    #for i,larf in enumerate(AllARF_Shrt_List):
    #for i,larf in enumerate(AllARF_Shrt_List):    
        #for i,d in enumerate(Dur_list):
    #    plt.plot(Area_list,larf,color=Col_list[i],linestyle = '--',label = str(Dur_list[i])+'Shrt')
    for i,larf in enumerate(AllARF_Long_List):    
        #for i,d in enumerate(Dur_list):
        plt.plot(Area_list,larf,color=Col_list[i],label = Dur_list[i])    
    headerline = 'ARR %s: Areal Reduction Factors (ARF) plot for %s' % (2019,'Durations in (Mins)')
    title = 'For AEP as a fraction: %.4f (or %.1f Yrs);' %(1/AEP,AEP)
    plt.suptitle(headerline,fontsize=18)
    plt.title(title,fontsize=12)
    plt.xscale('log')
    plt.xlabel('Catchment Area Sqkm')
    plt.ylabel('ARF (ARR-2019)')
    plt.grid(True, which="both", c='gray',ls="--")
    plt.legend()
    plt.show()
    return()
#-----------------------------------------------------------------------
#    MAIN LINE CODE
#-----------------------------------------------------------------------
# ----- TESTING ROUTINES ----------------
la=0.06
lb=0.361
lc=0.0
ld=0.317
le=8.11e-05
lf=0.651
lg=0.0
lh=0.0
li=0.0
# -------------- THE ABOVE DATA USUALLY FROM ARR HUB DATA
AEP = 100 # Yrs gets Inverted in Routine ???
plot_ARF2019_Dur_Area(la,lb,lc,ld,le,lf,lg,lh,li,AEP)
Area = 100 # Sqkm
EstDur = 0.76*Area**0.38 *60 # Minutes
print('Get ARF for %.1fSqkm catchment, estimated Duration: %.1f Minutes' %(Area,EstDur))
Dur = 60
ARF = get2019ARF_Long(la,lb,lc,ld,le,lf,lg,lh,li,Area,Dur,AEP)
print('ARF = %.4f for User Selected Dur: %.1f Minutes AEP %i Yrs' %(ARF,Dur,AEP))
if Dur <= 540:
    ARFS = get2019ARF_Shrt(Area,Dur,AEP)
    print('Short ARF: %.4f for User Selected Dur: %.1f Minutes AEP %i Yrs' %(ARF,Dur,AEP))
