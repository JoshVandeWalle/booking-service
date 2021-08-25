from flask import Flask, request
from flask_injector import FlaskInjector
from injector import inject
from src.api.reservation import ReservationRestService
from src.config.dependencies import configure
from flask_sqlalchemy import SQLAlchemy
from src.config.db_config import db
from src.api.error_handler import handle_error
from flask_cors import cross_origin
import traceback

def create_app():
    app = Flask(__name__)

    #app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@localhost:3306/booking'
    app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://admin:cst323gcu@cst323activity.cz6nq4gs34ua.us-west-1.rds.amazonaws.com/booking'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    return app

app = create_app()
db.init_app(app)

@app.route("/")
def home():
    return "Hello, Flask!"

@inject
@app.route("/bookings/reserve", methods = ['POST'])
@cross_origin()
def reserve_booking(service: ReservationRestService):
    return service.handle_reserve(request)

@inject
@app.route("/bookings", methods = ['GET'])
@cross_origin()
def get_bookings(service: ReservationRestService):
    with app.app_context():
        return service.handle_get()

@inject
@app.route("/bookings/edit", methods = ['PUT'])
@cross_origin()
def edit_booking(service: ReservationRestService):
    return service.handle_edit(request)

@inject
@app.route("/bookings/cancel", methods = ['DELETE'])
@cross_origin()
def cancel_booking(service: ReservationRestService):
    return service.handle_cancel(request)

@app.errorhandler(Exception)
def _(error):
    trace = traceback.format_exc()
    return handle_error(trace)

FlaskInjector(app=app, modules=[configure])