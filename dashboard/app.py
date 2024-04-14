import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

from auxiliary_functions import get_dataset, temp_combo_chart, temp_bar_charts, temp_bubble_chart, analytical_tables

# Page config
im = Image.open('dashboard/icon/bike.ico')
st.set_page_config(
    page_title="AW Reports",
    page_icon=im,
    layout="wide",
)

# Loads the dataset

df = get_dataset()

# Application tittle

st.markdown("""
    ## Adventure Works Sales Report
    ---
""")

# SIDEBAR - Filters

with st.sidebar:
    
    initial_date = st.date_input(label='Initial Date', value=df['Order Date'].min(),
     min_value=df['Order Date'].min(), max_value=df['Order Date'].max())
    
    initial_date = initial_date.strftime("%Y-%m-%d")
    

    end_date = st.date_input(label='End Date', value=df['Order Date'].max(),
     min_value=df['Order Date'].min(), max_value=df['Order Date'].max())
    
    end_date = end_date.strftime("%Y-%m-%d")

# Info do dataset

with st.expander('Dataset info'):

    st.header('Infos of the Dataset')
    st.subheader('First records')
    st.write(df.head())

    st.subheader('Columns')

    for col in df.columns:
        st.markdown(f'* {col}')

    st.subheader('Missing Data')
    st.write(df.isna().sum()[df.isna().sum() > 0])

    st.subheader('Descriptive statistics - numeric columns')
    df_description_numeric_columns = df.drop(columns=['Product Make Flag', 'Salable Item', 'Is Ordered Online'])
    st.write(df_description_numeric_columns.describe(include=[np.number]))

    st.subheader('Descriptive statistics - categorical columns')
    st.write(df.describe(include='object'))

# KPIs

col1, col2, col3, col4 = st.columns(4)

df_temp_cards = df.set_index(['Order Date'])
df = df.sort_index()


with col1:
    total_negociated_value = df_temp_cards.loc[initial_date:end_date]
    total_negociated_value = round(total_negociated_value['Unit Price'].sum(), 2)
    kpi1 = st.metric(label='Total Negociated Value', value=total_negociated_value)

with col2:
    average_ticket = df_temp_cards.loc[initial_date:end_date]
    average_ticket = round(average_ticket['Unit Price'].mean(), 2)
    kpi2 = st.metric(label='Average Ticket', value=average_ticket)

with col3:
    quantity_purchased = df_temp_cards.loc[initial_date:end_date]
    quantity_purchased = round(quantity_purchased['Quantity'].sum(), 2)
    kpi3 = st.metric(label='Quantity Purchased', value=quantity_purchased)

with col4:
    number_of_orders = df_temp_cards.loc[initial_date:end_date]
    number_of_orders = len(number_of_orders['Order'].unique())
    kpi4 = st.metric(label='Number of Orders', value=number_of_orders)


# Combo chart
subfig_combo_chart = temp_combo_chart(initial_date, end_date)

st.plotly_chart(subfig_combo_chart)


# Bar charts

col1, col2 = st.columns(2)

fig_1, fig_2 = temp_bar_charts(initial_date, end_date)

with col1:
    st.plotly_chart(fig_1)
 

with col2:
    st.plotly_chart(fig_2)

# Bubble chart

bubble_chart = temp_bubble_chart(initial_date, end_date)

st.plotly_chart(bubble_chart)

# Tables

table_1, table_2 = analytical_tables(initial_date, end_date)

st.dataframe(table_1, width=900)

st.dataframe(table_2, width=900)
