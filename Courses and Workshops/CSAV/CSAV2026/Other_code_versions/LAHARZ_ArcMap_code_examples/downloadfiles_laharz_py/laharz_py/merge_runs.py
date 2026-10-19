# ---------------------------------------------------------------------------
# merge_runs.py
#
# Usage: merge_runs.py is attached to Laharz_py.tbx (toolbox)
#   sys.argv[1] a workspace
#   sys.argv[2] a DEM, input surface raster
#   sys.argv[3] text file storing names of raster runs to merge
#   sys.argv[4] text file storing the volumes
#   sys.argv[5] string of filename prefix
#
#   This program will merge runs of the same volume from separate rasters.
#   The output is a raster containing cells for one volume from all runs at
#   a volcano.
# ---------------------------------------------------------------------------

# Start Up - Import system modules
import sys, string, os, arcpy, time
from arcpy import env
from arcpy.sa import *

starttimetot = time.clock()  # calculate time for program run

# Check out license
arcpy.CheckOutExtension("Spatial")

#===========================================================================
#  Local Functions
#===========================================================================

def OverlayMergeTwo(mylist,dellist, numMaps,z,filePrefix):
    #fname = "temp"+str(z)+str(numMaps)
    fname = filePrefix+str(z)+str(numMaps)

    a = 0
    b = 1
    outCon4 = Con((Raster(mylist[a]) == 1),Raster(mylist[b]),Raster(mylist[a]))
    outCon4.save(fname)
    mylist.reverse()
    mylist.pop()
    mylist.pop()
    mylist.append(fname)
    mylist.reverse()
    if arcpy.Exists(dellist[a]):
        arcpy.Delete_management(dellist[a])
    if arcpy.Exists(dellist[b]):
        arcpy.Delete_management(dellist[b])
    dellist.reverse()
    dellist.pop()
    dellist.pop()
    if len(mylist) > 1:
        dellist.append(fname)
    dellist.reverse()
        
    return dellist, mylist
    
def ConvertTxtToList(atxtfilename,alist):
    # =====================================
    # Parameters:
    #   atxtfilename:  name of a textfile
    #   alist:  empty python list
    #
    # Opens volume or starting coordinate textfile,
    # appends values read from textfile to the list,
    # volume list is sorted smallest to largest
    #
    # Returns:  list
    # =====================================

    afile = open(atxtfilename, 'r')
    
    for aline in afile:
        arcpy.AddMessage( "Current line is: " + aline)
        if aline.find(',') <> -1: # if it does have a ','
            x = aline.rstrip('\n')
            z = x.lstrip(' ')
            y = z.split(',')
            alist = y
            arcpy.AddMessage( "Current list id: " + str(alist))
    afile.close   
    return alist

def main():            
    try:
        #===========================================================================
        # Assign user inputs from menu to appropriate variables
        #===========================================================================

        arcpy.AddMessage("Parsing user inputs:")

        env.workspace = sys.argv[1]     # set the ArcGIS workspace
        Input_raster = sys.argv[2]      # name of filled DEM
        rasterTextFile = sys.argv[3]    # textfile containing names of runs to merge
        volumesTextFile = sys.argv[4]   # textfile of volumes used to create runs
        filePrefix = sys.argv[5]        # string of filename prefix

        #=============================================
        # Set the ArcGIS environment settings
        #=============================================      
        env.scratchWorkspace = env.workspace  # set ArcGIS scratchworkspace
        PathName = env.workspace + "\\"       # directory path
        rasterList = []                       # empty list to store rasters
        volumeList = []                       # empty list to store volumes
           


        # =====================================    
        # Call ConvertTxtToList function with  
        # rasters to merge and with volumns
        # =====================================
        
        arcpy.AddMessage( "________ Convert Textfile to List ________")
        
        rasterList = ConvertTxtToList(rasterTextFile, rasterList)
        numrasters = len(rasterList)
        rasterList.sort()

        volumeList = ConvertTxtToList(volumesTextFile, volumeList)
        numvolumes = len(volumeList)
        volumeList.sort()
        volumeList.reverse()
        arcpy.AddMessage("value of rasterList is: " + str(rasterList))
        arcpy.AddMessage("value of volumeList is: " + str(volumeList))
        # =====================================    
        # Get the lower left cell coordinates
        # and cell size
        # =====================================
        mylist = []
        dellist = []
        for x in range(len(volumeList)):
            z = x + 2
            for y in range(len(rasterList)):
                outCon2 = Con((Raster(rasterList[y]) >= z) & (Raster(rasterList[y]) > 1),z,1)
                outCon2.save("xx"+str(z)+str(y))
                mylist.append("xx"+str(z)+str(y))
            arcpy.AddMessage("  ")
            arcpy.AddMessage("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            arcpy.AddMessage("  ")
            arcpy.AddMessage("TIMES Through:   " + str(x+1))
            arcpy.AddMessage("         MERGING FILES...")

            numMaps = len(mylist)

            dellist.extend(mylist)

            arcpy.AddMessage("  ")
            arcpy.AddMessage("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

            for i in range(len(rasterList) - 1):
                
                dellist,mylist = OverlayMergeTwo(mylist,dellist,numMaps,z,filePrefix)

                numMaps = len(mylist)

            mylist = []
            dellist = []



        endtimetot = time.clock()
        tottime = endtimetot - starttimetot
        
        arcpy.AddMessage("...Processing Complete...")   
        arcpy.AddMessage("TOTAL TIME:  " + str(tottime) + " seconds")
        
        
    except:
        arcpy.GetMessages(2)

if __name__ == "__main__":
    main()   


        