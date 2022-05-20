import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.title('Covid-19 Dashboard For India')
st.markdown('The dashboard will visualize the Covid-19 Situation in India')
st.markdown('Coronavirus disease (COVID-19) is an infectious disease '
            'caused by a newly discovered coronavirus. '
            'Most people infected with the COVID-19 virus will experience'
            ' mild to moderate respiratory illness and recover without'
            ' requiring special treatment.')

st.sidebar.title('Visualization Selector')
st.sidebar.markdown('Select the Chart/Plots accordingly:')

# Load the dataset
DATA_URL = ('./data/country_wise_latest.csv')


# https://www.kaggle.com/datasets/imdevskp/corona-virus-report?select=country_wise_latest.csv
@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    return data


df = load_data()

st.sidebar.checkbox("Show Analysis by State", True, key=1)
select = st.sidebar.selectbox('Select a State', df['Country/Region'])

# get the state selected in the selectbox
state_data = df[df['Country/Region'] == select]
select_status = st.sidebar.radio("Covid-19 patient's status", ('Confirmed',
                                                               'Active', 'Recovered', 'Deceased'))


# Plotting

def get_total_dataframe(dataset):
    total_dataframe = pd.DataFrame({
        'Status': ['Confirmed', 'Recovered', 'Deaths', 'Active'],
        'Number of cases': (dataset.iloc[0]['Confirmed'],
                            dataset.iloc[0]['Recovered'],
                            dataset.iloc[0]['Deaths'],
                            dataset.iloc[0]['Active'])})
    return total_dataframe


state_total = get_total_dataframe(state_data)

if st.sidebar.checkbox('Show Analysis by State', True, key=2):
    st.markdown(' ## State level Analysis ')
    st.markdown("### Overall Confirmed, Active, Recovered and " +
                "Deceased cases in %s yet" % (select))
    if not st.checkbox('Hide Graph', False, key=1):
        state_total_graph = px.bar(
            state_total,
            x='Status',
            y='Number of cases',
            labels={'Number of cases': 'Number of cases in %s' % (select)},
            color='Status')
        st.plotly_chart(state_total_graph)


def get_table():
    datatable = df[['Country/Region', 'Confirmed', 'Recovered', 'Deaths', 'Active']].sort_values(by=['Confirmed'],
                                                                                                 ascending=False)
    datatable = datatable[datatable['Country/Region'] != 'State Unassigned']
    return datatable

datatable = get_table()
st.markdown("### Covid-19 cases in India")
st.markdown("The following table gives you a real-time analysis of the confirmed, active, recovered and deceased cases of Covid-19 pertaining to each state in India.")
st.dataframe(datatable) # will display the dataframe
st.table(datatable)# will display the table
