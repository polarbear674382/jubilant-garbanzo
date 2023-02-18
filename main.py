import altair as alt
import streamlit as st
import pandas as pd
import numpy as np



@st.cache_data
def load_data(url):
    data = pd.read_csv(url)
    return data

def load_wrapper(url):
    data_load_state = st.text('Loading data...')
    data = load_data(url)
    data_load_state.text("Done loading data!")
    
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)
    
    return data


def get_totals_index(data: pd.DataFrame):
    
    return data['PORT'] != 'TOTAL FOR ALL PORTS'

def draw_topten_nominal(data: pd.DataFrame):
    # stacked bars separating exports and imports
    st.subheader('Nominal')
    idx = get_totals_index(data)
    
    source = data.loc[idx].drop('Total Trade, USD bn', axis=1).melt(id_vars = ['PORT'])
    
    c = alt.Chart(source).mark_bar().encode(
        x='sum(value)',
        y='PORT',
        color='variable'
    )
    
    st.altair_chart(c, use_container_width=True)

def draw_topten_percent(data: pd.DataFrame):

    # merged bar showing percent of total bilateral trade
    st.subheader('Percent of total for all ports')
    idx = get_totals_index(data)
    port_bilateral = data[idx].set_index('PORT')['Total Trade, USD bn']
    aggregate_total = data.loc[~idx, 'Total Trade, USD bn'].iloc[0]
    port_pct = port_bilateral / aggregate_total * 100
    port_pct.name = 'Percentage of total import and export trade'
    port_pct_df = port_pct.reset_index()
    
    c = alt.Chart(port_pct_df).mark_bar().encode(
        x='Percentage of total import and export trade',
        y='PORT',
    )
    
    st.altair_chart(c, use_container_width=True)


def draw_topten():
    
    st.header('Top ten ports by combined imports and exports, most recent 12 months')
    
    url = 'https://census-trade-gateway3-7kt8jtbo.uk.gateway.dev/topten'
    
    data = load_wrapper(url)
    
    draw_topten_nominal(data)
    
    draw_topten_percent(data)



def draw_newyork():
    
    st.header('Top trading partners for ports in NY port districts')
    
    url = 'https://census-trade-gateway3-7kt8jtbo.uk.gateway.dev/newyork'
    
    data = load_data(url)
    
    st.subheader('Top trading partner by port, for ports in NY port districts')
    st.write(data)
    

def draw_california():
    
    st.header('Top import commodities for ports in CA port districts')
    
    url = 'https://census-trade-gateway3-7kt8jtbo.uk.gateway.dev/california'
    
    data = load_data(url)
    
    st.subheader('Top imports to CA port districts')
    st.write(data)




st.title('International Trade at US Ports')
draw_topten()
draw_newyork()
draw_california()