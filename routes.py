from market import app, db
from flask import render_template, redirect, url_for
from market.models import Item, User
from market.forms import RegisterForm
from datetime import date
from jugaad_data.nse import bhavcopy_save, bhavcopy_fo_save
import pandas as pd

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    # Download bhavcopy
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
    if form.validate_on_submit(): #means when clicked on the submit button, then check inside the scope of if
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            print(f'There was an error with creating a user: {err_msg}')

    return render_template('register.html', form=form)


# {'SYMBOL': 'SMARTLINK', 'SERIES': 'EQ', 'OPEN': 186.0, 'HIGH': 186.0, 'LOW': 176.2, 
#  'CLOSE': 177.05, 'LAST': 177.7, 'PREVCLOSE': 183.35, 'TOTTRDQTY': 25159, 'TOTTRDVAL': 4520201.35, 
#  'TIMESTAMP': '23-JAN-2024', 'TOTALTRADES': 623, 'ISIN': 'INE178C01020', 'Unnamed: 13': nan},