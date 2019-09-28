import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import (Input, Output)

import pandas as pd

from TrackingFlow import (GrabMagnitudes, GrabSpecificArea)
from GraphPlotting import (PlotDensityMap, PlotScatterMap, LayoutDensity, LayoutScatter)

external_scripts = ['https://www.google-analytics.com/analytics.js']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

cs_mag = [
	[0, '#a303b9'],	[0.25, '#ea6402'],[0.5, '#fa73a0'],	
	[0.75, '#f03b20'], [1, '#bd0026'],
]
radius_multiplier = {'inner' : 1.5, 'outer' : 3}
colors_useful = {
	'text_color' : '#154360',
	'bar_max_val' : 'rgba(222,45,38,0.8)',
	'bar_normal' : 'rgb(41,128,185)',
	'bar_min_val' : 'rgb(40,180,99)',
	'symmetry' : '#d0ece7',
	'rev_symmetry' : '#fff',
	'danger' : '#fc131a',
	'loc_color' : '#d35400',
	'report_color' : '#8e44ad',
	'tsunami_color' : '#0240da'
}

app = dash.Dash(__name__,
	external_scripts=external_scripts,
	external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
	html.Div([
		html.Div([html.H2('Earthquake Tracking System')],
			style={'textAlign' : 'center'}),
		html.Div([
			html.Div([html.H5('Past Occurence')], className='two columns', style={'textAlign' : 'center'}),
			html.Div([
				dcc.Dropdown(
					id='past-occurrence',
					options=[
						{'label' : 'This Hour', 'value' : 'all_hour'},
						{'label' : 'Yesterday', 'value' : 'all_day'},
						{'label' : 'Last Week', 'value' : 'all_week'},
					],
					value='all_hour'
				),
			], className='two columns', style={'textAlign' : 'center'}),
			html.Div([html.H5('Magnitude (+)')], className='two columns'),
			html.Div([dcc.Dropdown(id='magnitude-range')], 
				className='two columns', style={'textAlign' : 'center'}),
			html.Div([html.H5('Region')], className='one columns'),
			html.Div([dcc.Dropdown(id='area-list')], className='three columns')
		], className='row', 
		style={
			'borderBottom' : 'thin lightgrey solid', 
			'backgroundColor' : colors_useful['symmetry'], 
			'padding': '20px 20px', 'margin-left' : 20, 
			'margin-right' : 20, 'margin-top' : 10
		})
	]),
	html.Div([
		dcc.RadioItems(
			id='map-type',
			options=[{'label' : s, 'value' : s} for s in ['Density Map', 'Scatter Map']],
			value='Density Map',
			labelStyle={'display': 'inline-block'}
		)
	], style={'margin-left' : 20, 'margin-top' : 20, 'margin-bottom' : 20}),
	html.Div([dcc.Interval(id='output-update', interval=180*1000)]),
	html.Div(id='map-quakes')

])

@app.callback(
	Output('magnitude-range', 'options'), 
	[Input('past-occurrence', 'value'), Input('output-update', 'n_intervals')]
)
def update_mag_range(past_occurrence, n_intervals):
	mag_range = GrabMagnitudes(past_occurrence)
	mag_range.reverse()
	return [{'label' : m, 'value' : m} for m in mag_range]

@app.callback(
	Output('area-list', 'options'), 
	[Input('past-occurrence', 'value'), Input('magnitude-range', 'value'), 
		Input('output-update', 'n_intervals')]
)
def update_area_list(past_occurrence, mag_value, n_intervals):
	area_list = GrabSpecificArea(past_occurrence, mag_value)
	area_list.insert(0, 'Worldwide')
	return [{'label' : area, 'value' : area} for area in area_list]

@app.callback(
	Output('magnitude-range', 'value'),
	[Input('past-occurrence', 'value'), Input('magnitude-range', 'options')]
)
def set_magnitude_value(past_occurrence, options):
	if past_occurrence == 'all_hour':
		return options[-1]['value']
	return options[-3]['value']

@app.callback(
	Output('area-list', 'value'), [Input('area-list', 'options')]
)
def set_area_value(options):
	return options[0]['value']

@app.callback(
	Output('map-quakes', 'children'),
	[Input('past-occurrence', 'value'), Input('magnitude-range', 'value'), 
		Input('map-type', 'value'), Input('area-list', 'value'), 
		Input('output-update', 'n_intervals')],
)
def visualize_quakes(past_occurrence, mag_value, map_type, specific_area, n_intervals):
	eqdf = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/' + str(past_occurrence) + '.csv')

	try:
		eqdf = eqdf[eqdf['mag'] > int(mag_value)]

		if specific_area == 'Worldwide':
			eqdf = eqdf
			zoom = 1
			radius = 10
		else: 
			eqdf = eqdf[eqdf['place'].str.contains(str(specific_area))]
			zoom = 3
			radius = 15

		latitudes = eqdf['latitude'].to_list()
		longitudes = eqdf['longitude'].to_list()

		magnitudes = eqdf['mag'].to_list()
		mags = [float(i) * radius_multiplier['outer'] for i in magnitudes]
		mags_info = ['Magnitude : ' + str(m) for m in magnitudes]

		depths = eqdf['depth'].to_list()
		deps_info = ['Depth : ' + str(d) for d in depths]
		places = eqdf['place'].to_list()

		center_lat = eqdf[eqdf['mag'] == eqdf['mag'].max()]['latitude'].to_list()[0]
		center_lon = eqdf[eqdf['mag'] == eqdf['mag'].max()]['longitude'].to_list()[0]
		print(center_lat, center_lon)

		if (map_type == 'Density Map'):
			map_trace = PlotDensityMap(latitudes, longitudes, magnitudes, radius, 'Electric')
			layout_map = LayoutDensity(500, 930, 'stamen-terrain', center_lat, center_lon, zoom)
			visualization = html.Div([
				dcc.Graph(
					id='density-map',
					figure={'data' : [map_trace], 'layout' : layout_map}
				),
			], style={'margin-top' : 30, 'margin-left' : 20})
			return visualization

		if (map_type == 'Scatter Map'):
			quake_info = [places[i] + '<br>' + mags_info[i] + '<br>' + deps_info[i]
				for i in range(eqdf.shape[0])]
			map_trace = PlotScatterMap(latitudes, longitudes, mags, magnitudes, cs_mag, quake_info)
			layout_map = LayoutScatter(500, 930, 'stamen-terrain', center_lat, center_lon, zoom)
			visualization = html.Div([
				dcc.Graph(
					id='scatter-map',
					figure={'data' : [map_trace], 'layout' : layout_map}
				),
			], style={'margin-top' : 30, 'margin-left' : 20})
			return visualization
	except Exception as e:
		return html.Div([
			html.H4('Please select magnitude and a specific area')
		])






if __name__ == '__main__':
	app.run_server(debug=True)