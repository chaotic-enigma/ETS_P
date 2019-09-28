import pandas as pd

def GrabMagnitudes(past_occurrence):

	'''
	Parameters : `past_occurrence`
	Return : `list`
	'''

	qdf = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/' + str(past_occurrence) + '.csv')
	mags = qdf['mag'].to_list()
	max_mag = max(mags)
	mag_range = list(range(1, (int(max_mag) + 1)))
	return mag_range

def GrabSpecificArea(past_occurrence, mag_value):
	qdf = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/' + str(past_occurrence) + '.csv')
	qdf = qdf[qdf['mag'] > int(mag_value)]
	places = qdf['place'].to_list()

	specific_areas = []
	for place in places:
		area = place.split(', ')
		if len(area) == 2:
			specific_areas.append(area[1])
		if len(area) < 2:
			specific_areas.append(area[0])
	specific_areas = list(set(specific_areas))
	return specific_areas
