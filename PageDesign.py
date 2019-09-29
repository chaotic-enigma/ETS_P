import dash_core_components as dcc
import dash_html_components as html

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
		'padding': '20px 20px', 'margin-left' : 20, 
		'margin-right' : 20, 'margin-top' : 10
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
],style={'margin-left' : 20, 'margin-top' : 20, 'margin-bottom' : 10})
#</density_and_scatter_map>

#<seismic_report_result>
seismic_map_result = html.Div([
	html.Div([
		html.Div(id='largest-quake', style={'textAlign' : 'left'}),
		html.Div(id='map-quakes'),
	], className='nine columns', style={'margin-left' : 20}),

	html.Div([
		html.Div([
			html.H6('Seismic Report', 
				style={'backgroundColor' : colors_useful['symmetry'], 'textAlign' : 'center'}),
			html.Div([
				html.Div(id='people-reports')
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
			], style={'overflowY' : 'scroll', 'height' : 130})
		]),
	], className='three columns', style={'margin-top' : 50, 'margin-left' :5})
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
], className='row', style={'margin-left' : 20})
#</basic_visualization>