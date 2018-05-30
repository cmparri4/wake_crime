#crime analysis 2

#------------------------imports--------------------------#
import pandas as pandas
import numpy as np
import geocoder
import time

#-----------------------user things-----------------------#
Path_Data = '/Users/EllisA/Desktop/' + 'crime_filt.csv'
Path_To_Save = '/Users/EllisA/Desktop/'

#----------------------functions--------------------------#
def load_data(path):

	return pandas.read_csv(path)

def year_column_addition(df,Year):
	df['year'] = df['Date.of.Arrest'].apply(lambda x: pandas.to_datetime(x).year)
	df['year'] = df['year'].astype(str)
	df.loc[df['year'] == Year]
	return df

def clean_up(df):
	del df['Name']
	del df['Residence']
	del df['Date.of.Arrest']
	return df	

def XY_cor_row(row):

	return geocoder.google(row).latlng

def XY_calculation(df):
	cords = []
	times = []
	for i in range(0,len(df.index)):
	
		selection = df['Arrest.Location'].ix[i]
	
		start_time = time.time()
		cords.append(XY_cor_row(selection))
		elapsed = (time.time() - start_time)
		times.append(elapsed)
		print str(df.index[i]) + ': ' + str(elapsed) + ' ' + 'second(s).'

	print 'total time: ' + str(sum(times)/60.) + ' ' + 'minutes.'
	return cords 

def clean_expand(df):
	df.dropna(subset=['XY'], how='all', inplace = True)
	df[['X','Y']] = pandas.DataFrame(df.XY.values.tolist(), index= df['XY'].index)
	return df	

def analyze_save(path_data,path_save,year_test):
	#load
	df_crime = load_data(path_data)
	#year extraction
	df_crime = year_column_addition(df_crime, year_test)
	#finalize
	df_crime = clean_up(df_crime)
	#run geocoding thrice
	Run_XYCalc = XY_calculation(df_crime)
	#add to data frame
	df_crime['XY'] = pandas.Series(Run_XYCalc)
	#expand output
	df_crime = clean_expand(df_crime)
	#save
	df_crime.to_csv(path_save,index=False)

def years_test():
	years = []
	for i in range(2013,2019):
		years.append(i)
	return years


#-------------------running code--------------------------#
#years to test
Years = years_test()
#cycle through all years of interest
for year in Years:
	print '-----------YEAR' + ' ' + str(year) + '---------'
	save_path = Path_To_Save + str(year) + '_geocoded.csv'
	analyze_save(Path_Data,save_path,year)



