from flask import Flask, render_template, request, redirect, url_for, flash, session, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dateutil.relativedelta import relativedelta
import plotly.express as px
from datetime import date, datetime
from jugaad_data.nse import bhavcopy_save, stock_df, index_df
import pandas as pd
import requests
import csv
from jugaad_data.nse import NSELive
n = NSELive()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key
NEWS_API_KEY = '737401ce7fb44b42b952c278fb01ebf0'
# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    name_user = db.Column(db.String(100), nullable=False)
    email_address = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(100), nullable=False)
    user_data = db.relationship('UserData', backref='user', lazy=True)

class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Add fields for user-specific data, e.g., user_dashboard_content, etc.

# Initialize Database within Application Context
with app.app_context():
    db.create_all()



@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

# ------------Working login and registration page from the starter code ------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name_user = request.form['name']
        email_address = request.form['email_address']
        mobile = request.form['mobile']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, password_hash=hashed_password, name_user=name_user, email_address=email_address, mobile=mobile)
        db.session.add(new_user)
        db.session.commit()

        new_user_data = UserData(user=new_user)
        db.session.add(new_user_data)
        db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('just_login'))

    return render_template('register.html')


@app.route('/loginpage')
def just_login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_page():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        session['username'] = user.username
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('just_login'))

first_write = False
toppers_found = False

def write_dict_to_csv(data, file_path, write_header=False):
    fieldnames = ['symbol', 'open', 'close', 'pChange', 'change', 'lastPrice']
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        for row in data:
            writer.writerow(row)

def make_toppers(file_path):
    global first_write
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)
        second_column_index = 2
        for row in csv_reader:
            if len(row) > 1:
                element = row[second_column_index]
                print(element)
                q = n.stock_quote(element)
                q = q['priceInfo']
                q= {'symbol' : element,
                    'open': q['open'],
                    'close': q['close'],
                    'pChange': round(q['pChange'], 3),
                    'change': round(q['change'], 3),
                    'lastPrice': q['lastPrice']
                    }
                if not first_write :
                    write_dict_to_csv([q], 'toppers_data.csv', write_header=True)
                    first_write=True
                else:
                    write_dict_to_csv([q], 'toppers_data.csv', write_header=False)
                # print(q)
# Read the CSV file into a Pandas DataFrame
    df = pd.read_csv('toppers_data.csv')
# Sort the DataFrame based on the 'pChange' column in descending order
    df_sorted = df.sort_values(by='pChange', ascending=False)
# Write the sorted DataFrame back to the CSV file
    df_sorted.to_csv('toppers_data.csv', index=False)

@app.route('/dashboard')
def dashboard():
    global toppers_found
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        user_data = user.user_data  # Modify this based on your data structure
        if not toppers_found:
            make_toppers('nifty50list.csv')
            toppers_found = True
        # Read top gainers and top losers data from the CSV file
        topers_df = pd.read_csv('toppers_data.csv')
        top_gainers = topers_df.iloc[:3].to_dict(orient='records')
        top_losers = topers_df.iloc[-3:].to_dict(orient='records')
        index_data = index_df(symbol="NIFTY 50", from_date=date(2023,1,1),to_date=date(2024,1,30))
        fig = px.line(index_data, x='HistoricalDate', y='CLOSE', title='NIFTY 50 Index')
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Make background transparent
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Make plot area transparent
            # showgrid=False,  # Hide grid lines
            xaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=30 * 24 * 3600 * 1000,  # 1 month in milliseconds
                tickformat='%d %b %Y',
            ),
            yaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=400,  # Increase ticks every 2000 units on the y-axis
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            # xaxis_showgrid=False,  # Hide x-axis grid lines
            # yaxis_showgrid=False,  # Hide y-axis grid lines
            yaxis_gridcolor='rgba(0, 0, 0, 0)',
            xaxis_gridcolor='rgba(0, 0, 0, 0)',
        )
        fig.update_yaxes(title_text='VALUE')
        fig.update_xaxes(title_text='DATE')

        graph_html = fig.to_html(full_html=False)
        return render_template('dashboard.html', username=session['username'], user_data=user_data, top_gainers=top_gainers, top_losers=top_losers,graph_html=graph_html)
    else:
        flash('Please log in to access the dashboard.')
        return redirect(url_for('just_login'))

@app.route('/graph', methods=['POST', 'GET'])
def show_graph():
    if request.method == 'POST':
        # stock_symbols = request.form['stock_symbol'].split(',')  # Split symbols by comma
        duration = request.form['duration']
        stock_symbols_input = request.form['stock_symbol']
        stock_symbols = [symbol.strip() for symbol in stock_symbols_input.split(',')] 
        # additional_stock = request.form.get('additional_stock')
        stock_info=request.form['stock_data']
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
            combined_data = pd.merge(combined_data, stock_data[['DATE', stock_info]].rename(columns={stock_info: symbol}),how='left', on='DATE')
        # combined_data=combined_data.interpolate
        # combined_data['DATE'] = pd.to_datetime(combined_data['DATE'])  # Ensure 'DATE' column is in datetime format
        combined_data = combined_data.set_index('DATE').interpolate().reset_index()
        fig = px.line(combined_data, x='DATE', y=combined_data.columns[1:], title=f'Stock {stock_info} ({duration.capitalize()})')
        
        fig.update_traces(hovertemplate='Date: %{x}<br>' + f'{stock_info}:' + ' %{y:.2f} ')
        fig.update_xaxes(title_text='Date', tickformat='%d %b %Y')
        # fig.update_yaxes(title_text='Stock Price (INR)')
        if stock_info == "VOLUME":
            fig.update_yaxes(title_text='STOCK VOLUME')
        elif stock_info == "VALUE":
            fig.update_yaxes(title_text='STOCK VALUE ')
        elif stock_info == "NO. OF TRADES":
            fig.update_yaxes(title_text=' No. OF TRADES')
        else:
            fig.update_yaxes(title_text='Stock Price (INR)')

        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
        )

        return render_template('graph.html', plot=fig.to_html(), stock_symbols=stock_symbols, duration=duration)

def month_name(a):
    if (a==1):
        return "Jan"
    if (a==2):
        return "Feb"
    if (a==3):
        return "Mar"
    if (a==4):
        return "Apr"
    if (a==5):
        return "May"
    if (a==6):
        return "Jun"
    if (a==7):
        return "Jul"
    if (a==8):
        return "Aug"
    if (a==9):
        return "Sep"
    if (a==10):
        return "Oct"
    if (a==11):
        return "Nov"
    if (a==12):
        return "Dec"
changes_made = False

def change_csv(file_name):
    global changes_made
    if not changes_made:
        with open(file_name, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            rows = list(csv_reader)
        rows_to_remove = rows[1:93+1]
        del rows[1:93+1]
        rows.extend(rows_to_remove)
        with open(file_name, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(rows)
        changes_made = True

@app.route('/market')
def market_page():
    if 'user_id' in session:
        global changes_made
        today = datetime.now()
        dd, mm, yyyy = today.day, today.month, today.year
        df = stock_df(symbol="SBIN", from_date=date(2024,1,25),
                    to_date=date(yyyy,mm,dd), series="EQ")
        last_day = df.iloc[0]['DATE']
        month, day, year = last_day.month, last_day.day, last_day.year
        name_month = month_name(month)
        file_name = 'cm'+str(day)+name_month+str(year)+'bhav.csv'
        bhavcopy_save(date(year,month,day), "./")

        if not changes_made:
            change_csv(file_name)
        
        df = pd.read_csv(file_name)
        columns_to_keep = ['SYMBOL', 'OPEN', 'HIGH','LOW','CLOSE','SERIES']
        df = df[columns_to_keep]

        items = df.to_dict(orient='records')
        
        return render_template('market.html', items=items, username = session['username'])
    else:
        flash('Please log in to view user details.')
        return render_template(url_for('just_login'))
    

@app.route('/get_news')
def get_news():
    endpoint = 'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': NEWS_API_KEY,
        'category': 'business',
        'country': 'in',  # Adjust country code as needed
    }

    response = requests.get(endpoint, params=params)
    news_data = response.json()

    # Extract relevant data from the response, adjust as needed
    articles = news_data.get('articles', [])

    return jsonify(articles)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('just_login'))

@app.route('/stocks')
def stocks_page():
    if 'user_id' in session:
        
        return render_template('comparestocks.html', username = session['username'])
    else:
        flash('Please log in to view user details.')
        return render_template(url_for('just_login'))


@app.route('/user_details')
def user_details():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        user_data = user.user_data
        return render_template('user_details.html', username = session['username'],name_user=user.name_user, email_address=user.email_address,mobile=user.mobile)
    else:
        flash('Please log in to view user details.')
        return redirect(url_for('login.html'))


# -------------Login page and registration page using forms ----------------

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired

class RegisterForm(FlaskForm):
    username = StringField(label='', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='', validators=[DataRequired()])
    password1 = PasswordField(label='', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='', validators=[ DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='Enter your Username / Email Address', validators=[Length(min=2,max=30), DataRequired()])
    password = PasswordField(label='Enter your password', validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label='Login')

@app.route('/register2', methods=['GET','POST'])
def register_page2():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email_address = form.email_address.data
        password = form.password1.data
        new_user = User(username,password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('login_page2'))

    return render_template('register2.html', form=form)

def check_password(plaintext_password, stored_password):
    return plaintext_password == stored_password

@app.route('/login2')
def login_page2():
    form=LoginForm()
    username = form.username.data
    password = form.password.data
    check_user = User.query.filter_by(username).first()
    new_password = check_user.password_hash
    if check_user and check_password(new_password,password):
        session['user_id'] = check_user.id
        session['username'] = check_user.username
        return redirect(url_for('dashboard_page'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('index'))
    # return render_template('login.html', form=form)

@app.route('/dashboard2')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/filter')
def filterpage():
    if 'user_id' in session:

        return render_template('filter.html',username=session['username'])
    else:
        flash('Please log in to access the dashboard.')
        return redirect(url_for('just_login'))
    

import atexit
import os

# The file path you want to delete
file_pa = "toppers_data.csv"
def get_csv_name():
    today = datetime.now()
    dd, mm, yyyy = today.day, today.month, today.year
    df = stock_df(symbol="SBIN", from_date=date(2024,1,25),
                to_date=date(yyyy,mm,dd), series="EQ")
    last_day = df.iloc[0]['DATE']
    month, day, year = last_day.month, last_day.day, last_day.year
    name_month = month_name(month)
    file_name = 'cm'+str(day)+name_month+str(year)+'bhav.csv'
    return file_name

market_file = get_csv_name()

# Function to delete the file
def cleanup():
    try:
        os.remove(file_pa)
        print(f"File '{file_pa}' deleted successfully.")
    except FileNotFoundError:
        print(f"File '{file_pa}' not found.")

def cleanup1():
    try:
        os.remove(market_file)
        print(f"File '{market_file}' deleted successfully.")
    except FileNotFoundError:
        print(f"File '{market_file}' not found.")


# Register the cleanup function to be called at program exit
atexit.register(cleanup)
atexit.register(cleanup1)

if __name__ == '__main__':
    app.run(debug=True)
