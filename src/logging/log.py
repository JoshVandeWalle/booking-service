# dependencies
import logging as logger
from flask import Response
import traceback
from ..business.business_response import BusinessResponse
from ..data.dao_response import DaoResponse
from ..exceptions.server_error import ServerError
from flask.wrappers import Response as ApiResponse
from ..exceptions.validation_error import ValidationError
import inspect

# configure logger
logger.basicConfig(filename='record.log', level=logger.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

"""
This method is a decorator used to implement interceptor logging.
All API facade, business service, and DAO methods (except constructors) should be decorated with the @log decorator
All method entry and exit is automatically logged for methods decorated with @log. This includes happy paths, warning paths, and 
exception paths.

Parameters:

method: the method being wrapped (should be a bound method)

Returns: the return value of the parameter method
"""
def log(method):

    """
    This nested method is used to add logging functionality to passed in methods with any parameters.
    
    Parameters:

    *args: Non-keyword arguments of the passed-in method
    *kwargs: Keyword arguments of the parameter method

    Returns: the return value of the parameter method
    """
    def inner(*args, **kwargs):
        # define the return value and initialize to None
        ret = None
        # log method entry
        logger.info("Entering " + get_qual_name(method) + "()")
        # use try/except to handle the logging of exceptions
        try:
            # call the passed-in method and capture its return value
            ret = method(*args, **kwargs) 
        # a model validation error has occurred
        except (KeyError, ValidationError):
            # log the validation error at the warning level
            logger.warn("Exiting " + get_qual_name(method) + "() with status code 400" )
            # return the value from the passed-in method
            return ret
        # handle all other exceptions
        except:
            # log the error and traceback
            logger.error("Exiting " + get_qual_name(method) + "() with exception: " + traceback.format_exc())
            # rase a server error to be caught by the global exception handler
            raise ServerError("Internal Error")
        # check for a warning path
        # any warning path return value must be added here
        if ret is None or ret is DaoResponse.MISSING or ret is BusinessResponse.NOT_FOUND or isinstance(ret, ApiResponse) and ret.json['code'].startswith("4"):
            # initalize result to an empty string
            # ths value will be used in the log statement
            result = ""
            # if the passed-in method returned None
            if (ret is None):
                # set the result value to indicate the outcome
                result = "None"
            # the passed-in method returned DaoResponse.MISSING
            elif (ret is DaoResponse.MISSING):
                # set the result value to indicate the outcome
                result = "DaoResponse.MISSING"
            # the passed-in method returned BusinessResponse.MISSING
            elif (ret is BusinessResponse.NOT_FOUND):
                # set the result value to indicate the outcome
                result = "BusinessResponse.NOT_FOUND"
            # if the passed-in method returned a json response with a status code of 4xx
            elif (isinstance(ret, ApiResponse) and ret.json['code'].startswith("4")):
                # set the result value to indicate the outcome
                result = "status code " + ret.json['code']
            else: 
                # by default use the word Failure will be used to describe the return value of the passed-in method
                result = "Failure"
            # log the method exit at the warning level and include the result variable
            logger.warn("Exiting " + get_qual_name(method) + "() with " + result)
        # log happy path outomce
        else:
            # log method exit
            logger.info("Exiting " + get_qual_name(method) + "() with OK")
        # return the return value of the passed-in method
        return ret
    # return the inner method
    return inner


"""
This method returns the qualifed name of a given method. 
Format is class.method and the method must be bound.
Only bound methods are acceptable parameters because only bound methods should decorated with @log which depends on this method

Parameters:

method: the specified method

Returns: the qualified name of the specified method
"""
def get_qual_name(method):
    # if this is a bound method
    if '.' in method.__qualname__ and inspect.getargspec(method).args[0] == 'self':
        # return the qualified name of the method
        return method.__qualname__