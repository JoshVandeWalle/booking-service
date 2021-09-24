# dependencies
from flask import jsonify
from ..models.reservation import Reservation
from injector import inject
from ..business.reservation import ReservationBusinessServiceBase
from ..business.business_response import BusinessResponse
import traceback
from ..exceptions.validation_error import ValidationError
from ..logging.log import log
import json

"""
This class manages API behavior related to reservations
"""
class ReservationRestService:

    """
    The constructor used for constructor injection
    """
    @inject
    def __init__(self, service: ReservationBusinessServiceBase):
        # use dependency injection to inject the appropriate business service
        self.service = service

    """
    This method manages API behavior related to reserving a booking/reservation

    Parameters:

    self: the implicit object that allows access to class properties
    request: the http request including the reservation being made

    Returns: flask.wrappers.Response object containing a JSON including the response data, status code, and message
    """
    @log
    def handle_reserve(self, request):
        # instantiate and validate reservation
        try:
            # instantiate reservation from request json
            reservation = Reservation(None, request.json['name'], request.json['email'], request.json['datetime'], request.json['size'])
        # handle validation errors
        # handle missing json field
        except KeyError: 
            # return status code 400
            return jsonify(data=request.json, code="400", message="Invalid reservation")
        # handle invalid data in json 
        except ValidationError as e:
            # return status code 400 and specific validation error message
            return jsonify(data=request.json, code="400", message=e.message)
        # pass control to business layer to make the reservation
        res_data = self.service.reserve(reservation)
        # return status code 201
        return jsonify(data=res_data, code="201", message="Created")    
    
    """
    This method manages API behavior related to getting all reservations

    Parameters:

    self: the implicit object that allows access to class properties

    Returns: flask.wrappers.Response object containing a JSON including the response data, status code, and message
    """
    @log
    def handle_get(self):
        # pass control to business layer to get all bookings
        res_data = self.service.retrieve_all()
        # return status code 200
        return jsonify(data=res_data, code="200", message="OK")

    """
    This method manages API behavior related to editing a reservation

    Parameters:

    self: the implicit object that allows access to class properties
    request: the http request including the reservation being made
    """
    @log
    def handle_edit(self, request):
        # instantiate reservation and handle validation errors
        try:
            # instantiate reservation from request json
            reservation = Reservation(request.json['id'], request.json['name'], request.json['email'], request.json['datetime'], request.json['size'])
        # handle missing json field
        except KeyError: 
            # return status code 400
            return jsonify(data=request.json, code="400", message="Invalid reservation")
        # handle invalid json data
        except ValidationError as e:
            # return status code 400 and specific validation error message
            return jsonify(data=request.json, code="400", message=e.message)
        # pass contrl to business layer to make the edit
        res_data = self.service.edit(reservation)
        # if the edit was successful
        if res_data != None:
            # return status code 200
            return jsonify(data=res_data, code="200", message="OK")
        # the reservation could not be found
        else:
            # return status code 404
            return jsonify(data=None, code="404", message="Reservation not found")
    
    """
    This method manages API behavior related to canceling a reservation

    Parameters:

    self: the implicit object that allows access to class properties
    request: the http request including the reservation being made

    Returns: flask.wrappers.Response object containing a JSON including the response data, status code, and message
    """
    @log
    def handle_cancel(self, request):
        # instantiate reservation from the ID includied with the request's json
        reservation = Reservation(request.args['id'])
        # pass control to business layer to cancel the reservation
        res = self.service.cancel(reservation)
        # if the cancelation succeeed
        if res == BusinessResponse.OK:
            # return status code 200
            return jsonify(data=None, code="200", message="OK")
        # the reservation coud not be found
        else:
            # return status code 404
            return jsonify(data=None, code="404", message="Reservation not found")
