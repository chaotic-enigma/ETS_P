import pandas as pd

def GrabOccurrenceData(past_occurrence, mag_value):
	qdf = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/' + str(past_occurrence) + '.csv')
	qdf = qdf[qdf['mag'] > int(mag_value)]
	return qdf

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
	qdf = GrabOccurrenceData(past_occurrence, mag_value)
	places = qdf['place'].to_list()

	specific_areas = []
	for place in places:
		area = place.split(', ')
		if len(area) == 2:
			specific_areas.append(area[1])
		if len(area) < 2:
			specific_areas.append(area[0])

	area_counts = []
	for area in specific_areas:
		area_counts.append(area + ' - ' + str(specific_areas.count(area)))

	specific_areas = list(set(area_counts))
	return specific_areas
