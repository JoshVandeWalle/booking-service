# dependencies
import enum

"""
This enumeration class defines data layer responses to method calls.
Responses indicate the outcome of database queries.
"""
class DaoResponse(enum.Enum):
    # define responses
    # the SUCCESS response indicates a successfu query
    SUCCESS = 'SUCCESS'
    # the MISSING response indicates that a required record could not be found in the database
    MISSING = 'MISSING'