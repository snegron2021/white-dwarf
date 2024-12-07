import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np

# Read the data
data = pd.read_csv("/Users/shailynnegron/Desktop/Alldata.csv")

# Calculate distance in parsecs
data['distance'] = 1 / data['parallax']

# Cartesian coordinate calculations (parsecs)
data['x'] = (data['distance']) * np.cos(np.radians(data['b'])) * np.cos(np.radians(data['l']))  # x
data['y'] = (data['distance']) * np.cos(np.radians(data['b'])) * np.sin(np.radians(data['l']))  # y
data['z'] = (data['distance']) * np.sin(np.radians(data['b']))  # z

# Define temperature bins
bins = [5500, 6000, 7000, 10000, 15000, 40000]
labels = ['Cool', 'Moderate', 'Hot', 'Very Hot', 'Extremely Hot']
data['temperature_bin'] = pd.cut(data['teff_gspphot'], bins=bins, labels=labels, right=False)

# Create a new DataFrame with temperature and coordinates
df = data[['x', 'y', 'z', 'temperature_bin', 'teff_gspphot']].copy()
df['bin_numeric'] = df['temperature_bin'].cat.codes
df_sample = df.sample(frac=0.01)

# Create the Plotly 3D scatter plot
fig = px.scatter_3d(
    df_sample,
    x='x',
    y='y',
    z='z',
    color='bin_numeric',
    title="3D White Dwarf Distribution",
    labels={'x': 'X (Parsecs)', 'y': 'Y (Parsecs)', 'z': 'Z (Parsecs)', 'bin_numeric': 'Effective Temperature (K)'},
    hover_data={'x': True, 'y': True, 'z': True, 'teff_gspphot': True}
)

fig.update_traces(marker=dict(size=2))

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Interactive 3D White Dwarf Distribution"),
    dcc.Graph(figure=fig)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
