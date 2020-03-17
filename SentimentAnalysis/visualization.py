import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import csv
import datetime
from wordcloud import WordCloud
import base64
from io import BytesIO
import matplotlib
import mood_analysis

matplotlib.use('Agg')

external_stylesheets1 = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

start_date = "2012-09-04"
end_date = "2013-08-01"
start_date_politics = "2013-01-01"
end_date_politics = "2013-02-01"
original_dates = pd.date_range(start_date, end_date, freq='7D', tz='UTC')
political_dates = pd.date_range(start_date_politics, end_date_politics, freq='7D', tz='UTC')
# print(political_dates)
original_dates_naive = []
political_dates_naive = []


def date_splits(start, end, l):
    dateformat = '%Y-%m-%d'
    s = datetime.datetime.strptime(start, dateformat)
    e = datetime.datetime.strptime(end, dateformat)
    d = s
    step = datetime.timedelta(days=7)
    while d < e:
        l.append(d.strftime(dateformat))
        d += step


date_splits(start_date, end_date, original_dates_naive)
date_splits(start_date_politics, end_date_politics, political_dates_naive)
# print(political_dates_naive)

# lower counts 182 205 224
# lower hover 109 256 194
# external_stylesheets=external_stylesheets
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("PEARL by Zijun Deng and Nuoshi Li", style={"textAlign": "center"}),
    html.Div([
        html.Div([
            # bar with selections, id and set of emotions
            dcc.Dropdown(
                id="userDropDown",
                options=[
                    {'label': '14874721', 'value': 'pulvereyes'},
                    {'label': '14396017', 'value': 'wkulhanek'},
                    {'label': 'Democrats', 'value': 'TheDemocrats'},
                    {'label': 'Republicans', 'value': 'GOP'}
                ],
                value='TheDemocrats',
                style=({"textAlign": "center", "width": "50%", "left": 20, 'font-family': 'Open Sans'})
            )
        ],
            style=({"width": "49%", 'display': 'inline-block', 'border-radios': '10px'})),
        html.Div([
            dcc.Checklist(
                id="emotionCheckList",
                options=[
                    {'label': 'anger', 'value': 'anger'},
                    {'label': 'disgust', 'value': 'disgust'},
                    {'label': 'joy', 'value': 'joy'},
                    {'label': 'surprise', 'value': 'surprise'},
                    {'label': 'anticipation', 'value': 'anticipation'},
                    {'label': 'fear', 'value': 'fear'},
                    {'label': 'sadness', 'value': 'sadness'},
                    {'label': 'trust', 'value': 'trust'}
                ],
                value=['anger', 'fear', 'anticipation', 'surprise', 'joy', 'sadness', 'trust', 'disgust'],
                labelStyle={'display': 'inline-block'}
            )
        ],
            id='radioitems',
            style={'width': '49%', 'float': 'right', 'display': 'inline-block', 'border-radios': '8px',
                   'font-family': 'Open Sans', 'font-size': '14'})
    ],
        style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(205, 205, 205)',
            'border-radius': '10px',
            'border-color': 'rgb(170, 170, 170)',
            'border-width': '3px',
            'padding': '10px 5px',
            'right': '30px'
        }
    ),
    html.Div([
        html.Div([
            html.Div([
                dcc.Graph(id='overview_vis', hoverData={'points': [{'x': '2013-01-26'}]},
                          clickData={'points': [{'x': '2013-01-26'}]})
            ], style={'width': '79%', 'display': 'inline-block', 'padding': '0 20'}),
            html.Div([
                dcc.Graph(id='vad_vis')
            ], style={'display': 'inline-block', 'width': '20%'})
        ]),
        html.Div([
            # html.H1("expand view", style={"textAlign": "center"}),
            dcc.Graph(id='expandview_vis', hoverData={'points': [{'x': '2013-01-26'}]},
                      clickData={'points': [{'x': '2013-01-26'}]})
        ])
        # html.Div([
        # html.H1("Mood view", style={"textAlign": "center"}),
        # dcc.Graph(id='moodview_vis')
        # ])
    ]),
    # left: scatter plot of words within the same time frame
    # right: set of tweets within the same time frame
    html.Div([
        html.Div([
            # html.H5("VAD", style={"textAlign": "center"}),
            html.Img(id='image')
        ], style={'width': '40%', 'display': 'inline-block', 'padding': '0 20'}),
        html.Div([
            # html.H5("tweets", style={"textAlign": "center"}),
            dcc.Graph(id='tweets_vis')
        ], style={'display': 'inline-block', 'width': '59%'})
    ])
])


@app.callback(
    dash.dependencies.Output('overview_vis', 'figure'),
    [dash.dependencies.Input('userDropDown', 'value')]
)
def update_overview(user):
    file = 'new_output_' + user + '.csv'
    # area = the amount of tweets
    df = pd.read_csv(file)
    df.sort_values(by=['DateTime'])
    # height by the number of tweets of the day
    fig = go.Figure()
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df.index = df['DateTime']
    dg = df.resample('D').count()
    # print(dg)
    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=dg['Original Tweet'],
        fill='tozeroy',
        mode='markers',
        name='Tweet Counts'))
    fig.update_layout(
        height=230,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=True
    )
    fig.update_layout(
        legend_orientation="h"
    )
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=2,
                         label="2m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig


@app.callback(
    dash.dependencies.Output('expandview_vis', 'figure'),
    [dash.dependencies.Input('userDropDown', 'value'),
     dash.dependencies.Input('emotionCheckList', 'value')]
)
def update_expandview(user, emotion):
    # on top of valance?
    file = 'new_output_' + user + '.csv'
    df = pd.read_csv(file)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df.sort_values(by=['DateTime'], inplace=True, ascending=False)
    # print(emotion)
    # height by the number of tweets of the day
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df.index = df['DateTime']
    dg = df.resample('D').count()
    # print(dg)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if 'sadness' in emotion:
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['sadness'],
            hovertext='sadness',
            hoverinfo='text+y',
            mode='lines',
            name='sadness',
            line=dict(width=0.2, color='rgb(127, 156, 200)'),
            stackgroup='one'
        ), secondary_y=False)
    if 'surprise' in emotion:
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['surprise'],
            hovertext='surprise',
            hoverinfo='text+y',
            mode='lines',
            name='surprise',
            line=dict(width=0.2, color='rgb(106, 164, 190)'),
            stackgroup='one'
        ), secondary_y=False)
    if 'fear' in emotion:
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['fear'],
            hovertext='fear',
            hoverinfo='text+y',
            mode='lines',
            name='fear',
            line=dict(width=0.2, color='rgb(134, 185, 126)'),
            stackgroup='one'
        ), secondary_y=False)
    if 'trust' in emotion:
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['trust'],
            hovertext='trust',
            hoverinfo='text+y',
            mode='lines',
            name='trust',
            line=dict(width=0.2, color='rgb(168, 200, 70)'),
            stackgroup='one'
        ), secondary_y=False)
    if 'joy' in emotion:
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['joy'],
            hovertext='joy',
            hoverinfo='text+y',
            mode='lines',
            name='joy',
            line=dict(width=0.2, color='rgb(240, 218, 106)'),
            stackgroup='one'
        ), secondary_y=False)
    if 'anticipation' in emotion:
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['anticipation'],
            hovertext='anticipation',
            hoverinfo='text+y',
            mode='lines',
            name='anticipation',
            line=dict(width=0.2, color='rgb(213, 159, 97)'),
            stackgroup='one'
        ), secondary_y=False)
    if 'anger' in emotion:
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['anger'],
            hovertext='anger',
            hoverinfo='text+y',
            mode='lines',
            name='anger',
            line=dict(width=0.2, color='rgb(226, 53, 88)'),
            stackgroup='one'
        ), secondary_y=False)
    if 'disgust' in emotion:
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['disgust'],
            hovertext='disgust',
            hoverinfo='text+y',
            mode='lines',
            name='disgust',
            line=dict(width=0.2, color='rgb(165, 50, 189)'),
            stackgroup='one'
        ), secondary_y=False)
    # based on time segments
    df['Date'] = pd.to_datetime(df['DateTime'], format='%m/%d/%y')
    dates = original_dates
    for i in range(len(dates) - 1):
        s = pd.to_datetime(dates[i])
        e = pd.to_datetime(dates[i + 1])
        mask = (pd.to_datetime(df['DateTime']) > s) & (pd.to_datetime(df['DateTime']) <= e)
        # print(df.loc[mask, 'DateTime'])
        fig.add_trace(go.Scatter(
            x=df.loc[mask, 'DateTime'],
            # x=df['DateTime'],
            y=dg['Original Tweet'],
            fill='tozeroy',
            mode='lines',
            name='Tweet Counts period' + str(i),
            hoverinfo='x+y',
            showlegend=False,
            line=dict(width=0.2, color='rgb(182, 105, 224)')
        ), secondary_y=True)
    fig.update_layout(
        height=300,
        width=1310,
        margin=dict(l=20, r=0, t=20, b=20),
        showlegend=True,
    )
    fig.update_yaxes(range=[-0.5, 1.1], secondary_y=False)
    fig.update_yaxes(range=[0, 20], secondary_y=True)
    # add rannge slider
    # reference: https://plot.ly/python/range-slider/
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=2,
                         label="2m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig


@app.callback(
    dash.dependencies.Output('image', 'src'),
    [dash.dependencies.Input('overview_vis', 'hoverData'),
     dash.dependencies.Input('userDropDown', 'value')])
def update_image_src(hoverData, user_id):
    hover_date = hoverData['points'][0]['x'][0:10]
    img = BytesIO()
    mood_analysis.word_cloud(hover_date, user_id).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


@app.callback(
    dash.dependencies.Output('vad_vis', 'figure'),
    [dash.dependencies.Input('overview_vis', 'clickData'),
     dash.dependencies.Input('userDropDown', 'value')])
def update_vad_vis(clickData, user_id):
    emotion_categories = ['anger', 'fear', 'anticipation', 'surprise', 'joy', 'sadness', 'trust', 'disgust']
    click_date = clickData['points'][0]['x'][0:10]
    keyword_dic = mood_analysis.find_keywords(click_date, user_id)
    # print (keyword_dic)
    keyword_df = pd.DataFrame.from_dict(keyword_dic, orient='index',
                                        columns=['Emotions', 'Valence', 'Arousal', 'Dominance'])
    keyword_df['Word'] = keyword_dic.keys()
    print(keyword_df)
    fig = px.scatter(keyword_df, x="Arousal", y="Valence",
                     hover_data=['Word', 'Emotions', 'Valence', 'Arousal', 'Dominance'])
    fig.update_layout(
        height=200,
        margin=dict(l=20, r=20, t=20, b=20),
    )
    fig.update_yaxes(range=[0, 1.01])
    fig.update_xaxes(range=[0, 1.01])
    return fig


@app.callback(
    dash.dependencies.Output('tweets_vis', 'figure'),
    [dash.dependencies.Input('overview_vis', 'hoverData'),
     dash.dependencies.Input('userDropDown', 'value')])
def update_tweet_vis(hoverData, user):
    # print(hoverData)
    hover_date = hoverData['points'][0]['x'][0:10]
    file = 'new_output_' + user + '.csv'
    df = pd.read_csv(file)
    df['Date'] = pd.to_datetime(df['DateTime'][0:10], format='%Y-%m-%d')
    dates = original_dates_naive
    s = 0
    for i in range(len(dates) - 1):
        if datetime.datetime.strptime(dates[i], '%Y-%m-%d') <= pd.to_datetime(hover_date):
            s = i
    mask = (pd.to_datetime(df['DateTime']) > dates[s]) & (pd.to_datetime(df['DateTime']) <= dates[s + 1])
    mood = mood_analysis.find_mood(hover_date, user)
    fig = go.Figure(
        data=go.Table(
            header=dict(values=['DateTime', 'Original Tweet', 'Mood']),
            cells=dict(values=[df.loc[mask, 'DateTime'], df.loc[mask, 'Original Tweet'], mood])
        )
    )
    fig.update_layout(
        height=400
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8800)
