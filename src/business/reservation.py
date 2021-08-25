# dependencies
from abc import ABC, abstractmethod
from injector import inject
from ..data.reservation import ReservationDaoBase
from flask_sqlalchemy import SQLAlchemy
from .business_response import BusinessResponse
from ..data.dao_response import DaoResponse
from ..config.db_config import db
from ..logging.log import log

"""
This abstract class is used to define the API that reservation business services should implement
"""
class ReservationBusinessServiceBase(ABC):

    """
    This constructor method is used to configure injected dependencies for the business service

    Parameters:

    self: the implicit object that allows access to class properties
    """
    def __init__(self):
        pass

    """
    This method oversess business rules and business logic for reserving a booking/reservation

    Parameters:

    self: the implicit object that allows access to class properties
    reservation: the reservation being made

    Returns: dictionary of the newly reserved booking/reservation
    """
    @abstractmethod
    def reserve(self, reservation):
        pass

    """
    This method oversess business rules and business logic for retriving all reservations

    Parameters:

    self: the implicit object that allows access to class properties

    Returns: a list of all reservations as dictionaries
    """
    @abstractmethod
    def retrieve_all(self):
        pass

    """
    This method oversess business rules and business logic for editing a reservation

    Parameters:

    self: the implicit object that allows access to class properties
    reservation: the reservation being edited

    Returns: a dictionary of the updated reservation or None if the specified reservation could not be found
    """
    @abstractmethod
    def edit(self, reservation):
        pass

    """
    This method oversess business rules and business logic for canceling a reservation

    Parameters:

    self: the implicit object that allows access to class properties
    reservation: the reservation being canceled

    Returns: the appropriate BusinessResponse enumeration value. See .business_response.BusinessResponse
    """
    @abstractmethod
    def cancel(self, reservation):
        pass


"""
This class oversess business rules and business logic related to reservations
"""
class ReservationBusinessService(ReservationBusinessServiceBase):

    """
    This constructor method is used to configure injected dependencies for the business service

    Parameters:

    self: the implicit object that allows access to class properties
    dao: the abstract class used to inject the DAO dependency
    """
    @inject
    def __init__(self, dao: ReservationDaoBase):
        super().__init__()
        # use constructor injection to initalize dao 
        self.dao = dao

    """
    This method oversess business rules and business logic for reserving a booking/reservation

    Parameters:

    self: the implicit object that allows access to class properties
    reservation: the reservation being made

    Returns: dictionary of the newly reserved booking/reservation
    """
    @log
    def reserve(self, reservation):
        # pass control to data layer to create the reservation
        self.dao.create(reservation)
        # commit the transaction
        db.session.commit()
        # return the reservation in json serialized form
        return reservation.serialize()

    """
    This method oversess business rules and business logic for retriving all reservations

    Parameters:

    self: the implicit object that allows access to class properties

    Returns: a list of all reservations as dictionaries 
    """
    @log
    def retrieve_all(self):
        # pass control to data layer to read all reservations
        reservations = self.dao.read_all()
        # initialize empty list that will be used to hold return data
        data = []
        # iterate over the reservations
        for res in reservations: 
            # for each reservation add a serialized record to the return data
            data.append(res.serialize())
        # return all reservations in serialized form
        return data
    
    """
    This method oversess business rules and business logic for editing a reservation

    Parameters:

    self: the implicit object that allows access to class properties
    reservation: the reservation being edited

    Returns: a dictionary of the updated reservation or None if the specified reservation could not be found
    """
    @log
    def edit(self, reservation):
        # pass control to the data layer to update the reservation
        data = self.dao.update(reservation)
        # commit the transaction
        db.session.commit()
        # if the update failed
        if not data:
            # indicate the failure by returning None
            return None
        # the update was successful
        else:
            # return the updated reservation in serialized form
            return data.serialize()
    """
    This method oversess business rules and business logic for canceling a reservation

    Parameters:

    self: the implicit object that allows access to class properties
    reservation: the reservation being canceled

    Returns: the appropriate BusinessResponse enumeration value. See .business_response.BusinessResponse
    """
    @log
    def cancel(self, reservation):
        # pass control to the data layer to delete the reservation
        res = self.dao.delete(reservation)
        # commit the transaction
        db.session.commit()
        # if the deletion succeeded
        if res == DaoResponse.SUCCESS: 
            # return the appropriate business response
            return BusinessResponse.OK
        # deletion failed
        else:
            # return the appropriate business response
            return BusinessResponse.NOT_FOUND

