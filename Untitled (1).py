#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import networkx as nx
import numpy as np
import plotly.graph_objs as go
import dash_bootstrap_components as dbc


#
#visualtiation 1
#3d network
#

# Use for animation rotation at the end
x_eye = -1.25
y_eye = 2
z_eye = 0.5

df = pd.read_csv('enron-v1.csv')

num_of_nodes = 31041
df["edge"] = list(zip(df["fromId"], df["toId"]))
df['date'] = pd.to_datetime(df['date'])
df['date'] = df['date'].dt.year

df_edge = df["edge"][:num_of_nodes]
df_edge = df_edge.to_frame()
df_edge['date'] = df['date']





#
#Visualization 2
#Pyramid
#

#Importing the DataFrame and setting date as index
df = pd.read_csv('enron-v1.csv')

df['date'] = pd.to_datetime(df['date'])
df['date'] = df['date'].dt.year
df = df.sort_values(by = ['date'])
df = df.set_index('date')


#Counting the sent and received mails and combining them in one DataFrame

sent_mails = df.groupby(['fromJobtitle', 'date']).count()
received_mails = df.groupby(['toJobtitle', 'date']).count()


df_count = pd.DataFrame()

df_count['sentCount'] = sent_mails['fromId']
df_count['receivedCount'] = received_mails['toId']

#Adding missing values

df_count.loc[('Unknown', 1998),:] = (0,0)
df_count.loc[('Vice President', 1998),:] = (0,0)
df_count.loc[('Manager', 1998),:] = (0,0)
df_count.loc[('Director', 1998),:] = (0,0)
df_count.loc[('Director', 1999),:] = (0,0)
df_count.loc[('President', 1998),:] = (0,0)
df_count.loc[('CEO', 1998),:] = (0,0)
df_count.loc[('CEO', 1999),:] = (0,0)
df_count.loc[('In House Lawyer', 1998),:] = (0,0)
df_count.loc[('In House Lawyer', 1999),:] = (0,0)
df_count.loc[('In House Lawyer', 2002),:] = (0,0)
df_count.loc[('Trader', 1998),:] = (0,0)

#Sorting the values accordingly

df_count = df_count.reindex([('Employee', 1998), ('Employee', 1999), ('Employee', 2000), ('Employee', 2001), ('Employee', 2002),
                            ('Unknown', 1998), ('Unknown', 1999), ('Unknown', 2000), ('Unknown', 2001), ('Unknown', 2002),
                            ('Vice President', 1998), ('Vice President', 1999), ('Vice President', 2000), ('Vice President', 2001), ('Vice President', 2002),
                            ('Manager', 1998), ('Manager', 1999), ('Manager', 2000), ('Manager', 2001), ('Manager', 2002),
                            ('Director', 1998), ('Director', 1999), ('Director', 2000), ('Director', 2001), ('Director', 2002),
                            ('President', 1998), ('President', 1999), ('President', 2000), ('President', 2001), ('President', 2002),
                            ('Trader', 1998), ('Trader', 1999), ('Trader', 2000), ('Trader', 2001), ('Trader', 2002),
                            ('CEO', 1998), ('CEO', 1999), ('CEO', 2000), ('CEO', 2001), ('CEO', 2002),
                            ('Managing Director', 1998), ('Managing Director', 1999), ('Managing Director', 2000), ('Managing Director', 2001), ('Managing Director', 2002),
                            ('In House Lawyer', 1998), ('In House Lawyer', 1999), ('In House Lawyer', 2000), ('In House Lawyer', 2001), ('In House Lawyer', 2002) ])
df_count = df_count.reset_index().set_index('fromJobtitle')


#
#dash app
#layout
#

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )




app.layout = html.Div([
        dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    html.Div([
        html.H1(
            ['Visualization GR36'],
            style={'font-weight': 'bold', 'margin-left': '2vw', 'margin-top': '1vw'}
        ),

        html.H2(
            html.A('Back to website', href='https://www.cloud36-visualization.nl/'),
            style={'margin-right': '2vw', 'margin-top': '1vw'}
        ),
    ], style={'display':'flex', 'flex-direction': 'row', 'justify-content': 'space-between', 'align-items': 'center', 'flex-wrap': 'wrap'}
    ),

    html.Div([
        html.Div([
            dcc.Graph(id = 'funnel-graph')
        ], style={'max-width': 'auto', 'margin-top': '2vw'}
        ),

        html.Div([
            html.Div(dcc.Graph(id='Graph')),
        ], style={'max-width': 'auto', 'margin-top': '2vw'}
        ),
    ], style={'display':'flex', 'flex-direction': 'row', 'justify-content': 'space-around', 'align-items': 'center', 'flex-wrap': 'wrap'}
    ),
        html.Div([
        html.H5(['Time Slider:'],
            style={'font-weight': 'bold', 'margin-left':'3vw', 'margin-top': '2vw'}
        ),

        html.Div([
            dcc.Slider(
                id='Time_Slider',
                marks={
                    1998: '1998',
                    1999: '1999',
                    2000: '2000',
                    2001: '2001',
                    2002: '2002',
                },
                step=1,
                min=1998,
                max=2002,
                value=1998,
                dots=True,
                disabled=False,
                updatemode='drag',
                included=True,
                vertical=False,
                verticalHeight=1000,
                className='None',
                tooltip={'always visible':False,
                        'placement':'bottom'},
            ),
        ], style={'margin-left':'2vw', 'margin-right':'2vw', 'margin-top': '1vw'}
        ),
    ]),

    html.Div([
        html.Div([
            dcc.Graph(id='Graph_2d')
        ], style={'max-width': 'auto', 'margin-top': '2vw'}
        ),


    ], style={'max-width': 'auto', 'margin-top': '2vw', 'display':'flex', 'flex-direction': 'row', 'justify-content': 'space-around', 'align-items': 'center', 'flex-wrap': 'wrap'}
    ),
], style={'margin-bottom': '3vw'}
)

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@app.callback(
    Output('funnel-graph','figure'),
    [Input('Time_Slider','value')]
)


def update_output_div(the_year):

    df_slider = sum_year(the_year)

    funnel = go.Figure()

    funnel.add_trace(go.Funnel(
    name = '# of sent mails',
    orientation = 'h',
    y = df_slider.index,
    x = df_slider['sentCount'],
    textinfo = 'value'
        )
    )

    funnel.add_trace(go.Funnel(
    name = '# of received mails',
    orientation = 'h',
    y = df_slider.index,
    x = df_slider['receivedCount'],
    textinfo = 'value'
        )
    )

    return(funnel)

@app.callback(
    Output('Graph','figure'),
    [Input('Time_Slider','value')]
)

def update_output_network(the_year):

    df_new = network_year(the_year)
    edge = df_new['edge']

    G = nx.Graph()

    #3d
    G.add_edges_from(edge)
    pos = nx.layout.spring_layout(G, dim=3)


    #3d
    for node in G.nodes:
        G.nodes[node]['pos'] = list(pos[node])

    pos=nx.get_node_attributes(G,'pos')


    #3d
    dmin=1
    ncenter=0
    for n in pos:
        x,y,z= pos[n]
        d=(x-0.5)**2+(y-0.5)**2+(z-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d
    p=nx.single_source_shortest_path_length(G,ncenter)


    #3d
    edge_trace = go.Scatter3d(
        x=[],
        y=[],
        z=[],
        line=dict(width=0.5,color='#888'),
        hoverinfo='none',
        mode='lines')

    #3d
    for edge in G.edges():
        x0, y0, z0 = G.nodes[edge[0]]['pos']
        x1, y1, z1 = G.nodes[edge[1]]['pos']
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])
        edge_trace['z'] += tuple([z0, z1, None])


    #3d
    node_trace = go.Scatter3d(
        x=[],
        y=[],
        z=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    #3d
    for node in G.nodes():
        x, y, z = G.nodes[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['z'] += tuple([z])

    #3d
    #add color to node points
    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color']+=tuple([len(adjacencies[1])])
        node_info = 'Name: ' + str(adjacencies[0]) + '<br># of connections: '+str(len(adjacencies[1]))
        node_trace['text']+=tuple([node_info])

    #3d
    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title='<br>Network Graph of '+str(len(df_new))+' rules',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    return(fig)

@app.callback(
    Output('Graph_2d','figure'),
    [Input('Time_Slider','value')]
)
def update_output_2dnetwork(the_year):

    df_new = network_year(the_year)
    edge = df_new['edge']


    G = nx.Graph()

    G.add_edges_from(edge)
    pos2d = nx.layout.spring_layout(G)


    dmin=1
    ncenter=0
    for n in pos2d:
        x,y=pos2d[n]
        d=(x-0.5)**2+(y-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d
    p=nx.single_source_shortest_path_length(G,ncenter)
    for node in G.nodes:
        G.nodes[node]['pos2d'] = list(pos2d[node])

    pos2d=nx.get_node_attributes(G,'pos2d')


    edge_trace_2d = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5,color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos2d']
        x1, y1 = G.nodes[edge[1]]['pos2d']
        edge_trace_2d['x'] += tuple([x0, x1, None])
        edge_trace_2d['y'] += tuple([y0, y1, None])


    node_trace_2d = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

     #2d
    for node in G.nodes():
        x, y = G.nodes[node]['pos2d']
        node_trace_2d['x'] += tuple([x])
        node_trace_2d['y'] += tuple([y])

    #2d
    #add color to node points
    for node, adjacencies in enumerate(G.adjacency()):
        node_trace_2d['marker']['color']+=tuple([len(adjacencies[1])])
        node_info = 'Name: ' + str(adjacencies[0]) + '<br># of connections: '+str(len(adjacencies[1]))
        node_trace_2d['text']+=tuple([node_info])

    #2d
    fig_2d = go.Figure(data=[edge_trace_2d, node_trace_2d],
                 layout=go.Layout(
                    title='<br>Network Graph of '+str(len(df_new))+' rules',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    return(fig_2d)

#2d highlight
@app.callback(
    Output('selected-data', 'children'),
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
     [Input('Graph_2d','selectedData')],
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
   )


def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        print(filename)
        return df == pd.read_csv(filename)


def display_selected_data(selectedData):
    num_of_nodes = len(selectedData['points'])
    text = [html.P('Num of nodes selected: '+str(num_of_nodes))]
    for x in selectedData['points']:
        print(x['text'])
    return text

def sum_year(the_year):

    if the_year == 1998:
        return df_count[df_count['date'] == 1998]
        return(fig)
    else:
        return df_count[df_count['date'] == the_year] + sum_year(the_year - 1)
        return(fig)

def network_year(the_year):

    return df_edge[df_edge['date'] <= the_year]
    return(fig)




if __name__ == '__main__':
    app.run_server(debug = False)


# In[23]:


df.update(pd.Series([4, 5, 6]))


# In[24]:


df

