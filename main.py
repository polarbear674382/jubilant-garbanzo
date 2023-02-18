import streamlit as st
import pandas as pd
import numpy as np
"""
st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)
"""

st.title('International Trade at US Ports')

DATE_COLUMN = 'date/time'
DATA_URL = 'https://census-trade-gateway3-7kt8jtbo.uk.gateway.dev/topten'

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL)
    return data

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Top ten ports by combined import and export trade, most recent 12 months')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(data.set_index('PORT')['Total Trade, USD bn'])

####################

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# stacked bars separating exports and imports
idx = data['PORT'] != 'TOTAL FOR ALL PORTS'

source = data.loc[idx].melt(id_vars = ['PORT'])

c = alt.Chart(source).mark_bar().encode(
    x='sum(value)',
    y='PORT',
    color='variable'
)

st.altair_chart(c, use_container_width=True)


# merged bar showing percent of total bilateral trade
port_bilateral = x[idx].set_index('PORT')['Total Trade, USD bn']
aggregate_total = x.loc[~idx, 'Total Trade, USD bn'].iloc[0]
port_pct = port_bilateral / aggregate_total * 100
port_pct.name = 'Percentage of total import and export trade'
st.subheader('Top ten ports by combined import and export trade, most recent 12 months, percent of total')
st.bar_chart(port_pct)
