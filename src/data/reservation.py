# dependencies
from abc import ABC, abstractmethod
from ..models.reservation import Reservation
from .dao_response import DaoResponse
from sqlalchemy import exc
from ..exceptions.database_error import DatabaseError
from ..logging.log import log

"""
This abstract class is used to define the API that reservation DAO objects should implement
"""
class ReservationDaoBase(ABC):

    """
    This constructor method is used to configure injected dependencies for the DAO

    Parameters:

    self: the implicit object that allows access to class properties
    """
    def __init__(self):
        pass

    """
    This method creates a reservation record

    Parameters:

    self: the implicit object that allows access to class properties
    reservation: the reservation to create

    Returns: None
    """
    @abstractmethod
    def create(self, reservation):
        pass

    """
    This method selects all reservation records

    Parameters:

    self: the implicit object that allows access to class properties

    Returns: a list of all reservation records
    """
    @abstractmethod
    def read_all(self):
        pass

    """
    This method updates a reservation record

    Parameters:

    self: the implicit object that allows access to class properties
    reservation: the reservation to update along with the updated values

    Returns: a Reservation model representing the updated record or None if the record couldn't be found
    """
    @abstractmethod
    def update(self, reservation):
        pass

    """
    This method deletes a reservation record

    Parameters:

    self: the implicit object that allows access to class properties
    reservation: the reservation to delete

    Returns: the appropriate DAOResponse enumeration value. See .dao_response.DaoResponse
    """
    @abstractmethod
    def delete(self, reservation):
        pass


"""
This DAO class database operations on reservations
"""
class ReservationDao(ReservationDaoBase):

    """
    This constructor method is used to configure injected dependencies for the DAO

    Parameters:

    self: the implicit object that allows access to class properties
    """
    def __init__(self):
        super().__init__()

    """
    This method creates a reservation record

    Parameters:

    self: the implicit object that allows access to class properties
    reservation: the reservation to create

    Returns: None
    """
    @log
    def create(self, reservation):
        # use try/except to handle database errors
        try:
            # create the reservation
            reservation.db.session.add(reservation)
        # handle database errors
        except exc.SQLAlchemyError:
            # encapsulate the error by wrapping it with a custom exception
            raise DatabaseError("Database error")

    """
    This method selects all reservation records

    Parameters:

    self: the implicit object that allows access to class properties

    Returns: a list of all reservation records
    """
    @log
    def read_all(self):
        # use try/except to handle database errors
        try:
            # select all reservations
            reservations = Reservation.query.all()
        # handle database errors
        except exc.SQLAlchemyError:
            # encapsulate the error by wrapping it with a custom exception
            raise DatabaseError("Database error")
        # initialize list that will be used to hold return data
        data = []
        # iterate over reservations
        for res in reservations:
            # for each record add a model to the return data
            data.append(Reservation(res.id, res.name, res.email, res.datetime.strftime('%Y-%m-%d %H:%M:%S'), res.size))
        # return the list of models
        return data

    """
    This method updates a reservation record

    Parameters:

    self: the implicit object that allows access to class properties
    reservation: the reservation to update along with the updated values

    Returns: a Reservation model representing the updated record or None if the record couldn't be found
    """
    @log
    def update(self, reservation):
        # use try/except to handle database errors
        try:
            # select the reservation that will be updated
            record = Reservation.query.filter(Reservation.id == reservation.id).first()
            # if the reservation could not be found
            if record == None:
                # indicate the failure by returning None
                return None
            # update the record
            record.name = reservation.name
            record.email = reservation.email
            record.datetime = reservation.datetime
            record.size = reservation.size
            # return the updated model
            return reservation
        # handle database errors 
        except exc.SQLAlchemyError:
            # encapsulate the error by wrapping it with a custom exception
            raise DatabaseError("Database error")
    
    """
    This method deletes a reservation record

    Parameters:

    self: the implicit object that allows access to class properties
    reservation: the reservation to delete

    Returns: the appropriate DAOResponse enumeration value. See .dao_response.DaoResponse
    """
    @log
    def delete(self, reservation):
        # use try/except to handle database errors
        try:
            # select the reservation that will be deleted
            record = Reservation.query.filter(Reservation.id == reservation.id).first()
            # if the reservation could not be found
            if not record:
                # indicate the failure by returning the appropriate DAOResponse enumeration value
                return DaoResponse.MISSING
            # delete the reservation
            reservation.db.session.delete(record)
            # indicate the successful operation by returning the appropriate DAOResponse enumeration value
            return DaoResponse.SUCCESS
        # handle database errors     
        except exc.SQLAlchemyError:
            # encapsulate the error by wrapping it with a custom exception
            raise DatabaseError("Database error")
