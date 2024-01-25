
from flask import Flask, render_template, request
import plotly.express as px
from dateutil.relativedelta import relativedelta
from datetime import date 
import pandas as pd
from jugaad_data.nse import stock_df
# import cufflinks as cf

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/graph', methods=['POST', 'GET'])
def show_graph():
    if request.method == 'POST':
        stock_symbol = request.form['stock_symbol']
        duration = request.form['duration']

        today = date.today()
        if duration == '1w':
            back = today - relativedelta(days=7)
        elif duration == '1m':
            back = today - relativedelta(months=1)
        elif duration == '6m':
            back = today - relativedelta(months=6)
        elif duration == '1y':
            back = today - relativedelta(years=1)
        elif duration == '5y':
            back = today - relativedelta(years=5)
        else:
            back = today - relativedelta(days=7)  # Default to 1 day

        stock_data = stock_df(symbol=stock_symbol, from_date=back, to_date=today, series="EQ")
        stock_data = stock_data.sort_values(by='DATE', ascending=True)

        fig = px.line(stock_data, x='DATE' , y='CLOSE', title=f'{stock_symbol} Stock Price ({duration.capitalize()})')
        
        fig.update_traces(hovertemplate='Date: %{x}<br> Close:%{y:.2f} ')
        fig.update_xaxes( title_text='Date',tickformat='%d %b %Y')
        fig.update_yaxes(title_text='Stock Price (INR)')
        

        fig.update_layout(
        template='plotly_dark',  # You can use other built-in templates like 'plotly', 'plotly_white', etc.
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Make the background color transparent
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Make the plot area background color transparent
    )
        return render_template('graph.html', plot=fig.to_html(), stock_symbol=stock_symbol, duration=duration)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
