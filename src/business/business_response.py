# dependencies 
import enum

"""
This enumeration class defines business layer responses to method calls.
Responses are based on HTTP status codes.
"""
class BusinessResponse(enum.Enum):
    # define responses
    # OK response signifies that an operation succeeded
    OK = 200
    # CREATED response indicates that a nw record was created
    CREATED = 201
    # NOT_FOUND response indicates that a requested record does not exist
    NOT_FOUND = 404