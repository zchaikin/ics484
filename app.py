from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as pl
from plotly.subplots import make_subplots
import pandas as pd

app = Dash(__name__)

### header END

### DATASET import and prep START
def sep_by_brands(df): # Helper function to seperate GPUs into three datasets by company
    amd = df[df['ALL VIDEO CARDS'].str.contains('^AMD.*') == True]
    intel = df[df['ALL VIDEO CARDS'].str.contains('^Intel.*') == True]
    nvidia = df[df['ALL VIDEO CARDS'].str.contains('^NVIDIA.*') == True]
    return amd, intel, nvidia


data = pd.read_csv('data/Steam Hardware & Software Survey_ October 2022.csv')
by_card = pd.read_csv('data/PC_VIDEO_CARD_USAGE_DETAILS_JUN_-_OCT.csv')
by_company = pd.read_csv('data/Steam Hardware & Software Survey Video Card Company Comparison_ October 2022.csv')

amd, intel, nvidia = sep_by_brands(data)
### DATASET import and prep END

### FIGURE Vendor Market Share START
def vendor_share_month():
    June = by_company.iloc[:, [0, 1]]
    July = by_company.iloc[:, [0, 2]]
    Aug = by_company.iloc[:, [0, 3]]
    Sep = by_company.iloc[:, [0, 4]]
    Oct = by_company.iloc[:, [0, 5]]
### FIGURE Vendor Market Share END

### FIGURE amd line chart START
def amd_line_percent():
    #ss
### FIGURE amd line chart END

### FIGURE nvidia line chart START
### FIGURE nvidia line chart END

### FIGURE intel line chart START
### FIGURE intel line chart END

### ??? "other" line chart ???

### WEBSITE header, nav and footer START
app.layout = html.Div([
    html.H1('UH MANOA ICS-484 Fall 2022 Project 3'),
    dcc.Tabs(
        id="tabs",
        value='tab1',                       # SETTING for DEFAULT TAB
        parent_className='tabs-css',
        className='tabs-container-css',
        children=[
            dcc.Tab(label='TAB NAME HERE',  # EDIT Home tab!
                value='tab1',
                className='tab-css',
                selected_className='tab-selected-css',
            ),
            dcc.Tab(label='TAB NAME HERE',  # EDIT amd tab!
                value='tab2',
                className='tab-css',
                selected_className='tab-selected-css',
            ),
            dcc.Tab(label='TAB NAME HERE',  # EDIT nvidia tab !
                value='tab3',
                className='tab-css',
                selected_className='tab-selected-css',
            ),
            dcc.Tab(label='TAB NAME HERE',  # EDIT intel tab!
                value='tab4',
                className='tab-css',
                selected_className='tab-selected-css',
            ),
#            dcc.Tab(label='TAB NAME HERE',  # ??? "Other" tab ???
#                value='tab5',
#                className='tab-css',
#                selected_className='tab-selected-css',
#            ),
        ]),
    html.Div(id='tab-content'),             # DO NOT EDIT!

    html.Div(id='footer', children=[        # EDIT!
        html.P('Developed in Python, HTML and CSS. Leverages libraries from Plotly, Dash, and Panda'),
        html.P('Datafiles provided by ---'), ### TODO: Credit Valve
        html.P('Dashboard developed for assigned UH@Manoa ICS 484 Fall 2022 course material by'),
        html.P('Samuel Chrisopher Roberts (scrobert@hawaii.edu)'), ### TODO: create mailto link
        html.P('Taylor Wong (taylorsw@hawaii.edu)'), ### TODO: group mate attribution, create mailto link
        html.P('---- (---)'), ### TODO: group mate attribution, create mailto link
        html.P('---- (---)'), ### TODO: group mate attribution, create mailto link

    ])
])
### WEBSITE header, nav and footer END

### WEBSITE Tab Switching Navigation Callback Logic START
### WEBSITE Tab Switching Navigation Callback Logic END

### DASH footer START

if __name__ == '__main__':
    app.run_server(debug=True)