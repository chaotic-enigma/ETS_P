import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go

from CountryHistoryProne import risky_countries

colors_useful = {
	'text_color' : '#154360',
	'bar_max_val' : 'rgba(222,45,38,0.8)',
	'bar_normal' : 'rgb(41,128,185)',
	'bar_min_val' : 'rgb(40,180,99)',
	'symmetry' : '#c3c8fc',
	'rev_symmetry' : '#fff',
	'danger' : '#fc131a',
	'loc_color' : '#d35400',
	'report_color' : '#8e44ad',
	'tsunami_color' : '#0240da'
}

########################## Real-Time Tracking ##########################

#<heading_bar_page>
heading_bar = html.Div([
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
				clearable=False,
				searchable=False,
				value='all_hour'
			),
		], className='two columns', style={'textAlign' : 'center'}),

		html.Div([html.H5('Magnitude Range')], className='two columns'),

		html.Div([dcc.Dropdown(id='magnitude-range', clearable=False, searchable=False)], 
			className='two columns', style={'textAlign' : 'center'}),

		html.Div([html.H5('Region')], className='one columns'),

		html.Div([dcc.Dropdown(id='area-list', clearable=False, searchable=True)], 
			className='three columns')
	], className='row', 
	style={
		'borderBottom' : 'thin lightgrey solid', 
		'backgroundColor' : colors_useful['symmetry'], 
		'padding': '10px 10px', 'margin-left' : 10, 
		'margin-right' : 10, 'margin-top' : 10
	})
])
#</heading_bar_page>

#<density_and_scatter_map>
map_graphing_styles = html.Div([
	dcc.RadioItems(
		id='map-type',
		options=[{'label' : s, 'value' : s} for s in ['Density Map', 'Scatter Map']],
		value='Density Map',
		labelStyle={'display': 'inline-block'}
	)
],style={'margin-left' : 10, 'margin-top' : 20, 'margin-bottom' : 10})
#</density_and_scatter_map>

#<seismic_report_result>
seismic_map_result = html.Div([
	html.Div([
		html.Div(id='largest-quake', style={'textAlign' : 'left'}),
		html.Div(id='map-quakes'),
	], className='nine columns', style={'margin-left' : 10}),

	html.Div([
		html.Div([
			html.H6('Seismic Report', 
				style={'backgroundColor' : colors_useful['symmetry'], 'textAlign' : 'center'}),
			html.Div([
				html.Div(id='felt-reports')
			], style={'overflowY' : 'scroll', 'height' : 200})
		]),
		html.Div([
			html.H6('Alert Color', 
				style={'backgroundColor' : colors_useful['symmetry'], 'textAlign' : 'center'}),
			html.Div([
				html.Div(id='alert-reports')
			], style={'overflowY' : 'scroll', 'height' : 150})
		]),
		html.Div([
			html.H6('Triggered Tsunami', 
				style={'backgroundColor' : colors_useful['symmetry'], 'textAlign' : 'center'}),
			html.Div([
				html.Div(id='tsunami-reports')
			], style={'overflowY' : 'scroll', 'height' : 115})
		]),
	], className='three columns', style={'margin-top' : 50, 'margin-left' : 8})
], className='row')
#</seismic_report_result>

#<basic_visualization>
basic_visuals = html.Div([
	html.Div([
		html.Div(id='pie-quake-type')
	], className='five columns'),
	html.Div([
		html.Div(id='area-count-plot')
	], className='seven columns')
], className='row', style={'margin-left' : 10, 'margin-top' : 30})
#</basic_visualization>

tracking_realtime = html.Div([
	html.Div([]),
	heading_bar,
	map_graphing_styles,
	html.Div([dcc.Interval(id='output-update', interval=180*1000)]),
	seismic_map_result,
	basic_visuals,
], style={'margin-top' : 20, 'margin-bottom' : 20})

########################## Real-Time Tracking ##########################

########################## Historical Insights #########################

hist_heading_bar = html.Div([
	html.Div([
		html.Div([html.H5('Risky Countries')], 
			className='five columns', style={'textAlign' : 'right'}),
		html.Div([
			dcc.Dropdown(
				id='top-thirty-risky',
				options=[{'label' : name, 'value' : code} for name, code in risky_countries.items()],
				clearable=False,
				searchable=True,
				value='ID'
			)
		], className='three columns', style={'textAlign' : 'center'})
	], className='row', style={'textAlign' : 'center'})
], style={
		'borderBottom' : 'thin lightgrey solid', 
		'backgroundColor' : colors_useful['symmetry'], 
		'padding': '10px 10px', 'margin-left' : 10, 
		'margin-right' : 20, 'margin-top' : 20
	}
)

year_marks = np.linspace(1965, 2016, 15)
year_marks = [int(i) for i in year_marks]
range_slider = html.Div([
	dcc.Slider(
		id='year-slider',
		min=min(year_marks),
		max=max(year_marks),
		step=1,
		marks={i : '{}'.format(i) for i in year_marks},
		value=year_marks[0]
	)
], className='container', style={'margin-left' : 10, 'margin-top' : 10})

country_history_map = html.Div([
	html.Div([html.Div(id='map-history')], className='nine columns'),
	html.Div([
		html.Div([
			html.P('Total occurrences : ', className='six columns'),
			html.Div(id='res-total-occurrences', className='six columns'),
		], className='row'),
		html.Div([
			html.P('Yearly ', className='three columns'),
			html.Div(id='res-year-num', className='three columns'),
			html.Div(id='res-yearly-occ', className='six columns')
		], className='row'),
		html.Div([
			html.P('Highest magnitude : ', className='six columns'),
			html.Div(id='res-high-mag', className='six columns')
		], className='row'),
		html.Div([
			html.P('Depth : ', className='six columns'),
			html.Div(id='high-mag-depth', className='six columns')
		], className='row'),
		html.Div([
			html.P('Disaster type : ', className='six columns'),
			html.Div(id='high-mag-type', className='six columns')
		], className='row'),
		html.Div(id='res-place')
	], className='three columns', style={'margin-top' : 120})
], className='row')

def country_count_plot():
	dataq = pd.read_csv('quake_db_1965-2016.csv')
	dataq = dataq[dataq['Place'] != 'Unknown']
	dataq['CountryCode'] = dataq['Place'].apply(lambda x : x.split(', ')[len(x.split(', ')) - 1])
	thirty_prone = list(dataq['CountryCode'].value_counts().nlargest(30).index)
	thirty_updated = dataq['CountryCode'].where(dataq['CountryCode'].isin(thirty_prone), other='Other')
	thirty_df = thirty_updated.value_counts().to_frame()
	thirty_df.reset_index(inplace=True)
	thirty_df.columns = ['CountryCode', 'Count']
	trace = [
		go.Bar(
			x=thirty_df['CountryCode'],
			y=thirty_df['Count']
		)
	]
	layout = go.Layout(
		title='Total earthquakes by country', 
		xaxis=dict(title='Country'),
		yaxis=dict(title='Count')
	)
	return {'data' : trace, 'layout' : layout}

country_count_quakes = html.Div([
	dcc.Graph(
		id='country-count-res',
		figure=country_count_plot()
	)
], style={'margin-top' : 30})

insightful_history = html.Div([
	html.Div([]),
	hist_heading_bar,
	country_history_map,
	range_slider,
	country_count_quakes
])

########################## Historical Insights #########################