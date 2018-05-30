#crime stuff
#Ellis Ackerman

#-----------------time keeps on slipping------------------#
#time set up
import time
#set up time
start_time = time.time()

#-----------------------user things-----------------------#
Path_Data = '~/Desktop/wake_crime_sub1.csv'
Path_To_Save = '~/Desktop/geocoded_crime1b.csv'

#------------------------imports--------------------------#
import pandas as pandas
import numpy as np
import geocoder
import time

#----------------------functions--------------------------#
def load_data(path):
	print 'data loaded'
	return pandas.read_csv(path)


def year_column_addition(df):
	df['year'] = df['Date.of.Arrest'].apply(lambda x: pandas.to_datetime(x).year)
	df['year'] = df['year'].astype(str)
	df.loc[df['year'] == '2017']
	return df

def clean_up(df):
	del df['Name']
	del df['Residence']
	del df['Date.of.Arrest']
	return df

def XY_cor(df):
	df['XY'] = df['Arrest.Location'].apply(lambda x: geocoder.google(str(x)).latlng)
	df.dropna(subset=['XY'], how='all', inplace = True)
	df[['X','Y']] = pandas.DataFrame(df.XY.values.tolist(), index= df['XY'].index)
	return df

#-------------------running code--------------------------#
#load
df_crime = load_data(Path_Data)
#year extraction
df_crime = year_column_addition(df_crime)
#finalize
df_crime = clean_up(df_crime)
#geocoding
df_crime = XY_cor(df_crime)
#saving output
df_crime.to_csv(Path_To_Save,index=False)
#into the future
print 'processing and geolocating took', time.time() - start_time, 'seconds to run.'
