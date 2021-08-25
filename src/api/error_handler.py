# dependencies
from flask import jsonify

"""
This method handles any error that might occur in the service

Parameters:

trace: the error trace which is included in the response message for development environments

Returns: flask.wrappers.Response object containing a JSON including the response data, status code, and message
"""
def handle_error(trace):
    return jsonify(data=None, code="500", message="Internal error: " + trace)