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
