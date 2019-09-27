import plotly.graph_objs as go

def PlotDensityMap(lat, lon, z, radius, colorscale):
	density_trace = go.Densitymapbox(
	  lat=lat,
	  lon=lon,
	  z=z,
	  radius=radius,
	  colorscale=colorscale,
	)
	return density_trace

def LayoutDensity(height, width, mapbox_style, c_lat, c_lon):
	density_layout = go.Layout(
		height=height,
	  width=width,
	  autosize=True,
	  showlegend=False,
	  hovermode='closest',
	  margin=dict(l=0, r=0, t=0, b=0),
	  mapbox_style=mapbox_style,
	  mapbox_center_lat=c_lat,
	  mapbox_center_lon=c_lon
	)
	return density_layout

def PlotLayout(height, width, mapbox_style, c_lat, c_lon):
	layout_map = go.Layout(
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
	  )
	)
	return layout_map