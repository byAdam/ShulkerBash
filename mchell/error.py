class InvalidCommandException(Exception):
    def __init__(self, command):
        message = "Invalid Command: {}".format(command)
        super().__init__(message)

class UnknownCommandException(Exception):
    def __init__(self, command):
        message = "Unknown Command: {}".format(command)
        super().__init__(message)