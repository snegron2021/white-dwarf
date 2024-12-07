import plotly.express as px
import pandas as pd
import numpy as np
import plotly.io as pio

data = pd.read_csv("/Users/shailynnegron/Desktop/Alldata.csv")


data['distance'] = 1 / data['parallax']

data['x'] = (data['distance']) * np.cos(np.radians(data['b'])) * np.cos(np.radians(data['l']))  # x
data['y'] = (data['distance']) * np.cos(np.radians(data['b'])) * np.sin(np.radians(data['l']))  # y
data['z'] = (data['distance']) * np.sin(np.radians(data['b']))  # z


bins = [5500, 6000, 7000, 10000, 15000, 40000]
labels = ['Cool', 'Moderate', 'Hot', 'Very Hot', 'Extremely Hot']
data['temperature_bin'] = pd.cut(data['teff_gspphot'], bins=bins, labels=labels, right=False)


df = data[['x', 'y', 'z', 'temperature_bin', 'teff_gspphot']].copy()
df['bin_numeric'] = df['temperature_bin'].cat.codes
df_sample = df.sample(frac=0.001)
                      
fig = px.scatter_3d(
    df_sample,
    x='x',
    y='y',
    z='z',
    color='bin_numeric',
    title="3D White Dwarf Distribution",
    labels={'x': 'X (Parsecs)', 'y': 'Y (Parsecs)', 'z': 'Z (Parsecs)', 'bin_numeric':'Effective Temperature (K)'},
    hover_data={'x': True, 'y': True, 'z': True, 'teff_gspphot': True}
    )

fig.update_traces(marker=dict(size=2))

fig.update_layout(
    coloraxis_colorbar=dict(
        tickvals=[0, 1, 2, 3, 4],
        ticktext=['5500-6000 K', '6000-7000 K', '7000-10000 K', '10000-15000 K', '15000-40000 K']
    )
)
fig.update_traces(
    hovertemplate=(
        'X (Parsecs): %{x}<br>' 
        'Y (Parsecs): %{y}<br>' 
        'Z (Parsecs): %{z}<br>' 
        'Effective Temperature: %{customdata[0]:.2f} K'
    )
)

pio.write_html(fig, file='/Users/shailynnegron/Desktop/3d_star_plot.html', auto_open=True)
