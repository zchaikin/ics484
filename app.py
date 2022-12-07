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
Months = ['JUN', 'JUL', 'AUG', 'SEP', 'OCT']

amd, intel, nvidia = sep_by_brands(data)


### DATASET import and prep END

### FIGURE Vendor Market Share START
def vendor_share():
    fig = go.Figure()
    name = reformat.columns.tolist()
    name.remove('MONTH')
    count = 0
    blankgpu = Image.open('data/blankgpu.png')

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
            xref='x', yref='y', x=-1, y=95, sizex=10, sizey=95, opacity=0.5, layer='below'
        )
    )
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Market Share (%)',
        legend_title='Vendors',
        title='Steam Market Share by Vendor',
        width=1808,
        height=1017,
        template='plotly_white',
        font=dict(
            size=20
        )
    )
    fig.update_traces(marker=dict(size=18), line=dict(width=8))
    return fig


### FIGURE Vendor Market Share END

### FIGURE amd line chart START
def amd_line():
    fig = go.Figure()  # make fig

    AMD = by_card.filter(regex=('(AMD.*?)'))

    graphics = AMD.filter(regex=('[^.*?](Graphics.*?)'))
    graphics.insert(0, 'MONTH', Months, True)
    graphics = graphics.set_index(['MONTH'])

    RX = AMD.filter(regex=('[^.*?](RX.*?)'))
    RX.insert(0, 'MONTH', Months, True)
    RX = RX.set_index(['MONTH'])
    RX = RX.drop(columns=['AMD Radeon RX Vega 11 Graphics'])

    fig.update_layout(
        width=1600,
        height=900,
        template='plotly_white',
        font=dict(size=20),
        autosize=True,
    )
    for col in graphics.columns[:]:
        graphics[col] = graphics[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=graphics.index,
                y=graphics[col],
                name=col
            )
        )

    for col in RX.columns[:]:
        RX[col] = RX[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=RX.index,
                y=RX[col],
                name=col
            )
        )

    fig.update_layout(updatemenus=[go.layout.Updatemenu(
        active=0,
        x=0.55, y=1.11,
        buttons=list(
            [dict(label='ALL',
                  method='update',
                  args=[{'visible': [True, True, True, True, True, True, True, True, True, True, True, True,
                                     True, True, True, True, True, True, True, True]},
                        {'title': 'ALL',
                         'showlegend': True}]),
             dict(label='Graphics',
                  method='update',
                  args=[{'visible': [True, True, True, True, True, True, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False]},
                        {'title': 'Graphics',
                         'showlegend': True}]),
             dict(label='RX',
                  method='update',
                  args=[{'visible': [False, False, False, False, False, False, True, True, True, True, True, True, True,
                                     True, True, True, True, True, True, True, True]},
                        {'title': 'RX',
                         'showlegend': True}]),
             ]
        ))],
        xaxis_title='Month',
        yaxis_title='Market Share (%)',
        title='Steam Market Share (AMD)',
        legend_title='Card Name:',
        margin=dict(l=250, r=0, t=100, b=100),
    )
    return fig


### FIGURE and line chart END

### FIGURE nvidia line chart START
def nvi_line():
    fig = go.Figure()
    # I LOVE REGEXS
    NVI = by_card.filter(regex='NVIDIA GeForce .*?')

    GT = by_card.filter(regex=('[^.*?](GT .*?)'))
    GT.insert(0, 'MONTH', Months, True)
    GT = GT.set_index(['MONTH'])

    GTX10 = NVI.filter(regex=('[^.*?](GTX 10.*?)'))
    GTX10.insert(0, 'MONTH', Months, True)
    GTX10 = GTX10.set_index(['MONTH'])

    M = NVI.filter(regex=('[^.*?](940M.*?)'))
    M.insert(0, 'MONTH', Months, True)
    M = M.set_index(['MONTH'])

    GTX16 = NVI.filter(regex=('[^.*?](GTX 16.*?)'))
    GTX16.insert(0, 'MONTH', Months, True)
    GTX16 = GTX16.set_index(['MONTH'])

    GTX6 = NVI.filter(regex=('[^.*?](GTX 6.*?)'))
    GTX6.insert(0, 'MONTH', Months, True)
    GTX6 = GTX6.set_index(['MONTH'])

    GTX7 = NVI.filter(regex=('[^.*?](GTX 7.*?)'))
    GTX7.insert(0, 'MONTH', Months, True)
    GTX7 = GTX7.set_index(['MONTH'])

    GTX9 = NVI.filter(regex=('[^.*?](GTX 9.*?)'))
    GTX9.insert(0, 'MONTH', Months, True)
    GTX9 = GTX9.set_index(['MONTH'])

    MX = NVI.filter(regex=('[^.*?](MX.*?)'))
    MX.insert(0, 'MONTH', Months, True)
    MX = MX.set_index(['MONTH'])

    RTX20 = NVI.filter(regex=('[^.*?](RTX 20.*?)'))
    RTX20.insert(0, 'MONTH', Months, True)
    RTX20 = RTX20.set_index(['MONTH'])

    RTX30 = NVI.filter(regex=('[^.*?](RTX 30.*?)'))
    RTX30.insert(0, 'MONTH', Months, True)
    RTX30 = RTX30.set_index(['MONTH'])

    fig.update_layout(
        width=1600,
        height=900,
        template='plotly_white',
        font=dict(size=20),
        autosize=True,
    )
    # FOR LOOPS (I WANT TO DIE)
    for col in GT.columns[:]:
        GT[col] = GT[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=GT.index,
                y=GT[col],
                name=col
            )
        )

    for col in GTX10.columns[:]:
        GTX10[col] = GTX10[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=GTX10.index,
                y=GTX10[col],
                name=col
            )
        )
    for col in M.columns[:]:
        M[col] = M[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=M.index,
                y=M[col],
                name=col
            )
        )
    for col in GTX16.columns[:]:
        GTX16[col] = GTX16[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=GTX16.index,
                y=GTX16[col],
                name=col
            )
        )
    for col in GTX6.columns[:]:
        GTX6[col] = GTX6[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=GTX6.index,
                y=GTX6[col],
                name=col
            )
        )
    for col in GTX7.columns[:]:
        GTX7[col] = GTX7[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=GTX7.index,
                y=GTX7[col],
                name=col
            )
        )
    for col in GTX9.columns[:]:
        GTX9[col] = GTX9[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=GTX9.index,
                y=GTX9[col],
                name=col
            )
        )
    for col in MX.columns[:]:
        MX[col] = MX[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=MX.index,
                y=MX[col],
                name=col
            )
        )
    for col in RTX20.columns[:]:
        RTX20[col] = RTX20[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=RTX20.index,
                y=RTX20[col],
                name=col
            )
        )
    for col in RTX30.columns[:]:
        RTX30[col] = RTX30[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=RTX30.index,
                y=RTX30[col],
                name=col
            )
        )

    # layout
    fig.update_layout(updatemenus=[go.layout.Updatemenu(
        active=0,
        x=0.55, y=1.11,
        buttons=list(
            [dict(label='ALL',
                  method='update',
                  args=[{'visible': [True, True, True, True, True, True, True, True, True, True, True, True,
                                     True, True, True, True, True, True, True, True, True, True, True, True,
                                     True, True, True, True, True, True, True, True, True, True, True, True,
                                     True, True, True, True, True, True, True, True, True, True, True, True,
                                     True, True, True, True, True, True, True, True, True, True]},
                        {'title': 'ALL',
                         'showlegend': True}]),
             dict(label='M Series',
                  method='update',
                  args=[{'visible': [False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, True, True, True, True, True, True, True, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False]},
                        {'title': 'M Series',
                         'showlegend': True}]),
             dict(label='GT',
                  method='update',
                  args=[{'visible': [True, True, True, True, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False]},
                        {'title': 'GT',
                         'showlegend': True}]),
             dict(label='GTX 6 Series',
                  method='update',
                  args=[{'visible': [False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, True,
                                     True, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False]},
                        {'title': 'GTX 6 Series',
                         'showlegend': True}]),
             dict(label='GTX 7 Series',
                  method='update',
                  args=[{'visible': [False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False,
                                     False, False, True, True, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False]},
                        {'title': 'GTX 7 Series',
                         'showlegend': True}]),
             dict(label='GTX 9 Series',
                  method='update',
                  args=[{'visible': [False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False,
                                     False, False, False, False, True, True, True, True, True, True,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False]},
                        {'title': 'GTX 9 Series',
                         'showlegend': True}]),
             dict(label='GTX 10 Series',
                  method='update',
                  args=[{'visible': [False, False, False, False, True, True, True, True, True, True,
                                     True, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False]},
                        {'title': 'GTX 10 Series',
                         'showlegend': True}]),
             dict(label='GTX 16 Series',
                  method='update',
                  args=[{'visible': [False, False, False, False, False, False, False, False, False, False, False,
                                     False, True, True, True, True, True, True,
                                     False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False]},
                        {'title': 'GTX 16 Series',
                         'showlegend': True}]),
             dict(label='RTX 20 Series',
                  method='update',
                  args=[{'visible': [False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, True,
                                     True, True, True, True, True, True, True, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False]},
                        {'title': 'RTX 20 Series',
                         'showlegend': True}]),
             dict(label='RTX 30 Series',
                  method='update',
                  args=[{'visible': [False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, True, True, True,
                                     True, True, True, True, True, True, True, True, True, True, True,
                                     True, True, True, True, True, True, True]},
                        {'title': 'RTX 30 Series',
                         'showlegend': True}]),

             ]
        ))],
        xaxis_title='Month',
        yaxis_title='Market Share (%)',
        title='Steam Market Share (Nvidia)',
        legend_title='Card Name:',
        margin=dict(l=250, r=0, t=100, b=100),
        width=1600,
        height=900,
        template='plotly_white',
        font=dict(size=20),
        autosize=True,
    )
    return fig


### FIGURE nvidia line chart END

### FIGURE intel line chart START
def int_line():
    INT = by_card.filter(regex=('(Intel.*?)'))

    # ROUND 3 REGEX WOOOOOOOOOOOOOOOOOOO
    Graphic = INT.filter(regex=('[^.*?](Graphics .*?)'))
    Graphic.insert(0, 'MONTH', Months, True)
    Graphic = Graphic.set_index(['MONTH'])

    fig = go.Figure()
    # FOR LOOPS (I WANT TO DIE)
    for col in Graphic.columns[1:]:
        Graphic[col] = Graphic[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=Graphic.index,
                y=Graphic[col],
                name=col
            )
        )

    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Market Share (%)',
        title='Steam Market Share (Intel)',
        legend_title='Card Name:',
        margin=dict(l=250, r=0, t=100, b=100),
        width=1600,
        height=900,
        template='plotly_white',
        font=dict(size=20),
        autosize=True,
    )

    return fig


### FIGURE intel line chart END

### WEBSITE header, nav and footer START
app.layout = html.Div([
    html.H1('GP4U - Data Visualization Representing Steam Market Shares for Video Cards'),
    dcc.Tabs(
        id="tabs",
        value='tab1',  # SETTING for DEFAULT TAB
        parent_className='tabs-css',
        className='tabs-container-css',
        children=[
            dcc.Tab(label='Market Share',  # EDIT Home tab!
                    value='tab1',
                    className='tab-css',
                    selected_className='tab-selected-css',
                    ),
            dcc.Tab(label='AMD',  # EDIT amd tab!
                    value='tab2',
                    className='tab-css',
                    selected_className='tab-selected-css',
                    ),
            dcc.Tab(label='NVIDIA',  # EDIT nvidia tab !
                    value='tab3',
                    className='tab-css',
                    selected_className='tab-selected-css',
                    ),
            dcc.Tab(label='Intel',  # EDIT intel tab!
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
    #    html.Div(id='vendor-graph', children=[
    #        html.Div([dcc.Graph(figure=vendor_share())], )
    #    ]),

    html.Div(id='footer', style={'font-family': 'Arial',
                                 'font-size': '15pt',
                                 'padding-left': '80px',
                                 'padding-bottom': '10px',
                                 'padding-top': '10px', }, children=[
        html.P('Visualization generated using Python, HTML and CSS. Leverages libraries from Plotly, Dash, and Panda.'),
        html.P('ICS 484 Data Visualization developed by University of Hawaii at Mānoa students:'),
        html.P(['Gunwook Baik ', html.A('(gbaik@hawaii.edu)', href='gbaik@hawaii.edu')]),
        html.P(['Zachary Chaikin ', html.A('zchaikin@hawaii.edu', href='zchaikin@hawaii.edu')]),
        html.P(['Samuel Chrisopher Roberts ', html.A('scrobert@hawaii.edu', href='scrobert@hawaii.edu')]),
        html.P(['Taylor Wong ', html.A('taylorsw@hawaii.edu', href='taylorsw@hawaii.edu')]),
        html.P(['Datafiles provided by the ', html.A('Steam Hardware & Software Survey', href='https://store.steampowered.com/hwsurvey/videocard/')]),
    ]),

])
### WEBSITE header, nav and footer END

### DASH footer START
venfig = vendor_share()  # Added as a workaround, costs performance


### WEBSITE Tab Switching Navigation Callback Logic START
@app.callback(Output('tab-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab1':
        return html.Div(id='vendor_graph', children=[
            html.H1(
                children='GP4U is a Data Visualization displaying Steam GPU (Graphics Processing Unit) or Video card usage over 5 months (June - October).',
                style={
                    'font-family': 'Arial',
                    'font-size': '20pt',
                    'padding-bottom': '10px',
                    'padding-left': '80px',
                    'padding-top': '10px',

                }
            ),

            html.Div(children='GP4U is practical for many applications. (1) Gamers. From the new individuals diving into gaming to the more advanced gamers, the visualization provides insight to determine what GPU to/not to choose amongst the '
                              'diverse market of GPU models. (2) Game Developers also benefit from the visualization by determining the GPU specs their player base(s) are using. Indie game developers are lately favorable towards higher-end '
                              'graphics. Using this visualization, developers can determine whether or not they should favor graphical intensity over performance, given the player base specs. (3) Companies and stock traders can also use this '
                              'visualization to watch and determine trends and make more accurate conclusions about a company and specific models from the data. Click on the tabs to explore the different Video Card Companies.', style={
                'font-family': 'Arial',
                'font-size': '15pt',
                'padding-left': '80px',
            }),

            dcc.Graph(figure=venfig),

            html.Div(
                children='The Overall Market Share Graph shows each video card company comparatively by their market share percentage over 5 months. NVIDIA is king with an average of 74.32% market share over 5 months. AMD comes in second '
                         'accounting for an average of 9.59% market share, while Intel has a market share of 5.85%. Other video card companies total a market share of 9.22%. Click on the legend to toggle the video card companies.',
                style={
                    'font-family': 'Arial',
                    'font-size': '15pt',
                    'padding-bottom': '15px',
                    'padding-left': '80px',
                    'padding-top': '10px',
                    'textAlign': 'left',
                    'width': '1808px',
                }),
        ])

    elif tab == 'tab2':
        return html.Div(id='amd_graph', children=[
            dcc.Graph(figure=amd_line()),

            html.Div(
                children='The AMD Market Share Graph shows each AMD video card model comparatively by market share percentage over five months. The highest average market share belongs to the AMD Radeon Graphics card at 1.59%, '
                         'while the lowest average market share percentage belongs to the AMD Radeon RX 6800 XT at 0.17%. Click on the dropdown menu to sort the AMD video card models by their model series, and click on the legend to toggle a set '
                         'of GPU model data points.',
                style={
                    'font-family': 'Arial',
                    'font-size': '15pt',
                    'padding-bottom': '15px',
                    'padding-left': '80px',
                    'padding-top': '10px',
                    'textAlign': 'left',
                    'width': '1808px',
                }),
        ])
    elif tab == 'tab3':
        return html.Div(id='nvi_graph', children=[
            dcc.Graph(figure=nvi_line()),

            html.Div(
                children='The NVIDIA Market Share Graph shows each NVIDIA video card model comparatively by market share percentage over five months. The highest average market share belongs to the NVIDIA GeForce GTX 1060 Graphics card at 7.06%, '
                         'while the lowest average market share percentage belongs to the NVIDIA GeForce GTX 980 at 0.18%. Click on the dropdown menu to sort the NVIDIA video card models by their model series, and click on the legend to toggle a '
                         'set of GPU model data points.',
                style={
                    'font-family': 'Arial',
                    'font-size': '15pt',
                    'padding-bottom': '15px',
                    'padding-left': '80px',
                    'padding-top': '10px',
                    'textAlign': 'left',
                    'width': '1808px',
                }),
        ])
    elif tab == 'tab4':
        return html.Div(id='int_graph', children=[
            dcc.Graph(figure=int_line()),

            html.Div(
                children='The Intel Market Share Graph shows each Intel video card model comparatively by market share percentage over five months. The highest average market share belongs to the Intel(R) UHD Graphics card at 1.24%, '
                         'while the lowest average market share percentage belongs to the Intel HD Graphics 630 at 0.23%. Click on the legend to toggle a set of GPU model data points.',
                style={
                    'font-family': 'Arial',
                    'font-size': '15pt',
                    'padding-bottom': '15px',
                    'padding-left': '80px',
                    'padding-top': '10px',
                    'textAlign': 'left',
                    'width': '1808px',
                }),
        ])


### WEBSITE Tab Switching Navigation Callback Logic END


if __name__ == '__main__':
    app.run_server(debug=True)
### DASH footer END
