import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st

# https://sakizo-blog.com/158/
# Streamlit Setting
st.set_page_config(layout="wide")

# Main Window

st.title('Dashboard Example')
st.write(
    '''
    ### This apps is showing the plot chart with data that will be uploaded through streamlit.
    ### Developed by S.Choe Ph.D.
    ### 2022 Tomomi Research, Inc.
    '''
)

# Layout SideBar
st.sidebar.title('CSV file uploader')
# Upload file
uploade_csv = st.sidebar.file_uploader('Choose a CSV file')

if uploade_csv is not None:
    # Data frame
    df = pd.read_csv(uploade_csv)
    # categorical varables, continous variables list
    var_cat = [var for var in df.columns if var.startswith('cat')]
    var_cont = [var for var in df.columns if var.startswith('cont')]

    st.subheader('Graph')
    df_target = df[['id', 'target']].groupby('target').count() / len(df)
    st.write(df_target)
    fig_target = go.Figure(data=[go.Pie(
        labels=df_target.index,
        values=df_target['id'],
        hole=.3)]
    )



    fig_target.update_layout(showlegend=False,
                             height=200,
                             margin={'l': 20, 'r': 60, 't': 0, 'b': 0})
    fig_target.update_traces(
        textposition='inside',
        textinfo='label+percent'
    )

    # layout(sidebar later)
    st.markdown('## Settings')
    cat_selected = st.selectbox('Categorical Variables', var_cat)
    cont_selected = st.selectbox('Continuous Variables', var_cont)
    cont_multi_selected = st.multiselect('Correlation Matrix', var_cont, default=var_cont)

    st.markdown('## Target Variables')
    st.plotly_chart(fig_target, use_container_width=True)
