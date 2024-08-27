
class UserError(Exception):
    """Exception raised for errors due to incorrect usage of parameters
    (also includes bad parameters for the current specification)."""
    def __init__(self, message="There was an error with the parameters (maybe in the context of the timed language)."):
        self.message = message
        super().__init__(self.message)

class EmptyLanguageError(Exception):
    """Exception raised for errors due to bad specifications empty languages, etc."""
    def __init__(self, message="There was an error with the timed language."):
        self.message = message
        super().__init__(self.message)
