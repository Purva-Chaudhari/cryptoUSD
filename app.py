from flask import Flask, render_template, request, jsonify
from flask_caching import Cache 
import requests
import json
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

cache = Cache()

# Converter for USD to crypto and crypto to USD for Ethereum, Bitcoin and Litecoin

app = Flask(__name__)

app.config['CACHE_TYPE'] = 'simple'

cache.init_app(app)

    # Home page :
    # Select crypto to USD or USD to crypto
@app.route('/')
def index():
    return render_template('index.html')

    # Returns the equivalent value of the coin in USD.
@app.route('/get_usd/<float:amount>/<string:crypto>', methods=['GET', 'POST']) 
def get_usd(amount, crypto):
    if request.method == 'POST':
        try:
            from_crypto = crypto
            rate_all = convert(crypto)
            rate = float(rate_all[from_crypto]["usd"])
            result = rate * amount
            output = {
                'amount': amount,
                'currency': crypto,
                'in_usd': result
            }
            return jsonify(output)
        except Exception as e:
            return '<h1>Bad Request : {}</h1>'.format(e)
    else:
        return render_template('getusd.html')
    
    # Returns the amount of coin that can be purchased for the given USD.
@app.route('/get_crypto/<float:amount>/<string:crypto>', methods=['GET', 'POST']) 
def get_crypto(amount, crypto):
    if request.method == 'POST':
        try:

            amount = float(amount)
            to_crypto = crypto
            rate_all = convert(crypto)
            rate = float(rate_all[to_crypto]["usd"])
            result = (1/rate) * amount
            output = {
                'USD amount': amount,
                'in_crypto': result
            }
            return jsonify(output)
        except Exception as e:
            return '<h1>Bad Request : {}</h1>'.format(e)
    else:
        return render_template('getcrypto.html')

# Cache for storing the USD values
@cache.memoize(timeout=30)
#@cache.cached(timeout=30, key_prefix='convert')
def convert(crypto):
    # call coingecko api
    cg = CoinGeckoAPI() 
    out = cg.get_price(ids=crypto, vs_currencies='usd')
    return out

app.run(port=5000)