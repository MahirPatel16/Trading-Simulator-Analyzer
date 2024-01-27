from market import app, db
from flask import  render_template, redirect, url_for, flash, jsonify, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm
from dateutil.relativedelta import relativedelta
import plotly.express as px

from datetime import date
from jugaad_data.nse import bhavcopy_save, bhavcopy_fo_save, stock_df
import pandas as pd
import requests

NEWS_API_KEY = '737401ce7fb44b42b952c278fb01ebf0'

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')

@app.route('/graph', methods=['POST', 'GET'])
def show_graph():
    if request.method == 'POST':
        # stock_symbols = request.form['stock_symbol'].split(',')  # Split symbols by comma
        duration = request.form['duration']
        stock_symbols_input = request.form['stock_symbol']
        stock_symbols = [symbol.strip() for symbol in stock_symbols_input.split(',')] 
        # additional_stock = request.form.get('additional_stock')

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

        combined_data = pd.DataFrame({'DATE': pd.date_range(start=back, end=today)})

        for symbol in stock_symbols:
            stock_data = stock_df(symbol=symbol, from_date=back, to_date=today, series="EQ")
            stock_data = stock_data.sort_values(by='DATE', ascending=True)

            # Merge the data into the combined DataFrame using DATE as the key
            combined_data = pd.merge(combined_data, stock_data[['DATE', 'CLOSE']].rename(columns={'CLOSE': symbol}),how='left', on='DATE')
        # combined_data=combined_data.interpolate
        # combined_data['DATE'] = pd.to_datetime(combined_data['DATE'])  # Ensure 'DATE' column is in datetime format
        combined_data = combined_data.set_index('DATE').interpolate().reset_index()
        fig = px.line(combined_data, x='DATE', y=combined_data.columns[1:], title=f'Stock Prices ({duration.capitalize()})')
        
        fig.update_traces(hovertemplate='Date: %{x}<br> Close:%{y:.2f} ')
        fig.update_xaxes(title_text='Date', tickformat='%d %b %Y')
        fig.update_yaxes(title_text='Stock Price (INR)')

        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
        )

        return render_template('graph.html', plot=fig.to_html(), stock_symbols=stock_symbols, duration=duration)

@app.route('/market')
def market_page():
    # Download bhavcopy
    # today_new = datetime.now()
    # yesterday = today_new - relativedelta(days=1)
    # one_year_ago = yesterday - relativedelta(years=1)
    # to_day, to_month, to_year = yesterday.day, yesterday.month, yesterday.year
    # from_day, from_month, from_year = one_year_ago.day, one_year_ago.month, one_year_ago.year

    bhavcopy_save(date(2024,1,23), "./")
    file_path = 'cm23Jan2024bhav.csv'
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(file_path)
    columns_to_keep = ['SYMBOL', 'OPEN', 'HIGH','LOW','CLOSE','SERIES']
    df = df[columns_to_keep]
    items = df.to_dict(orient='records')
    # items = [
    #     {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
    #     {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
    #     {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    # ]
    return render_template('market.html', items=items)

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/get_news')
def get_news():
    endpoint = 'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': NEWS_API_KEY,
        'category': 'business',
        'country': 'us',  # Adjust country code as needed
    }

    response = requests.get(endpoint, params=params)
    news_data = response.json()

    # Extract relevant data from the response, adjust as needed
    articles = news_data.get('articles', [])

    return jsonify(articles)
# {'SYMBOL': 'SMARTLINK', 'SERIES': 'EQ', 'OPEN': 186.0, 'HIGH': 186.0, 'LOW': 176.2, 
#  'CLOSE': 177.05, 'LAST': 177.7, 'PREVCLOSE': 183.35, 'TOTTRDQTY': 25159, 'TOTTRDVAL': 4520201.35, 
#  'TIMESTAMP': '23-JAN-2024', 'TOTALTRADES': 623, 'ISIN': 'INE178C01020', 'Unnamed: 13': nan},