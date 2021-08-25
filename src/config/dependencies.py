# dependencies 
from injector import singleton
from ..data.reservation import ReservationDaoBase, ReservationDao
from ..business.reservation import ReservationBusinessServiceBase, ReservationBusinessService
from ..api.reservation import ReservationRestService

"""
This method configures dependencies for dependency injection
Parameters:

binder: the binder object used to bind concrete dependencies to abstract classes
Returns: None
"""
def configure(binder):
    # bind dependencies
    binder.bind(ReservationRestService, to=ReservationRestService, scope=singleton)
    binder.bind(ReservationBusinessServiceBase, to=ReservationBusinessService, scope=singleton)
    binder.bind(ReservationDaoBase, to=ReservationDao, scope=singleton)