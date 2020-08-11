import os
from flask import Flask
import plotly.graph_objects as go
import plotly.express as px
from utils import fetch_data, build_model
import pandas as pd

if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.exists('models'):
    os.makedirs('models')

# Instantiate an app
app = Flask(__name__)


@app.route('/')
def home():
    return 'Use the following endpoint: /data/tickername OR /plot/tickername'


@app.route('/data/<tickername>')
def data(tickername):
    data = fetch_data(tickername)
    # data.to_csv(f'data/{tickername}.csv')
    return data.reset_index().to_html()


@app.route('/plot/<tickername>')
def plot(tickername):
    data = fetch_data(tickername).reset_index()
    # data = pd.read_csv(f'data/{tickername}.csv')
    fig = go.Figure([go.Scatter(x=data['Date'], y=data['Close'])])
    return fig.to_html()


@app.route('/forecast/<tickername>/<steps>')
def forecast(tickername, steps):
    model = build_model(tickername)
    fcast = model.forecast(int(steps))
    return str(fcast[0])


@app.route('/forecast_plot/<tickername>/<steps>')
def forecast_plot(tickername, steps):
    data = fetch_data(tickername).reset_index()
    data['Type'] = 'HISTORICAL'
    model = build_model(tickername)
    fcast = model.forecast(int(steps))
    new_series = pd.date_range(data['Date'].iloc[-1], periods=int(steps))
    fcast_df = pd.DataFrame({'Date': new_series,
                             'Close': fcast[0],
                             'Type': 'FORECAST'})
    final_df = pd.concat([data[['Date', 'Close', 'Type']], fcast_df])
    fig = px.line(final_df, x='Date', y='Close', color='Type')
    # fig = go.Figure([go.Scatter(x=data['Date'], y=data['Close'])])
    # fig.add_trace(go.Scatter(x=fcast['Date'], y=fcast[0]))
    return fig.to_html()

    # return 'you should have a plot of the data + forecast here'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
