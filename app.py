from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from PIL import Image

app = Dash(__name__)


### header END

### DATASET import and prep START
def sep_by_brands(df):  # Helper function to seperate GPUs into three datasets by company
    amd = df[df['ALL VIDEO CARDS'].str.contains('^AMD.*') == True]
    intel = df[df['ALL VIDEO CARDS'].str.contains('^Intel.*') == True]
    nvidia = df[df['ALL VIDEO CARDS'].str.contains('^NVIDIA.*') == True]
    return amd, intel, nvidia


data = pd.read_csv('data/Steam Hardware & Software Survey_ October 2022.csv')
by_card = pd.read_csv('data/PC_VIDEO_CARD_USAGE_DETAILS_JUN_-_OCT.csv')
by_company = pd.read_csv('data/Steam Hardware & Software Survey Video Card Company Comparison_ October 2022.csv')
reformat = pd.read_csv('data/Reformated.csv')
June = by_company.iloc[:, [0, 1]]
July = by_company.iloc[:, [0, 2]]
Aug = by_company.iloc[:, [0, 3]]
Sep = by_company.iloc[:, [0, 4]]
Oct = by_company.iloc[:, [0, 5]]

amd, intel, nvidia = sep_by_brands(data)


### DATASET import and prep END

### FIGURE Vendor Market Share START
def vendor_share():
    fig = go.Figure()
    name = reformat.columns.tolist()
    name.remove('MONTH')
    count = 0
    blankgpu=Image.open('data/blankgpu.png')

    for i in reformat.columns[1:]:
        reformat[i] = reformat[i].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=reformat.MONTH,
                y=reformat[i],
                name=name[count],
            )
        )
        count += 1

    fig.add_layout_image(
        dict(
            source=blankgpu,
            xref='x', yref='y', x=-1, y=80, sizex=10, sizey=75, opacity=0.5, layer='below'
        )
    )
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Market Share (%)',
        legend_title='Vendors',
        title='Steam Market Share by Vendor',
        annotations=[dict(text='NVIDIA still #1', x='OCT', y=76.24),
                     dict(text='Race for last place', x='OCT', y=9.25)],
        width=1808,
        height=1017,
        template='plotly_white'
    )
    return fig


### FIGURE Vendor Market Share END

### FIGURE amd line chart START
def amd_line():
    fig = go.Figure()


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
        value='tab1',  # SETTING for DEFAULT TAB
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
    html.Div(id='tab-content'),  # DO NOT EDIT!
    html.Div(id='vendor-graph', children=[
        html.Div([dcc.Graph(figure=vendor_share())], )
    ]),

    html.Div(id='footer', children=[  # EDIT!
        html.P('Developed in Python, HTML and CSS. Leverages libraries from Plotly, Dash, and Panda'),
        html.P('Datafiles provided by ---'),  ### TODO: Credit Valve
        html.P('Dashboard developed for assigned UH@Manoa ICS 484 Fall 2022 course material by'),
        html.P('Samuel Chrisopher Roberts (scrobert@hawaii.edu)'),  ### TODO: create mailto link
        html.P('Taylor Wong (taylorsw@hawaii.edu)'),  ### TODO: group mate attribution, create mailto link
        html.P('---- (---)'),  ### TODO: group mate attribution, create mailto link
        html.P('---- (---)'),  ### TODO: group mate attribution, create mailto link

    ]),

])
### WEBSITE header, nav and footer END

### WEBSITE Tab Switching Navigation Callback Logic START
### WEBSITE Tab Switching Navigation Callback Logic END

### DASH footer START
### DASH footer END

### Callback functions START

### Callback functions END

if __name__ == '__main__':
    app.run_server(debug=True)
