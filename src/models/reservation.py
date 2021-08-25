# dependencies
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from ..exceptions.validation_error import ValidationError
from ..config.db_config import db
import re

"""
This model class represents a reservation
"""
class Reservation(db.Model):
    # the unique database ID of the reservation
    id = db.Column(db.Integer, primary_key=True)
    # the name provided with the reservation
    name = db.Column(db.String(20), nullable=True)
    # the email address provided with the reservation
    email = db.Column(db.String(60))
    # the date and time of the reservation
    datetime = db.Column(db.DateTime)
    # the party size for the reservation
    size = db.Column(db.Integer)

    """
    This constructor method is used to initialize reservation properties

    Parameters:

    self: the implicit object that allows access to class properties
    id: the unique database ID of the reservation
    name: the name provided with the reservation
    email: the email address provided with the reservation
    datetime: # the date and time of the reservation
    size: the party size for the reservation
    """
    def __init__(self, id, name="UNPROVIDED", email="unprovided@unprovided.com", datetime="1998-06-14 13:12:00", size=1):
        # initialize class properties
        self.id = id
        self.name = name
        self.email = email
        self.datetime = datetime
        self.size = size
        # setup Flask_SQLAlchemy object for this models
        self.db = db
    
    """
    This method is used to validate the name associated with the reservation

    Parameters:

    self: the implicit object that allows access to class properties
    key: the json key
    value: the name value

    Returns: the name value if it is valid an exception will be raised if the value is invalid
    """
    @validates('name')
    def validate_name(self, key, value):
        # if the value is invalid due to its length
        if len(value) < 2 or len(value) > 20:
            # raise the appropriate error and provided a message explaing the error
            raise ValidationError("name must be 2-20 characters")
        # the value is valid, return it
        return value
    
    """
    This method is used to validate the email address associated with the reservation

    Parameters:

    self: the implicit object that allows access to class properties
    key: the json key
    value: the email address value

    Returns: the email address value if it is valid an exception will be raised if the value is invalid
    """
    @validates('email')
    def validate_email(self, key, value):
        # if the value is invalid because it is too long
        if len(value) > 60:
            # raise the appropriate error and provided a message explaing the error
            raise ValidationError("email field cannot exceed 60 characters")
        # define regular expression to validate email address format
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        # if the value is invalid because of its format
        if not re.search(regex, value):
            # raise the appropriate error and provided a message explaing the error
            raise ValidationError("Invalid email format")
        # the value is valid, return it
        return value
    
    """
    This method is used to validate the date and time associated with the reservation

    Parameters:

    self: the implicit object that allows access to class properties
    key: the json key
    value: the datetime value

    Returns: the datetime value if it is valid an exception will be raised if the value is invalid
    """
    @validates('datetime')
    def validate_datetime(self, key, value):
        # define a regular expression to validate the datetime format
        regex = "^(((\d{4})(-)(0[13578]|10|12)(-)(0[1-9]|[12][0-9]|3[01]))|((\d{4})(-)(0[469]|11)(-)(0[1-9]|[12][0-9]|30))|((\d{4})(-)(02)(-)(0[1-9]|[12][0-9]|2[0-8]))|(([02468][048]00)(-)(02)(-)(29))|(([13579][26]00)(-)(02)(-)(29))|(([0-9][0-9][0][48])(-)(02)(-)(29))|(([0-9][0-9][2468][048])(-)(02)(-)(29))|(([0-9][0-9][13579][26])(-)(02)(-)(29)))(\s)(([0-1][0-9]|2[0-4]):([0-5][0-9]):([0-5][0-9]))$"
        # if the value is invalid because of its format
        if not re.search(regex, value):
            # raise the appropriate error and provided a message explaing the error
            raise ValidationError("Invalid date format")
        # the value is valid, return it
        return value
    
    """
    This method is used to validate the party size associated with the reservation

    Parameters:

    self: the implicit object that allows access to class properties
    key: the json key
    value: the party size value

    Returns: the party size value if it is valid an exception will be raised if the value is invalid
    """
    @validates('size')
    def validate_size(self, key, value):
        # if the value is invalid
        if value < 0 or value >= 6:
            # raise the appropriate error and provided a message explaing the error
            raise ValidationError("Party size must be between 1 and 6")
        # the value is valid, return it
        return value
    

    """
    This method is used to serialize reservation objects

    Parameters:

    self: the implicit object that allows access to class properties

    Returns: a dictionary of reservation key/value pairs
    """
    def serialize(self):
        # return dictionary of reservation key/value pairs
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'datetime': self.datetime,
            'size': self.size
        }