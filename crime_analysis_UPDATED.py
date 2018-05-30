#crime analysis 2

#------------------------imports--------------------------#
import pandas as pandas
import numpy as np
import geocoder
import time

#-----------------------user things-----------------------#
bottom_index = 0
top_index = 4
Path_Data = '/Users/EllisA/Desktop/Wake_Crime_Analysis/crime_filt.csv'
Path_To_Save = '/Users/EllisA/Desktop/Wake_Crime_Analysis/geocoded_'+ str(bottom_index)+'_'+str(top_index)+'.csv'

#----------------------functions--------------------------#
def load_data(path):

	return pandas.read_csv(path)

def year_column_addition(df):
	df['year'] = df['Date.of.Arrest'].apply(lambda x: pandas.to_datetime(x).year)
	df['year'] = df['year'].astype(str)
	return df

def clean_up(df):
	del df['Name']
	del df['Residence']
	del df['Date.of.Arrest']
	return df	

def XY_cor_row(row):

	return geocoder.google(row).latlng

def XY_calculation(df,min_val,max_val):
	
	#df = df.iloc[min_val:max_val+1]
	cords = []
	times = []
	for i in range(min_val,max_val+1):
	
		selection = df['Arrest.Location'].ix[i]
	
		start_time = time.time()
		cord = XY_cor_row(selection)
		elapsed = (time.time() - start_time)
		cords.append(cord)
		times.append(elapsed)
		print str(df.index[i]) + ': ' + str(elapsed) + ' ' + 'second(s).' + ' Lat/Long -->' + str(cord)
	print 'total geocoding time: '+ str(sum(times)/60.) + 'minutes.'
	return cords

def clean_expand(df):
	df.dropna(subset=['XY'], how='all', inplace = True)
	df[['X','Y']] = pandas.DataFrame(df.XY.values.tolist(), index= df['XY'].index)
	return df	

def prepare_analyze(path_data,min_val,max_val):
	#load
	df = load_data(path_data)
	#year extraction
	df = year_column_addition(df)
	#clea up
	df = clean_up(df)
	#make selection
	df = df.iloc[min_val:max_val+1]
	return df

#-------------------running code--------------------------#
#prepare df
df_crime = prepare_analyze(Path_Data,bottom_index,top_index)
#geocode on index range
XY_calcs = XY_calculation(df_crime,bottom_index,top_index)
#add geocodes to df
df_crime['XY'] = pandas.Series(XY_calcs)
#clean geocoded column
df_crime = clean_expand(df_crime)
#save df
df_crime.to_csv(Path_To_Save,index=False)




































'''
#i just cant delete this because its so sexy, even though
--the new functions i made wouldnt work ont it
#old version if google api didnt make you pay
#-------------------running code--------------------------#
#years to test
Years = years_test()
#cycle through all years of interest
for year in Years:
	print '-----------YEAR' + ' ' + str(year) + '---------'
	save_path = Path_To_Save + str(year) + '_geocoded.csv'
	analyze_save(Path_Data,save_path,year)'''



