from flask import Flask, request, abort, g
from flask_caching import Cache
from flask_cors import CORS

from controller import mt5_controller
from controller import linebot_webhook_controller
from controller import login_controller
from controller import exness_controller
from controller import hello_controller

from controller.binance import balance_controller
from controller.binance import wallets_controller
from controller.binance import futures_controller

app = Flask(__name__)
CORS(app)

linebot_webhook_controller.cache.init_app(app, config={'CACHE_TYPE': 'redis'})

# registered controllers
app.register_blueprint(login_controller.bp)
app.register_blueprint(mt5_controller.bp)
app.register_blueprint(linebot_webhook_controller.bp)

app.register_blueprint(balance_controller.bp)
app.register_blueprint(wallets_controller.bp)
app.register_blueprint(futures_controller.bp)
app.register_blueprint(exness_controller.bp, url_prefix='/api/v1/exness')

app.register_blueprint(hello_controller.bp)

@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return {
        "code": -1,
        "msg": f"{err}",
        "data": []
    }, 200

# app.run()
