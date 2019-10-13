import geopandas as gpd
import pandas as pd

def GrabGeojsonData(past_occurrence, mag_value):
	eq_geojson = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/' + str(past_occurrence) + '.geojson'
	eq_geodf = gpd.read_file(eq_geojson)
	eq_geodf = pd.DataFrame(eq_geodf)
	eq_geodf = eq_geodf[eq_geodf['mag'] > int(mag_value)]
	return eq_geodf

def GrabFeltReport(past_occurrence, mag_value, specific_area):
	eq_geodf = GrabGeojsonData(past_occurrence, mag_value)
	f_df = eq_geodf[['title', 'mag', 'felt']].dropna()
	f_df.sort_values(by='felt', ascending=False, inplace=True)

	if specific_area == 'Worldwide':
		f_df = f_df[f_df['felt'] > 5]
		f_locations = f_df['title'].to_list()
		f_reports = f_df['felt'].to_list()
	else:
		f_df = f_df[f_df['title'].str.contains(str(specific_area.split(' - ')[0]))]
		f_locations = f_df['title'].to_list()
		f_reports = f_df['felt'].to_list()
	return f_locations, f_reports

def GrabAlertReport(past_occurrence, mag_value, specific_area):
	eq_geodf = GrabGeojsonData(past_occurrence, mag_value)
	a_df = eq_geodf[['title', 'mag', 'alert']].dropna()
	a_df.sort_values(by='mag', ascending=False, inplace=True)

	if specific_area == 'Worldwide':
		a_locations = a_df['title'].to_list()
		a_reports = a_df['alert'].to_list()
	else:
		a_df = a_df[a_df['title'].str.contains(str(specific_area.split(' - ')[0]))]
		a_locations = a_df['title'].to_list()
		a_reports = a_df['alert'].to_list()
	return a_locations, a_reports

def GrabTsunamiReport(past_occurrence, mag_value, specific_area):
	eq_geodf = GrabGeojsonData(past_occurrence, mag_value)
	t_df = eq_geodf[['title', 'mag', 'tsunami']].dropna()
	t_df.sort_values(by='mag', ascending=False, inplace=True)
	t_df = t_df[t_df['tsunami'] > 0]

	if specific_area == 'Worldwide':
		t_locations = t_df['title'].to_list()
	else:
		t_df = t_df[t_df['title'].str.contains(str(specific_area.split(' - ')[0]))]
		t_locations = t_df['title'].to_list()
	return t_locations
