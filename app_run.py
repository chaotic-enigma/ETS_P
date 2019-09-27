import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import (Input, Output)

import pandas as pd

from GraphPlotting import (PlotDensityMap, LayoutDensity, PlotLayout)

external_scripts = ['https://www.google-analytics.com/analytics.js']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

with open('map_token.txt', 'r') as mk:
	map_token = mk.read()

app = dash.Dash(__name__,
	external_scripts=external_scripts,
	external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True



app.layout = html.Div([
	html.Div([
		html.Div([html.H2('Earthquake Tracking System')],
			style={'textAlign' : 'center'}),
		html.Div([
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
			], className='three columns')
		], className='row'),
		html.Div([
			dcc.Interval(
				id='map-update',
				interval=60*1000
			)
		]),
		html.Div(id='map-quakes')
	])
])

@app.callback(
	Output('map-quakes', 'children'),
	[Input('past-occurrence', 'value'), Input('map-update', 'n_intervals')],
)
def visualize_quakes(past_occurrence, n):
	eqdf = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/' + str(past_occurrence) + '.csv')

	if past_occurrence != 'all_hour':
		eqdf = eqdf[eqdf['mag'] >= 2]

	latitudes = eqdf['latitude'].to_list()
	longitudes = eqdf['longitude'].to_list()
	magnitudes = eqdf['mag'].to_list()
	places = eqdf['place'].to_list()

	center_lat = eqdf[eqdf['mag'] >= eqdf['mag'].max()]['latitude'].to_list()[0]
	center_lon = eqdf[eqdf['mag'] >= eqdf['mag'].max()]['longitude'].to_list()[0]
	print(center_lat, center_lon)

	map_trace = PlotDensityMap(latitudes, longitudes, magnitudes, 10, 'Electric')
	density_layout = LayoutDensity(500, 1000, 'stamen-terrain', center_lat, center_lon)

	visualization = html.Div([
		dcc.Graph(
			id='past-result',
			figure={'data' : [map_trace], 'layout' : density_layout}
		),
	], style={'margin-top' : 30, 'margin-left' : 180})

	return visualization





if __name__ == '__main__':
	app.run_server(debug=True)