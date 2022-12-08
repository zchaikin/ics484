from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
from PIL import Image

app = Dash(__name__)

# DATASET import and prep START
# Function to separate GPUs into three datasets by company
def sep_by_brands(df):
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
gamebg = Image.open('data/releasedgames.png')
gamebg2 = gamebg.resize((1340, 690))
amd, intel, nvidia = sep_by_brands(data)
# DATASET import and prep END

# FIGURE Vendor Market Share START
def vendor_share():
    fig = go.Figure()
    name = reformat.columns.tolist()
    name.remove('MONTH')
    count = 0
    blankgpu = Image.open('data/blankgpu.png')
    blankgpu2 = blankgpu.resize((2080, 700))
    blankgpu3 = blankgpu2.transform(blankgpu2.size, Image.AFFINE, (1, 0, 0, 0, 1, 1))
    colorList = ['#FF5733', '#338AFF', '#5BFF33', '#C941C9']

    for i in reformat.columns[1:]:
        reformat[i] = reformat[i].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=reformat.MONTH,
                y=reformat[i],
                name=name[count],
                line=dict(color=colorList[count]),
                hoverlabel=dict(namelength=-1)
            )
        )
        count += 1

    fig.add_layout_image(
        dict(
            source=blankgpu3,
            xref='x', yref='y', x=-0.20, y=100, sizex=10, sizey=100, opacity=0.5, layer='below'
        )
    )
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Market Share (%)',
        yaxis_range=[0, 100],
        legend_title='Vendors',
        title='Steam Market Share by Vendor',
        width=1800,
        height=700,
        template='plotly_white',
        font=dict(
            size=20
        )
    )
    fig.update_traces(marker=dict(size=18), line=dict(width=8))
    return fig
# FIGURE Vendor Market Share END

# FIGURE amd line chart START
def amd_line():
    fig = go.Figure()

    # Filter data by AMD name
    AMD = by_card.filter(regex=('(AMD.*?)'))
    # F
    graphics = AMD.filter(regex=('[^.*?](Graphics.*?)'))
    graphics.insert(0, 'MONTH', Months, True)
    graphics = graphics.set_index(['MONTH'])

    RX = AMD.filter(regex=('[^Graphics](RX.*?)'))
    RX.insert(0, 'MONTH', Months, True)
    RX = RX.set_index(['MONTH'])

    for col in graphics.columns[:]:
        graphics[col] = graphics[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=graphics.index,
                y=graphics[col],
                name=col,
                hoverlabel=dict(namelength=-1)
            )
        )

    for col in RX.columns[:]:
        RX[col] = RX[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=RX.index,
                y=RX[col],
                name=col,
                hoverlabel=dict(namelength=-1)
            )
        )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', showgrid=True, gridwidth=1, gridcolor='Black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', showgrid=True, gridwidth=1, gridcolor='Black')

    fig.add_layout_image(
        dict(
            source=gamebg2,
            xref='x', yref='y', x=0, y=1.9, sizex=120, sizey=2, opacity=0.15, layer='below'
        )
    )
    fig.update_layout(
        width=1700,
        height=700,
        template='plotly_white',
        font=dict(size=20),
        autosize=True,
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
                  args=[{'visible': [True, True, True, True, True, False, False, False, False, False, False, False,
                                     False, False, False, False, False, False, False, False]},
                        {'title': 'Graphics',
                         'showlegend': True}]),
             dict(label='RX',
                  method='update',
                  args=[{'visible': [False, False, False, False, False, True, True, True, True, True, True, True, True,
                                     True, True, True, True, True, True, True, True]},
                        {'title': 'RX',
                         'showlegend': True}]),
             ]
        ))],
        xaxis_title='Month',
        yaxis_title='Market Share (%)',
        xaxis_range=[0, 4.2],
        yaxis_range=[0, 1.8],
        title='Steam Market Share (AMD)',
        legend_title='AMD GPUs:',
        margin=dict(l=250, r=0, t=100, b=100),
    )
    return fig
# FIGURE and line chart END

# FIGURE nvidia line chart START
def nvi_line():
    fig = go.Figure()
    # Filter through dataset for NVIDIA GeForce Series
    NVI = by_card.filter(regex='NVIDIA GeForce .*?')

    # Filter through dataset for NVIDIA GT Series
    GT = by_card.filter(regex=('[^.*?](GT .*?)'))
    GT.insert(0, 'MONTH', Months, True)
    GT = GT.set_index(['MONTH'])

    # Filter through dataset for NVIDIA GT Series
    GTX10 = NVI.filter(regex=('[^.*?](GTX 10.*?)'))
    GTX10.insert(0, 'MONTH', Months, True)
    GTX10 = GTX10.set_index(['MONTH'])

    # Filter through dataset for NVIDIA 940 Series
    M = NVI.filter(regex=('[^.*?](940M.*?)'))
    M.insert(0, 'MONTH', Months, True)
    M = M.set_index(['MONTH'])

    # Filter through dataset for NVIDIA GTX 16 Series
    GTX16 = NVI.filter(regex=('[^.*?](GTX 16.*?)'))
    GTX16.insert(0, 'MONTH', Months, True)
    GTX16 = GTX16.set_index(['MONTH'])

    # Filter through dataset for NVIDIA GTX 6 Series
    GTX6 = NVI.filter(regex=('[^.*?](GTX 6.*?)'))
    GTX6.insert(0, 'MONTH', Months, True)
    GTX6 = GTX6.set_index(['MONTH'])

    # Filter through dataset for NVIDIA GTX 7 Series
    GTX7 = NVI.filter(regex=('[^.*?](GTX 7.*?)'))
    GTX7.insert(0, 'MONTH', Months, True)
    GTX7 = GTX7.set_index(['MONTH'])

    # Filter through dataset for NVIDIA GTX 9 Series
    GTX9 = NVI.filter(regex=('[^.*?](GTX 9.*?)'))
    GTX9.insert(0, 'MONTH', Months, True)
    GTX9 = GTX9.set_index(['MONTH'])

    # Filter through dataset for NVIDIA GTX MX Series
    MX = NVI.filter(regex=('[^.*?](MX.*?)'))
    MX.insert(0, 'MONTH', Months, True)
    MX = MX.set_index(['MONTH'])

    # Filter through dataset for NVIDIA RTX 20 Series
    RTX20 = NVI.filter(regex=('[^.*?](RTX 20.*?)'))
    RTX20.insert(0, 'MONTH', Months, True)
    RTX20 = RTX20.set_index(['MONTH'])

    # Filter through dataset for NVIDIA RTX 30 Series
    RTX30 = NVI.filter(regex=('[^.*?](RTX 30.*?)'))
    RTX30.insert(0, 'MONTH', Months, True)
    RTX30 = RTX30.set_index(['MONTH'])

    # For loops for NVIDIA GT Series
    for col in GT.columns[:]:
        GT[col] = GT[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=GT.index,
                y=GT[col],
                name=col,
                hoverlabel=dict(namelength=-1)
            )
        )
    # For loops for NVIDIA GTX10 Series
    for col in GTX10.columns[:]:
        GTX10[col] = GTX10[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=GTX10.index,
                y=GTX10[col],
                name=col,
                hoverlabel=dict(namelength=-1)
            )
        )
    # For loops for NVIDIA M Series
    for col in M.columns[:]:
        M[col] = M[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=M.index,
                y=M[col],
                name=col,
                hoverlabel=dict(namelength=-1)
            )
        )
    # For loops for NVIDIA GTX16 Series
    for col in GTX16.columns[:]:
        GTX16[col] = GTX16[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=GTX16.index,
                y=GTX16[col],
                name=col,
                hoverlabel=dict(namelength=-1)
            )
        )
    # For loops for NVIDIA GTX6 Series
    for col in GTX6.columns[:]:
        GTX6[col] = GTX6[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=GTX6.index,
                y=GTX6[col],
                name=col,
                hoverlabel=dict(namelength=-1)
            )
        )
    # For loops for NVIDIA GTX7 Series
    for col in GTX7.columns[:]:
        GTX7[col] = GTX7[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=GTX7.index,
                y=GTX7[col],
                name=col,
                hoverlabel=dict(namelength=-1)
            )
        )
    # For loops for NVIDIA GTX9 Series
    for col in GTX9.columns[:]:
        GTX9[col] = GTX9[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=GTX9.index,
                y=GTX9[col],
                name=col,
                hoverlabel=dict(namelength=-1)
            )
        )
    # For loops for NVIDIA MX Series
    for col in MX.columns[:]:
        MX[col] = MX[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=MX.index,
                y=MX[col],
                name=col,
                hoverlabel=dict(namelength=-1)
            )
        )
    # For loops for NVIDIA RTX20 Series
    for col in RTX20.columns[:]:
        RTX20[col] = RTX20[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=RTX20.index,
                y=RTX20[col],
                name=col,
                hoverlabel=dict(namelength=-1)
            )
        )
    # For loops for NVIDIA RTX30 Series
    for col in RTX30.columns[:]:
        RTX30[col] = RTX30[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=RTX30.index,
                y=RTX30[col],
                name=col,
                hoverlabel=dict(namelength=-1)
            )
        )
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', showgrid=True, gridwidth=1, gridcolor='Black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', showgrid=True, gridwidth=1, gridcolor='Black')
    fig.update_layout(
        width=1700,
        height=700,
        template='plotly_white',
        font=dict(size=20),
        autosize=True,
    )
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
        legend_title='NVIDIA GPUs:',
        margin=dict(l=250, r=0, t=100, b=100),
        width=1880,
        height=700,
        xaxis_range=[0, 4.2],
        template='plotly_white',
        font=dict(size=20),
        autosize=True,
    )
    return fig
# FIGURE nvidia line chart END

# FIGURE intel line chart START
def int_line():
    INT = by_card.filter(regex=('(Intel.*?)'))
    Graphic = INT.filter(regex=('[^.*?](Graphics .*?)'))
    Graphic.insert(0, 'MONTH', Months, True)
    Graphic = Graphic.set_index(['MONTH'])

    fig = go.Figure()
    for col in Graphic.columns[1:]:
        Graphic[col] = Graphic[col].str.rstrip('%').astype('float')
        fig.add_trace(
            go.Scatter(
                x=Graphic.index,
                y=Graphic[col],
                name=col,
                hoverlabel=dict(namelength=-1)
            )
        )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', showgrid=True, gridwidth=1, gridcolor='Black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', showgrid=True, gridwidth=1, gridcolor='Black')
    fig.add_layout_image(
        dict(
            source=gamebg2,
            xref='x', yref='y', x=0, y=0.45, sizex=120, sizey=0.3, opacity=0.15, layer='below'
        )
    )
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Market Share (%)',
        title='Steam Market Share (Intel)',
        legend_title='Intel Integrated Graphics:',
        margin=dict(l=250, r=0, t=100, b=100),
        width=1600,
        height=700,
        xaxis_range=[0, 4.2],
        template='plotly_white',
        font=dict(size=20),
        autosize=True,
    )
    return fig
# FIGURE intel line chart END

# Website Tabs Layout
app.layout = html.Div([
    html.H1('GP4U - Data Visualization Representing Steam Market Shares for Video Cards'),
    dcc.Tabs(
        id="tabs",
        value='tab1',  # SETTING for DEFAULT TAB
        parent_className='tabs-css',
        className='tabs-container-css',
        style={'background-color': 'aliceblue'},
        children=[
            dcc.Tab(label='Market Share',  # EDIT Home tab!
                    value='tab1',
                    className='tab-css',
                    selected_className='tab-selected-css',
                    style={'background-color': 'ghostwhite'},
                    ),
            dcc.Tab(label='AMD',  # EDIT amd tab!
                    value='tab2',
                    className='tab-css',
                    selected_className='tab-selected-css',
                    style={'background-color': 'salmon'},
                    ),
            dcc.Tab(label='NVIDIA',  # EDIT nvidia tab !
                    value='tab3',
                    className='tab-css',
                    selected_className='tab-selected-css',
                    style={'background-color': 'lightgreen'},
                    ),
            dcc.Tab(label='Intel',  # EDIT intel tab!
                    value='tab4',
                    className='tab-css',
                    selected_className='tab-selected-css',
                    style={'background-color': 'lightskyblue'},
                    ),
        ]),
    html.Div(id='tab-content'),
    #    html.Div(id='vendor-graph', children=[
    #        html.Div([dcc.Graph(figure=vendor_share())], )
    #    ]),
])
# WEBSITE header, nav and footer END

# DASH footer START
venfig = vendor_share()

# Website Layout Tab Switching Navigation Callback Logic START
@app.callback(Output('tab-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab1':
        return html.Div(style={
            'background-color': 'ghostwhite',
        }
            , children=[
                html.Div(id='vendor_graph', children=[
                    html.H1(
                        children='GP4U is a Data Visualization displaying Steam GPU (Graphics Processing Unit) or Video card usage over 5 months (June - October).',
                        style={
                            'background-color': 'ghostwhite',
                            'font-family': 'Arial',
                            'font-size': '20pt',
                            'padding-left': '80px',
                            'padding-top': '15px',
                            'width': '1808px',
                        }
                    ),

                    html.Div(
                        children='GP4U visualizes data provided by Steam on what GPUs its users use. Visualizing the data offers valuable insight and information regarding the GPU market. For example, with gaming becoming more mainstream, '
                                 'less tech-savvy people can take advantage of the visualization to understand what GPUs they may want to purchase. Similarly, Game Developers can use the visualization to observe what GPUs the average gamer uses. '
                                 'Also, investors could follow this data to help figure out which companies are doing sufficiently and, by using it in conjunction with additional information, could determine future trends in the market.',
                        style={
                            'background-color': 'ghostwhite',
                            'font-family': 'Arial',
                            'font-size': '15pt',
                            'padding-left': '80px',
                            'width': '1808px',
                        }),

                    dcc.Graph(figure=venfig, style={'padding-bottom': '45px',
                                                    'padding-left': '80px',
                                                    'padding-top': '30px', }),

                    html.Div(
                        children='The Overall Market Share Graph shows each video card company comparatively by their market share percentage over 5 months. NVIDIA is king with an average of 74.32% market share over 5 months. AMD comes in second '
                                 'accounting for an average of 9.59% market share, while Intel has a market share of 5.85%. Other video card companies total a market share of 9.22%. Click on the legend to toggle the video card companies.',
                        style={
                            'font-family': 'Arial',
                            'font-size': '15pt',
                            'padding-bottom': '15px',
                            'padding-left': '80px',
                            'textAlign': 'left',
                            'width': '1808px',
                        }),
                    html.Div(id='footer', style={'background-color': 'ghostwhite',
                                                 'font-family': 'Arial',
                                                 'font-size': '15pt',
                                                 'padding-left': '80px',
                                                 'padding-bottom': '10px',
                                                 'padding-top': '25px', }, children=[
                        html.P('Visualization generated using Python, HTML and CSS. Leverages libraries from Plotly, Dash, and Panda.'),
                        html.P('ICS 484 Data Visualization developed by University of Hawaii at Mānoa students:'),
                        html.P(['Gunwook Baik ', html.A('(gbaik@hawaii.edu)', href='gbaik@hawaii.edu')]),
                        html.P(['Zachary Chaikin ', html.A('zchaikin@hawaii.edu', href='zchaikin@hawaii.edu')]),
                        html.P(['Samuel Chrisopher Roberts ', html.A('scrobert@hawaii.edu', href='scrobert@hawaii.edu')]),
                        html.P(['Taylor Wong ', html.A('taylorsw@hawaii.edu', href='taylorsw@hawaii.edu')]),
                        html.P(['Datafiles provided by the ', html.A('Steam Hardware & Software Survey', href='https://store.steampowered.com/hwsurvey/videocard/')]),
                    ]),
                ])])

    elif tab == 'tab2':
        return html.Div(style={
            'background-color': 'ghostwhite',
        }
            , children=[
                html.Div(id='amd_graph', children=[
                    dcc.Graph(figure=amd_line(), style={'padding-bottom': '15px',
                                                        'padding-left': '80px',
                                                        'padding-top': '30px', }),
                    html.Div(
                        children='The AMD Market Share Graph shows each AMD video card model comparatively by market share percentage over five months. The highest average market share belongs to the AMD Radeon Graphics card at 1.59%, '
                                 'while the lowest average market share percentage belongs to the AMD Radeon RX 6800 XT at 0.17%. Click on the dropdown menu to sort the AMD video card models by their model series, and click on the legend to toggle '
                                 'a set of GPU model data points.',
                        style={
                            'font-family': 'Arial',
                            'font-size': '15pt',
                            'padding-bottom': '15px',
                            'padding-left': '80px',
                            'padding-top': '10px',
                            'textAlign': 'left',
                            'width': '1808px',
                        }),
                    html.Div(id='footer2', style={'background-color': 'ghostwhite',
                                                  'font-family': 'Arial',
                                                  'font-size': '15pt',
                                                  'padding-left': '80px',
                                                  'padding-bottom': '10px',
                                                  'padding-top': '25px', }, children=[
                        html.P('Visualization generated using Python, HTML and CSS. Leverages libraries from Plotly, Dash, and Panda.'),
                        html.P('ICS 484 Data Visualization developed by University of Hawaii at Mānoa students:'),
                        html.P(['Gunwook Baik ', html.A('(gbaik@hawaii.edu)', href='gbaik@hawaii.edu')]),
                        html.P(['Zachary Chaikin ', html.A('zchaikin@hawaii.edu', href='zchaikin@hawaii.edu')]),
                        html.P(['Samuel Chrisopher Roberts ', html.A('scrobert@hawaii.edu', href='scrobert@hawaii.edu')]),
                        html.P(['Taylor Wong ', html.A('taylorsw@hawaii.edu', href='taylorsw@hawaii.edu')]),
                        html.P(['Datafiles provided by the ', html.A('Steam Hardware & Software Survey', href='https://store.steampowered.com/hwsurvey/videocard/')]),
                    ]),
                ])])
    elif tab == 'tab3':
        return html.Div(style={
            'background-color': 'ghostwhite',
        }
            , children=[
                html.Div(id='nvi_graph', children=[
                    dcc.Graph(figure=nvi_line(), style={'padding-bottom': '15px',
                                                        'padding-left': '80px',
                                                        'padding-top': '30px', }),
                    html.Div(
                        children='The NVIDIA Market Share Graph shows each NVIDIA video card model comparatively by market share percentage over five months. The highest average market share belongs to the NVIDIA GeForce GTX 1060 Graphics card at '
                                 '7.06%, while the lowest average market share percentage belongs to the NVIDIA GeForce GTX 980 at 0.18%. Click on the dropdown menu to sort the NVIDIA video card models by their model series, '
                                 'and click on the legend to toggle a set of GPU model data points.',
                        style={
                            'font-family': 'Arial',
                            'font-size': '15pt',
                            'padding-bottom': '15px',
                            'padding-left': '80px',
                            'padding-top': '10px',
                            'textAlign': 'left',
                            'width': '1808px',
                        }),
                    html.Div(id='footer3', style={'background-color': 'ghostwhite',
                                                  'font-family': 'Arial',
                                                  'font-size': '15pt',
                                                  'padding-left': '80px',
                                                  'padding-bottom': '10px',
                                                  'padding-top': '25px', }, children=[
                        html.P('Visualization generated using Python, HTML and CSS. Leverages libraries from Plotly, Dash, and Panda.'),
                        html.P('ICS 484 Data Visualization developed by University of Hawaii at Mānoa students:'),
                        html.P(['Gunwook Baik ', html.A('(gbaik@hawaii.edu)', href='gbaik@hawaii.edu')]),
                        html.P(['Zachary Chaikin ', html.A('zchaikin@hawaii.edu', href='zchaikin@hawaii.edu')]),
                        html.P(['Samuel Chrisopher Roberts ', html.A('scrobert@hawaii.edu', href='scrobert@hawaii.edu')]),
                        html.P(['Taylor Wong ', html.A('taylorsw@hawaii.edu', href='taylorsw@hawaii.edu')]),
                        html.P(['Datafiles provided by the ', html.A('Steam Hardware & Software Survey', href='https://store.steampowered.com/hwsurvey/videocard/')]),
                    ]),
                ])])
    elif tab == 'tab4':
        return html.Div(style={
            'background-color': 'ghostwhite',
        }
            , children=[
                html.Div(id='int_graph', children=[
                    dcc.Graph(figure=int_line(), style={'padding-bottom': '15px',
                                                        'padding-left': '80px',
                                                        'padding-top': '30px', }),
                    html.Div(
                        children='All Intel models listed are integrated graphics built into Intel CPUs, meaning these people do not own a GPU card. The Intel Market Share Graph shows each Intel graphics chip comparatively by market share '
                                 'percentage over five months. The highest average market share belongs to the Intel(R) UHD Graphics 620 at 0.58%, while the lowest average market share percentage belongs to the Intel HD Graphics 5500 at 0.21%. '
                                 'Click on the legend to toggle a set of GPU model data points.',
                        style={
                            'font-family': 'Arial',
                            'font-size': '15pt',
                            'padding-bottom': '15px',
                            'padding-left': '80px',
                            'padding-top': '10px',
                            'textAlign': 'left',
                            'width': '1808px',
                        }),
                    html.Div(id='footer4', style={'background-color': 'ghostwhite',
                                                  'font-family': 'Arial',
                                                  'font-size': '15pt',
                                                  'padding-left': '80px',
                                                  'padding-bottom': '10px',
                                                  'padding-top': '25px', }, children=[
                        html.P('Visualization generated using Python, HTML and CSS. Leverages libraries from Plotly, Dash, and Panda.'),
                        html.P('ICS 484 Data Visualization developed by University of Hawaii at Mānoa students:'),
                        html.P(['Gunwook Baik ', html.A('(gbaik@hawaii.edu)', href='gbaik@hawaii.edu')]),
                        html.P(['Zachary Chaikin ', html.A('zchaikin@hawaii.edu', href='zchaikin@hawaii.edu')]),
                        html.P(['Samuel Chrisopher Roberts ', html.A('scrobert@hawaii.edu', href='scrobert@hawaii.edu')]),
                        html.P(['Taylor Wong ', html.A('taylorsw@hawaii.edu', href='taylorsw@hawaii.edu')]),
                        html.P(['Datafiles provided by the ', html.A('Steam Hardware & Software Survey', href='https://store.steampowered.com/hwsurvey/videocard/')]),
                    ]),
                ])])
# Website Layout Tab Switching Navigation Callback Logic END

if __name__ == '__main__':
    app.run_server(debug=True)
# DASH footer END
