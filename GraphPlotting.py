import plotly.graph_objs as go

#<DensityMap>
def PlotDensityMap(lat, lon, z, radius, colorscale):
	density_map_trace = go.Densitymapbox(
	  lat=lat,
	  lon=lon,
	  z=z,
	  radius=radius,
	  colorscale=colorscale,
	)
	return density_map_trace

def LayoutDensity(height, width, mapbox_style, c_lat, c_lon, zoom):
	layout_density_map = go.Layout(
		height=height,
	  width=width,
	  autosize=True,
	  showlegend=False,
	  hovermode='closest',
	  margin=dict(l=0, r=0, t=0, b=0),
	  mapbox_style=mapbox_style,
	  mapbox_center_lat=c_lat,
	  mapbox_center_lon=c_lon,
	  mapbox=dict(
	  	zoom=zoom
	  )
	)
	return layout_density_map
#</DensityMap>

#<ScatterMap>
def PlotScatterMap(lat, lon, size, color, colorscale, text):
	scatter_map_trace = go.Scattermapbox(
		lat=lat,
		lon=lon,
		mode='markers',
		marker=dict(
			size=size, color=color, opacity=1,
			colorscale=colorscale,
		),
		text=text, hoverinfo='text', showlegend=True
	)
	return scatter_map_trace

def LayoutScatter(height, width, mapbox_style, c_lat, c_lon, zoom):
	layout_scatter_map = go.Layout(
	  height=height,
	  width=width,
	  autosize=True,
	  showlegend=False,
	  hovermode='closest',
	  margin=dict(l=0, r=0, t=0, b=0),
	  mapbox_style=mapbox_style,
	  mapbox=dict(
	    center=dict(
	      lat=c_lat,
	      lon=c_lon
	    ),
	    zoom=zoom
	  )
	)
	return layout_scatter_map
#</ScatterMap>

