import sqlite3
import pandas as pd
import plotly.express as px

import dash
from dash import dcc, html
from dash import dash_table
from dash_table import DataTable, FormatTemplate
from dash.dependencies import Input, Output

# For connection to HTML
import dash_bootstrap_components as dbc

# Establish connection to the database
conn = sqlite3.connect(f'ecom_data.sqlite3')

# Load data from the Employee table into a DataFrame
ecom_sales = pd.read_sql_query("SELECT * FROM 'ecom_data'", conn)

logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/fdbe0accd2581a0c505dab4b29ebb66cf72a1803/e-comlogo.png'
major_categories = list(ecom_sales['Major Category'].unique())
large_tb = ecom_sales.groupby(['Country'])['OrderValue'].agg(['sum', 'count', 'mean', 'median']).reset_index().rename(columns={'count':'Sales Volume', 'sum':'Total Sales ($)', 'mean':'Average Order Value ($)', 'median':'Median Order Value ($)'})
ecom_country = ecom_sales.groupby('Country')['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')
bar_fig_country = px.bar(ecom_country, x='Total Sales ($)', y='Country', width=500, height=450, title='Total Sales by Country (Hover to filter the Minor Category bar chart!)', custom_data=['Country'], color='Country', color_discrete_map={'United Kingdom':'lightblue', 'Germany':'orange', 'France':'darkblue', 'Australia':'green', 'Hong Kong':'red'})

money_format = FormatTemplate.money(2)
money_cols = ['Total Sales ($)', 'Average Order Value ($)', 'Median Order Value ($)']
d_columns = [{'name':x, 'id':x} for x in large_tb.columns if x not in money_cols]
d_columns += [
    {'name':'Total Sales ($)', 'id':'Total Sales ($)',
    'type':'numeric',
    'format':money_format
     # Allow columns to be selected
    , 'selectable':True
    },
    {'name':'Average Order Value ($)', 'id':'Average Order Value ($)',
    'type':'numeric',
    'format':money_format
     # Allow columns to be selected
    , 'selectable':True
    },
    {'name':'Median Order Value ($)', 'id':'Median Order Value ($)',
    'type':'numeric',
    'format':money_format
     # Allow columns to be selected
    , 'selectable':True
    }]


d_table = DataTable(
  			id='my_dt',
            columns=d_columns,
            data=large_tb.to_dict('records'),
            cell_selectable=False,
            sort_action='native',
  			# Make single columns selectable
            column_selectable='single'
            )

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Iframe(srcDoc=open('layout.html', 'r').read(), style={"width": "100%", "height": "100vh", "border": "none"}),

    # Dash Components as Placeholders
    html.Div(dcc.Dropdown(id='major_cat_dd', options=[{'label': cat, 'value': cat} for cat in major_categories]), style={"display": "none"}),
    html.Div(dcc.Dropdown(id='minor_cat_dd'), style={"display": "none"}),
    html.Div(DataTable(id='my_dt', columns=d_columns, data=large_tb.to_dict('records'), cell_selectable=False, sort_action='native', column_selectable='single'), style={"display": "none"}),
    html.Div(dcc.Graph(id='scatter_compare'), style={"display": "none"}),
    html.Div(dcc.Graph(id='sales_line'), style={"display": "none"}),
    html.Div(dcc.Graph(id='major_cat', figure=bar_fig_country), style={"display": "none"}),
    html.Div(dcc.Graph(id='minor_cat'), style={"display": "none"}),
    html.H3(id='chosen_major_cat_title', style={"display": "none"})
])

# Create a callback triggered by selecting a column
@app.callback(
    Output('scatter_compare', 'figure'),
    Input('my_dt', 'selected_columns'))

def table_country(selected_columns):
    comparison_col = 'Total Sales ($)'

    # Extract comparison col using its index
    if selected_columns:
        comparison_col = selected_columns[0]

    scatter_fig = px.scatter(
        data_frame=large_tb,
        x='Sales Volume',
      	# Use comparison col in figure
        y=comparison_col,
        color='Country',
        title=f'Sales Volume vs {comparison_col} by country'
    )

    return scatter_fig

@app.callback(
   Output('minor_cat_dd', 'options'),
   Output('chosen_major_cat_title', 'children'),
   Input('major_cat_dd', 'value'))

def update_dd(major_cat_dd):
    major_minor = ecom_sales[['Major Category', 'Minor Category']].drop_duplicates()
    relevant_minor = major_minor[major_minor['Major Category'] == major_cat_dd]['Minor Category'].values.tolist()
    minor_options = [dict(label=x, value=x) for x in relevant_minor]

    if not major_cat_dd:
        major_cat_dd = 'ALL'

    major_cat_title = f'This is in the Major Category of : {major_cat_dd}'

    return minor_options, major_cat_title

@app.callback(
    Output('sales_line', 'figure'),
    Input('minor_cat_dd', 'value'))

def update_line(minor_cat):
    minor_cat_title = 'All'
    ecom_line = ecom_sales.copy()
    if minor_cat:
        minor_cat_title = minor_cat
        ecom_line = ecom_line[ecom_line['Minor Category'] == minor_cat]
    ecom_line = ecom_line.groupby('Year-Month')['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')
    line_graph = px.line(ecom_line, x='Year-Month',  y='Total Sales ($)', title=f'Total Sales by Month for Minor Category: {minor_cat_title}', height=350)

    return line_graph

@app.callback(
    Output('minor_cat', 'figure'),
    Input('major_cat', 'hoverData'))

def update_min_cat_hover(hoverData):
    hover_country = 'Australia'

    if hoverData:
        hover_country = hoverData['points'][0]['customdata'][0]

    minor_cat_df = ecom_sales[ecom_sales['Country'] == hover_country]
    minor_cat_agg = minor_cat_df.groupby('Minor Category')['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')
    ecom_bar_minor_cat = px.bar(minor_cat_agg, x='Total Sales ($)', y='Minor Category', orientation='h', height=450, width=480,title=f'Sales by Minor Category for: {hover_country}')
    ecom_bar_minor_cat.update_layout({'yaxis':{'dtick':1, 'categoryorder':'total ascending'}, 'title':{'x':0.5}})

    return ecom_bar_minor_cat


if __name__ == '__main__':
    app.run_server(debug=True)