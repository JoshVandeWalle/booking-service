"""
This exception class defines the custom error type used to indicate model data validation errors
"""
class ValidationError(Exception):

    """
    This constructor method initializes the class' properties
    Parameters:

    self: the implicit object that allows access to class properties
    message: the error message
    """
    def __init__(self, message):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        # initialize error message
        self.message = message