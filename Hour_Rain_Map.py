#############################################################################
# Name: Elizabeth Rentschlar                                                #
# Assistantce from:                                                         #
# Purpose: Use Hourly rain totals condensed in Hours.py to create a series  #
#          of maps that show the                                            #
# Created: 12/21/15                                                         #
# Copyright: (c) City of Bryan                                              #
# ArcGIS Version: 10.2.2                                                    #
# Python Version: 2.7                                                       #
#############################################################################
#Import arcpy module
import arcpy
import datetime
import os

# set workspace
arcpy.env.overwriteOutput = True
work_space = 'G:/GIS_PROJECTS/WATER_SERVICES/Rain_Gauges'
map_doc = work_space + '/Rain_Guage_Map.mxd'

hours_xy = work_space + '/Hour_xy.shp'
hour_shp = work_space + '/hour.shp'

# Local Variables
hours = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
dates = []
one_day = datetime.timedelta(days = 1)

# Functions
def assure_path_exists(my_path):
    dir = os.path.dirname(my_path)
    if not os.path.exists(dir):
        os.mkdir(dir)

def get_start_date(raw_user):
    try:
        f_mounth, f_day, f_year = raw_user.split('-')
        fd = datetime.date(int(f_year), int(f_mounth), int(f_day))
        ft = datetime.time(00,0,0)	
        first_date = datetime.datetime.combine(fd, ft)
        #print "Is %s-%s-%s the date you wanted for the first date?" % (f_mounth, f_day, f_year)
        return (first_date)
    except:
        print "You input a bad date, we will use the first data record..."
        d = datetime.date(2014,9,23)
        t = datetime.time(00,0,0)
        first_date = datetime.datetime.combine(d, t)
        return (first_date)

def get_end_date(raw_user):
    try:
        l_mounth, l_day, l_year = raw_user.split('-')
        ld = datetime.date(int(l_year), int(l_mounth), int(l_day))
        lt = datetime.time(00,0,0)
        last_date = datetime.datetime.combine(ld, lt)    
        #print "Is %s-%s-%s the date you wanted for the last date?" % (l_mounth, l_day, l_year)
        return (last_date)	
    except:
        print "Today will do..."
        last_date = datetime.datetime.now()     		
        return (last_date)
	
# Get the user to input the dates to produce the desired maps 
print "Please input the first date in m-d-yyyy."
first_date = get_start_date(raw_input(">   "))
print first_date

print "Please input the last date in m-d-yyyy."
last_date = get_end_date(raw_input(">   "))
print last_date

# while loop fills in the dates list		
i = first_date
while i <= last_date :
    dates.append(i)
    new_date = i + one_day
    i = new_date

#use the dates list and hours to create hourly rain maps
for date in dates:
    for hour in hours:
        # could add to query to only select hours where it rained
        query = "\"Day\" = date'" + str(date) +"' AND \"Hour\" = " + str(hour)
        arcpy.Select_analysis( hours_xy, hour_shp, query)
        result = arcpy.GetCount_management(hour_shp)
        count = int(result.getOutput(0))		
        if count == 0:
            print "There were no records for %s ." % (date)
        else:
            my_mapdoc = arcpy.mapping.MapDocument(map_doc)
            
            for text in arcpy.mapping.ListLayoutElements(my_mapdoc, 
                    "TEXT_ELEMENT"): 
                if text.text == "Text":
                    text.text = "Date: " + str(date.date()) + '\n' 
                        + "Hour: " + str(hour)
                else:
                    pass
            arcpy.RefreshActiveView() 
            arcpy.RefreshTOC()
            c_date = str(date.date())
            map_output = work_space + "/Rain_Maps/Date" + c_date + "/rain_"
                + c_date + "_" + str(hour) + ".gif"
            assure_path_exists(map_output)
        
            print map_output
            arcpy.mapping.ExportToGIF(my_mapdoc, map_output)
            del my_mapdoc
            #print "Created Map for ", date, hour
            #print "selected" , hour, date
        #except:
        #    print "Was unable to create map for", hour, date
        #    print "Make sure the Rain_Maps folder is closed."
        #    break #pass

