from flask import Flask, render_template, request
from flask_caching import Cache 
import requests
import json
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

cache = Cache()

# Converter for USD to crypto and crypto to USD for Ethereum, Bitcoin and Litecoin

def create_app():
    app = Flask(__name__)

    app.config['CACHE_TYPE'] = 'simple'

    cache.init_app(app)

    # Home page :
    # Select crypto to USD or USD to crypto
    @app.route('/')
    def index():
        return render_template('index.html')

    # Returns the equivalent value of the coin in USD.
    @app.route('/get_usd', methods=['GET', 'POST']) 
    def get_usd():
        if request.method == 'POST':
            try:
                amount = request.form['amount']
                amount = float(amount)
                from_crypto = request.form['from_c']
                rate_all = convert()
                rate = float(rate_all[from_crypto]["usd"])
                result = rate * amount
                return render_template('getusd.html', result=round(result, 2), amount=amount)
            except Exception as e:
                return '<h1>Bad Request : {}</h1>'.format(e)
        else:
            return render_template('getusd.html')
    
    # Returns the amount of coin that can be purchased for the given USD.
    @app.route('/get_crypto', methods=['GET', 'POST']) 
    def get_crypto():
        if request.method == 'POST':
            try:
                amount = request.form['amount']
                amount = float(amount)
                to_crypto = request.form['to_c']
                rate_all = convert()
                rate = float(rate_all[to_crypto]["usd"])
                result = (1/rate) * amount
                return render_template('getcrypto.html', result=round(result, 5), amount=amount, crypto=to_crypto)
            except Exception as e:
                return '<h1>Bad Request : {}</h1>'.format(e)
        else:
            return render_template('getcrypto.html')
        
    return app

# Cache for storing the USD values
@cache.cached(timeout=30, key_prefix='convert')
def convert():
    # call coingecko api
    cg = CoinGeckoAPI() 
    out = cg.get_price(ids=['bitcoin', 'litecoin', 'ethereum'], vs_currencies='usd')
    return out
