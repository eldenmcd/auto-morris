# define Python user-defined exceptions
class MM3MoveException(Exception):
    """Exception for an invalid move in 3 Mens Morris"""

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

        def __str__(self):
            if self.message:
                return f"MM3MoveException, {self.message}"
            else:
                return "MM3MoveException raised"
