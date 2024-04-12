import numpy as np
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots


# Defines the function that creates the pandas dataset and made some changes on it

def get_dataset():

    df = pd.read_csv('./dashboard/data/fct_sales_order.csv')

    df = df.drop(columns=['products_fk', 'customer_fk', 'location_sk'])

    df = df.rename(columns={'sales_order_id_fk': 'Order', 'full_customer_name': 'Customer', 'bill_city': 'Bill City', 'bill_state_or_province':'Bill State/Province',
    'bill_country':'Bill Country', 'ship_city':'Ship City', 'ship_state_or_province': 'Ship State/Province', 'ship_country':'Ship Country',
           'credit_card_name': 'Credit Card Name', 'product_name': 'Product', 'model_name': 'Model', 'category_name':'Category',
           'subcategory_name':'Subcategory', 'product_make_flag':'Product Make Flag', 'product_salable_item':'Salable Item',
           'product_line':'Product Line', 'product_class':'Product Class', 'product_style':'Product Style', 'reason_per_order':'Sale Reason',
           'order_date':'Order Date', 'due_date':'Due Date', 'ship_date':'Ship Date', 'is_ordered_online':'Is Ordered Online', 'order_qty':'Quantity',
           'unit_price':'Unit Price', 'unit_price_discount':'Discount', 'order_tax_amount_per_product':'Tax',
           'order_freight_per_product':'Freight per product', 'revenue':'Revenue'})
    df['Order Date'] = pd.to_datetime(df['Order Date']).dt.date
    df['Due Date'] = pd.to_datetime(df['Due Date']).dt.date
    df['Ship Date'] = pd.to_datetime(df['Ship Date']).dt.date
    return df

# Defines the function that creates the combo chart of the aplication
def temp_combo_chart(initial_date, end_date):

    df = get_dataset()

    df_temp_combo_chart = df.set_index(['Order Date'])
    df_temp_combo_chart = df_temp_combo_chart[initial_date:end_date]
    df_temp_combo_chart = df_temp_combo_chart[['Unit Price', 'Quantity']]
    resampled = df_temp_combo_chart.resample(rule='m').sum() 
    subfig = make_subplots(specs=[[{"secondary_y": True}]])
    fig_bar = px.bar(data_frame=resampled, x=resampled.index, y='Quantity', labels={
        'Quantity': 'Quantity Purchased'
    })
    fig_bar.update_traces(marker_color='#023047')
    fig_line = px.line(data_frame=resampled, x=resampled.index, y='Unit Price', labels={
        'Unit Price':'Total Negociated Value'
    })
    fig_line.update_traces(line_color='#ffb703', yaxis="y2")
    subfig.add_traces(fig_line.data + fig_bar.data)
    subfig.update_layout(title={
        'text' : 'Total Negociated and Quantity Purchased Over Time',
        'font_size':18},width=950, height=400, template='presentation')
    return subfig

# Defines the function that creates the bar charts of the aplication
def temp_bar_charts(initial_date, end_date):
    df = get_dataset()
    df_bar_plots = df.set_index(['Order Date'])

    total_negociated_per_reason = df_bar_plots[initial_date:end_date]
    total_negociated_per_reason = total_negociated_per_reason[['Sale Reason', 'Unit Price']].groupby(['Sale Reason'], as_index=False).sum()
    total_negociated_per_reason = total_negociated_per_reason.sort_values(by=['Unit Price'], ascending=False)
    fig_1 = px.histogram(data_frame=total_negociated_per_reason, x='Sale Reason', y='Unit Price', labels={
        'Unit Price':'Total Negociated Value'
    })
    fig_1.update_traces(marker_color='#023047')
    fig_1.update_layout(
        title={
    'text' : 'Total Negociated per Sales reason',
    'font_size':18},
    xaxis_title={
        'text':'',
        'font_size':12
    },
    yaxis_title={
        'text':''
    },
    font_size=14, width=500, height=400, template='presentation')

    total_negociated_per_customer = df_bar_plots[initial_date:end_date]
    total_negociated_per_customer = total_negociated_per_customer[['Customer', 'Unit Price']].groupby(['Customer'], as_index=False).sum()
    total_negociated_per_customer = total_negociated_per_customer.sort_values(by=['Unit Price'], ascending=False)
    fig_2 = px.bar(data_frame=total_negociated_per_customer.head(15), x='Customer', y='Unit Price', labels={
        'Unit Price':'Total Negociated Value',
    })
    fig_2.update_traces(marker_color='#ffb703')
    fig_2.update_layout(
        title={
    'text' : 'Total Negociated per Customer',
    'font_size':18},
    xaxis_title={
        'text':'',
        'font_size':12
    },
    yaxis_title={
        'text':''
    },
    font_size=12, width=500, height=400, template='presentation')

    return fig_1, fig_2

# Defines the function that creates a bubble chart to the application

def temp_bubble_chart(initial_date, end_date):
    df = get_dataset()
    df_bubble_chart = df.set_index(['Order Date'])
    df_bubble_chart = df_bubble_chart[initial_date:end_date]
    df_bubble_chart = df_bubble_chart[['Ship Country', 'Ship City', 'Quantity', 'Unit Price', 'Revenue']].groupby(['Ship Country', 'Ship City'], as_index=False).sum()
    bubble_chart = px.scatter(data_frame=df_bubble_chart, x='Revenue', y="Unit Price", size="Quantity", color="Ship Country",
               hover_name="Ship City", log_x=True, size_max=60, labels={
                'Ship Country': 'Country',
                'Ship City': 'City',
                'Quantity':'Quantity Purchased',
                'Unit Price': 'Total Negociated Value'
               },color_discrete_sequence=px.colors.qualitative.Bold, width=900, height=400, template='presentation')
    return bubble_chart

def analytical_tables(initial_date, end_date):
    df = get_dataset()
    df_product_info = df.set_index(['Order Date'])
    df_product_info = df_product_info[initial_date:end_date]
    df_product_info = df_product_info[['Product', 'Quantity', 'Unit Price']]
    df_quantity = df_product_info[['Product', 'Quantity']].groupby(['Product'], as_index=False).sum()

    df_average = df_product_info[['Product', 'Unit Price']].groupby(['Product'], as_index=False).mean()
    df_average = df_average.rename(columns={'Unit Price':'Average Ticket'})
    df_average = df_average.drop(columns=['Product'], axis=1)

    df_total_negociated = df_product_info[['Product', 'Unit Price']].groupby(['Product'], as_index=False).sum()
    df_total_negociated = df_total_negociated.rename(columns={'Unit Price':'Total Negociated Value'})
    df_total_negociated = df_total_negociated.drop(columns=['Product'], axis=1)

    df_qty_avg_total = pd.concat([df_quantity, df_average, df_total_negociated], axis=1)
    df_qty_avg_total = df_qty_avg_total.sort_values(by=['Total Negociated Value'], ascending=False)


    df_credit_info = df.set_index(['Order Date'])
    df_credit_info = df_credit_info[initial_date:end_date]
    df_credit_info = df_credit_info[['Credit Card Name', 'Unit Price']]
    df_number_of_orders = df_credit_info[['Credit Card Name']].groupby(['Credit Card Name'], as_index=False).value_counts()

    df_total_negociated = df_credit_info[['Credit Card Name', 'Unit Price']].groupby(['Credit Card Name'], as_index=False).sum()
    df_total_negociated = df_total_negociated.rename(columns={'Unit Price':'Total Negociated Value'})
    df_total_negociated = df_total_negociated.drop(columns=['Credit Card Name'], axis=1)

    df_num_total = pd.concat([df_number_of_orders, df_total_negociated], axis=1)
    df_num_total = df_num_total.sort_values(by=['Total Negociated Value'], ascending=False)

    return df_qty_avg_total, df_num_total