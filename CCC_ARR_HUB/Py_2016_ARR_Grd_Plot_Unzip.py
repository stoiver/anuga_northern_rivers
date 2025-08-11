"""


                                                PYTHON 3.xx
                                                
Py_2016_ARR_Grd_Plot_Unzip.py                         
                                                
- Need a routine to Download the IFD Grid DATA

Then a routine to get IFD data limited to a Catchment Polygon
- Then perform statistics on the data sets for the Catchment Extent

A routine to extract the IFD at a Point from the Zip File
Plot the IFD Curves


Frq_EYear =  [12.000,6.0000,4.0000,3.0000,2.0000,1.0000,0.6900,0.5000,0.2200,0.2000,0.1100,0.0500,0.0200,0.0100,0.0050,0.0020,0.0010,0.0005,0.0002]
Frq_AEPpct = [99.999,99.752,98.168,95.021,86.466,63.212,50.000,39.347,20.000,18.127,10.000,5.0000,2.0000,1.0000,0.5000,0.2000,0.1000,0.0500,0.0200]
Frq_AEP_1x = [1.0001,1.0020,1.0200,1.0500,1.1600,1.5800,2.0000,2.5400,5.0000,5.5200,10.000,20.000,50.000,100.00,200.00,500.00,1000.0,2000.0,5000.0]
Frq_ARI    = [0.0830,0.1700,0.2500,0.3300,0.5000,1.0000,1.4400,2.0000,4.4800,5.0000,9.4900,20.000,50.000,100.00,200.00,500.00,1000.0,2000.0,5000.0]
Frq_Cat    = ['freq','freq','freq','freq','freq','freq','freq','freq','freq','freq','intt','intt','intt','rare','rare','rare','rare','rare','rare']



"""


def world2Pixel_yours(x, y):
    '''
    your values
    ncols         4
    nrows         6
    xllcorner     0.0
    yllcorner     0.0
    cellsize      50.0
    NODATA_value  -9999
    '''
    ulX = 0.0
    ulY = 0.0 + 6 * 50.0
    xDist = 50.0
    yDist = 50.0
    
    pixel_x = int((x - ulX) / xDist)
    pixel_y = int((ulY - y) / yDist)
    return (pixel_x, pixel_y)




#----------------------------------------------------------------------    
    
def read_ASCgrd(IFD_DIR,file_in_zip,settings):
    """
    CALLED BY: IFD_GRD_val_at_Lon_Lat(filename,X0,Y0)
    RETURNS: x,y,z (Grid)
    CALLS:
    
    
    Reads an Ascii GRD file and returns a x array, y array and z array
    Format is 6 header lines with start cell details and the:
    ncols        96
    nrows        115
    xllcorner    150.602500000000    X Lon
    yllcorner    -34.717500000000    Y Lat
    cellsize     0.005000000000
    NODATA_value  -9999
    -9999 -9999 5 2 .... (96 columns of values)
    -9999 20 100 36
    3 8 35 10
    32 42 50 6
    88 75 27 9
    13 5 1 -9999
    .
    .
    .
    (115 Rows)    
    In the ESRI ASCII DEM Format:
    Note that the data is packed from the Topleft in Rows (Y) and Columns (X)
    """
    import zipfile
    if settings.Debug == 'True': print( 'In read_ASCgrd...')
    for Zip_file in glob.glob(os.path.join(IFD_DIR, '*.zip')):
        zip = zipfile.ZipFile(Zip_file)
        # available files in the container
        #print (zip.namelist())  
        files_inzip_list = zip.namelist()
        f=zip.open(file_in_zip)
    with f as infile:
        ncols = int(infile.readline().split()[1]) # Read Line 1 (x Positions)
        nrows = int(infile.readline().split()[1]) # Read Line 2 (y Positions)
        xllcorner = float(infile.readline().split()[1]) # Read Line 3
        yllcorner = float(infile.readline().split()[1]) # Read Line 4
        cellsize = float(infile.readline().split()[1]) # Read Line 5
        nodata_value = float(infile.readline().split()[1]) # Read Line 6
        #version = float(infile.readline().split()[1]) # Read Line 7 Is this there or NOT ?????
        #print ncols,nrows,xllcorner,yllcorner
        x = xllcorner + cellsize * np.arange(ncols) # This is now the X Array
        y = yllcorner + cellsize * np.arange(nrows)
        #x = xllcorner + cellsize * np.arange(nrows) # This is now the X Array
        #y = yllcorner + cellsize * np.arange(ncols)
        z = np.loadtxt(infile) #, skiprows=6) # Read Rest of File into an Array of Z based on x*y elements.... <------- THIS READS the Z into an array !!!
    
    if settings.Debug == 'True':
        #print x,y
        print( x.shape,y.shape)
        #print z
        print (z.shape)
        print (' Why is the SHAPE Opposite of X,Y ???')
    if settings.Debug == 'True': print( 'OUT read_ASCgrd...')
    return(x, y, z,ncols,nrows,xllcorner,yllcorner,cellsize)  # Returns Arrays of the Grid


# -----------------------------------------------------------------------------------------------------------------
def PLOT_ARR2016IFDGRD(x,y,z,x0,y0,z0,Loc_Label,filename,debug):
    """
    CALLED BY: IFD_GRD_val_at_Lon_Lat(filename,X0,Y0,Loc_Label)
    RETURNS: Nothing
    CALLS:   Nothing  
    Plots the 2016 IFD grids with a Location Point and Point value
    - Saves the Figure, could have an option to SHOW it ?
    
    
    """
    import matplotlib.pyplot as plt
    import numpy as np
    import string
    import csv
    from matplotlib.colors import LogNorm
    #-------------------------------------------------------------------
    if debug >0 :print( 'In   PLOT_ARR2016IFDGRD...')
    script_dir = os.path.dirname(__file__)
    GRDPlt_dir = os.path.join(script_dir, 'IFD_Grd_Plt/')
    if not os.path.isdir(GRDPlt_dir):
        os.makedirs(GRDPlt_dir) # Create DIRECTORY to STORE IMAGES
    # PLOT THE GRID ?
    if debug > 2 : print( x0,y0)
    #plt.style.use("dark_background")
    plt.suptitle(Loc_Label.strip()+' Location:%.3f,%.3f' %(x0,y0)+ 'in '+settings.Polygon_File)
    plt.title(os.path.splitext(os.path.basename(filename))[0]+' Grid value: %.3f' %(float(z0)))
    #--------- PLOT THE IFD GRID ---------------------------------------
    plt.imshow(z, extent=(np.amin(x), np.amax(x), np.amin(y), np.amax(y)), norm=LogNorm(), aspect = 'auto',cmap = 'jet')
    plt.colorbar()
    #---------- PLOT THE POINT OF ENQUIRY ------------------------------
    plt.scatter(x0, y0, marker='+',color = 'white', s=10, zorder=10)
    # PLOT A REFERENCE POLYGON
    xp = []
    yp = []
    # Get reference Line From Polygon File
    print(settings.Polygon_File)
    with open(settings.Polygon_File,'r') as f:
        #xp,yp = zip(*float([l.split(',') for l in f ]))
        #xp,yp = zip(*csv.reader(f))
        reader = csv.reader(f)
        for line in reader:
            #print line[:][0],line[:][1]
            xp.append(float(line[:][0]))
            yp.append(float(line[:][1]))
    # s.translate(None, string.punctuation) # To get rid of Punctuation in txt
    #for x in xp: xp = [x.translate(None, string.punctuation)]  # But gets rid of Decimal POINT !!!! ????
    #for y in yp: yp = [y.translate(None, string.punctuation)]
    #for x in xp: xp = [x.strip("'")]  # But gets rid of Decimal POINT !!!! ????
    #for y in yp: yp = [y.strip("'")]
    #import csv
    #    x,y = zip(*csv.reader(f,delimeter=','))

    plt.plot(xp,yp,c = 'white',linestyle = '--',linewidth = 1.5)
    plt.savefig(os.path.splitext(GRDPlt_dir+os.path.basename(filename))[0]+'_Grid.png')
    plt.show()
    plt.close()
    if check: input('Check Plot...')
    """
    import numpy as np
    from matplotlib.colors import LogNorm
    x_list = np.array([-1,2,10,3])
    y_list = np.array([3,-3,4,7])
    z_list = np.array([5,1,2.5,4.5])
    
    N = int(len(z_list)**.5)
    z = z_list.reshape(N, N)
    plt.imshow(z, extent=(np.amin(x_list), np.amax(x_list), np.amin(y_list), np.amax(y_list)), norm=LogNorm(), aspect = 'auto')
    plt.colorbar()
    plt.show()
    """
    # try to Clip the Grd to the Catchment ONLY
    from osgeo import gdal
    ds = 'dataset' # Typically Geotiff
    dsClip = gdal.warp('demClip.tif', ds, cutlineDSName = 'CutPoly', cropToCutline = True,dstNodata = np.nan)
    array = dsClip.getRasterBand(1).ReadAsArray()
    plt.iimshow()
    plt.colorbar()
    
    if settings.Debug == 'True' :print( 'OUT   PLOT_ARR2016IFDGRD...')
    return()

#-----------------------------------------------------------------------   
def decode(l):
    """
    .decode('utf-8').strip('\r\n').split(',')
    This decodes a list that is identified as bytes
    """
    if isinstance(l, list):
        return [decode(x) for x in l]
    else:
        return l.decode('utf-8').strip('\r\n').split(',')

#-----------------------------------------------------------------------
def get_ARR2016_IFD_grd_zip_file_list(IFD_DIR,Lat,Lon,Frq,Dur,debug, check=False):
    """
    Structure of Names in the Grid IFD Rainfall ZIP file is as follows:
    
    catchment_depth_1min_99999aep.txt.asc
    
    Durations can be found by min, and frequency by aep
    ncols         27
    nrows         23
    xllcorner     150.975
    yllcorner     -33.6
    cellsize      0.025
    NODATA_value  -9999
    """

    import zipfile
    import glob
    import os
    if debug> 0: print('IN....get_ARR2016_IFD_grd_zip_file_list....')
    DUR_list = []
    #DUR_list = [1,2,3,4,5,10,15,20,25,30,45,60,90,120,180,270,360,540,720,1080,1440,1800,2160,2880,4320,5760,7200,8640,10080]
    #FREQ_list = [50,100,200,500,1000,2000,5000,10000,18127,20000,39347,50000,63212,86466,95021,98168,99752,99999]
    #ARI_Label = [2k,1k, 500,200,100, 50  ,20  ,10   ,5    ,4.48 ,2,   ,1.44 ,1    ,0.5  ,0.33 ,0.25 ,0.17 ,0.08]
    FREQ_list = []
    OPENZIP = True
    for Zip_file in glob.glob(os.path.join(IFD_DIR, '*IFD*.zip')):# just get the IFD file only
        zip = zipfile.ZipFile(Zip_file)
        # available files in the container
        print (zip.namelist())  
        files_inzip_list = zip.namelist()
        for file_in_zip in files_inzip_list: # 
            if 'epsg' in file_in_zip:
                pass # Not the File we want
            else:
                print (file_in_zip)
                #if 'min' in file_in_zip: 
                #print file_in_zip.split('min')[0].split('_')[2]
                # CHECK DURATION
                Dur_R = file_in_zip.split('min')[0].split('_')[2] 
                print (Dur_R,Dur)
                if not Dur_R.isdigit():
                    if debug > 1:
                        print ('NOT DIGIT....')
                        print (Dur_R,Dur)
                if Dur_R.isdigit()and Dur_R in DUR_list:
                    pass
                else:
                    if Dur_R.isdigit():
                        DUR_list.append(Dur_R)
                # CHECK FREQUENCY
                #   catchment_depth_1min_99999aep.txt.asc
                Frq_R = file_in_zip.split('aep')[0].split('_')[3] 
                print (Frq_R,Frq)
                if not Frq_R.isdigit():
                    if debug > 1:
                        print ('NOT DIGIT....')
                        print (Frq_R,Frq)
                if Frq_R.isdigit()and Frq_R in FREQ_list:
                    pass
                else:
                    if Frq_R.isdigit():
                        FREQ_list.append(Frq_R)
                # Get Specific Frq-Dur File
                if Dur == int(Dur_R) and Frq == int(Frq_R) and OPENZIP:
                    # extract a specific file from zip 
                    f=zip.open(file_in_zip)
                    lines = f.readlines()
                    # format of Grid IFD data
                    """
                    ncols         27
                    nrows         23
                    xllcorner     150.975   # lon
                    yllcorner     -33.6     # lat
                    cellsize      0.025
                    NODATA_value  -9999
                    Note that
                    lon=(0:-1:-(nrows-1)).*cellsize + yllcorner + cellsize/2   ## Check this
                    lat=(0:ncols).*celsize + xllcorner + cellsize/2
                    """
                    # Get cols,rows,xllcorner,yllcorner,cellsiize,NODATA_value
                    for line in lines:
                        line = decode(line)
                        if debug > 2: print (line)
                        line = ' '.join(line[0].split()) # Get Rid of all but one space
                        if line.startswith('ncols'):
                            cols =int(line.split('ncols')[1].strip())
                            if debug > 2:print (cols)
                        if line.startswith('nrows'):
                            rows =int(line.split('nrows')[1].strip())
                            if debug > 2:print (rows)
                        if line.startswith('xllcorner'):
                            xllcorner =float(line.split('xllcorner')[1].strip())
                            if debug > 2:print (xllcorner)
                        if line.startswith('yllcorner'):
                            yllcorner =float(line.split('yllcorner')[1].strip())
                            if debug > 2:print (yllcorner)
                        if line.startswith('cellsize'):
                            cellsize =float(line.split('cellsize')[1].strip())
                            print (cellsize)
                        if line.startswith('NODATA_value'):
                            NODATA_value =line.split('NODATA_value')[1].strip()
                            xurcorner = float(xllcorner) + int(cols)*float(cellsize) # Upper Right Lon
                            yurcorner = float(yllcorner) + int(rows)*float(cellsize)  # Upper Right Lat
                            if debug > 2:
                                print (NODATA_value)
                                print (xurcorner)
                                print (yurcorner)
                    #---------------------------------------------------
                    Tar_col = round(float((Lon - xllcorner) /cellsize))
                    Tar_row = round(float((Lat - yllcorner) /cellsize))
                    print('Target Location: %i,%i' %(Tar_col,Tar_row))
                    Tar_row = int(rows)-Tar_row
                    print('Inverted Tar_row : %i ' %(Tar_row))
                    Ldecode = decode(lines[Tar_row+3])
                    if Ldecode[0].startswith("'"):
                        Ldecode = Ldecode.remove("'")
                    print(Ldecode[0])
                    LLRain = float(Ldecode[0].split(' ')[Tar_col+1]) # Check the Location is correct !!!!!!
                    print('Rain at Target: %.1fmm' %(LLRain))
                    if check: input('Check...')
                    #---------------------------------------------------
            #f = open('extracted.txt', 'wb')
            #f.write(content)
            #f.close()
        if check: input('Check....')
        OPENZIP = False
        if debug > 1:print (len(files_inzip_list))
        #print DUR_list
        DUR_list = [ int(x) for x in DUR_list ]
        DUR_list = sorted(DUR_list)
        for x in DUR_list:
            if debug > 1:print (x)
        FREQ_list = [ int(x) for x in FREQ_list ]
        FREQ_list = sorted(FREQ_list)
        for x in FREQ_list:
            if debug > 1:print (x)
    if debug> 0: print('OUT....get_ARR2016_IFD_grd_zip_file_list....')
    return(cols,rows,xllcorner,yllcorner,cellsize,NODATA_value,lines,LLRain)


#----------------------------------------------------------------------- 
def convert_ASCII_2_GRD(IFDgrd_lines,LLRain,SiteLabel,Lat,Lon,Frq,Dur, cols,rows,lx,ly,cellsize,NODATA_value,IFD_DIR,debug=0):
    """
    PLOT the IFD Grid for a specified FREQ & DUR,
    plot a Reference Polyline (Catchment)
    plot a Reference Location PT and label the Rainfall at that point
    
    
    """

    import numpy as np
    import matplotlib.pyplot as plt
    import cmaps as nclcmaps
    import glob
    import os
    
    IFDgrd_lines = decode(IFDgrd_lines)
    #     [[int(float(j)) for j in i] for i in x]
    IFD_Data = []
    for l in IFDgrd_lines[6:]:
        l[0] = l[0].rstrip(' ')
        #print(l[0])
        #print(len(l[0].split(' ')))
        IFD_Data.append([float(s) for s in l[0].split(' ')])

    IFD_Data = np.asarray(IFD_Data, dtype=float)

    if debug>0: print(IFD_Data)
    
    lons   = lx + np.arange(cols)*cellsize
    lats_r = ly + np.arange(rows)*cellsize
    lats   = lats_r[::-1] # keep in mind to flip up-down latitude.

    return lons,lats,IFD_Data



#----------------------------------------------------------------------- 
def PlotGRD(lons,lats,IFD_Data,LLRain,SiteLabel,Lat,Lon,Frq,Dur, cols,rows,lx,ly,cellsize,NODATA_value,IFD_DIR,debug=0):
    """
    PLOT the IFD Grid for a specified FREQ & DUR,
    plot a Reference Polyline (Catchment)
    plot a Reference Location PT and label the Rainfall at that point
    
    
    """

    import numpy as np
    import matplotlib.pyplot as plt
    import cmaps as nclcmaps
    import glob
    import os

    #-------------- PLOT ---------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 6))

    mask = IFD_Data > 0.0
    vmax = np.max(IFD_Data)
    vmin = np.min(IFD_Data[mask])

    print(vmin,vmax)

    #norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    cs = ax.pcolormesh(lons, lats,IFD_Data, cmap='hsv', vmin=vmin, vmax=vmax)  #  nclcmaps.MPL_plasma_r, 'inferno'
    fig.colorbar(cs)
    #ax.axis('off')

    #---------- PLOT Poly Lines --------------------------------------------
    # File *.ply
    for poly_file in glob.glob(os.path.join(IFD_DIR, '*.ply')):
        xp = []
        yp = []
        print('Plot: '+poly_file)
        with open(poly_file, 'r') as f:
            lines = f.readlines()
            for l in lines:
                xp.append(float(l.split(',')[0]))
                yp.append(float(l.split(',')[1]))
        plt.plot(xp,yp,c = 'white',linestyle = '--',linewidth = 1.5)

    #-------------- PLOT IFD LOCATION --------------------------------------
     #PLOT THE POINT OF ENQUIRY
    plt.scatter(Lon, Lat, marker='+',color = 'white', s=10, zorder=10)

    # ------- Titles --------------
    st_txt = '2016 IFD Grd for %.4fpctEY; %i Mins' %(Frq/1000.0,Dur)
    fig.suptitle(st_txt, fontsize=16,color='red')
    t_txt = '%s Lat: %.4f, Lon: %.4f Rainfall: %.1fmm' %(SiteLabel,Lat,Lon,LLRain)
    _ = ax.set_title(t_txt, fontsize=12,color = 'blue')
    plt.show()
    return

#-----------------------------------------------------------------------     
def get_ARR2016_IFD_at_PT(IFD_DIR,Lat,Lon,debug):
    """
    This will open the grd IFD data zip file and extract the IFD data at a location for 512 Grids
    Which will populate the IFD
    
    """
    if debug> 0: print('IN....get_ARR2016_IFD_at_PT....')
    # ----- GET THE Grd Zip File
    
    
    if debug> 0: print('OUT....get_ARR2016_IFD_at_PT....')
    return() 
    
    


#=======================================================================
#                 MAIN LINE CODE
#======================================================================= 
if __name__ == "__main__":           
    debug = 1
    #D:\Users\RUDY\Documents\00_PYTHON\03_PYTHON\AR&R2016\CCC_ARR_HUB\East_Coast_South
    IFD_DIR = 'East_Coast_South'            
    SiteLabel = 'Test Site Tuggerah Lakes'
    Lat = -33.21990875
    Lon = 151.34782281
    Frq = 1000
    Dur = 540
    Catchment_Area = 100 # In SqKm

    #-----------------------------------------------------------------------

    cols,rows,lx,ly,cellsize,NODATA_value,IFDgrd_lines,LLRain = get_ARR2016_IFD_grd_zip_file_list(IFD_DIR,Lat,Lon,Frq,Dur,debug)

    lons,lats, IFD_Data = convert_ASCII_2_GRD(IFDgrd_lines,LLRain,SiteLabel,Lat,Lon,Frq,Dur,cols,rows,lx,ly,cellsize,NODATA_value,IFD_DIR)
    PlotGRD(lons,lats,IFD_Data,LLRain,SiteLabel,Lat,Lon,Frq,Dur,cols,rows,lx,ly,cellsize,NODATA_value,IFD_DIR)

    #PLOT_ARR2016IFDGRD(x,y,z,Lon,Lat,LLRain,SiteLabel,filename,debug)

    get_ARR2016_IFD_at_PT(IFD_DIR,Lat,Lon,debug)
