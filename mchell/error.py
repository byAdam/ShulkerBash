class InvalidArgumentException(Exception):
    def __init__(self, command):
        message = "Invalid Command: {}\n".format(command)
        message += "Try 'help {0}' for more information.".format(command.split(" ")[0])
        super().__init__(message)

class InvalidCommandException(Exception):
    def __init__(self, command, reason):
        message = "Invalid Command: {}\n".format(command)
        message += "Reason: {}".format(reason)
        super().__init__(message)

class UnknownCommandException(Exception):
    def __init__(self, command):
        message = "Unknown Command: {}".format(command)
        super().__init__(message)

class UnknownFunctionException(Exception):
    def __init__(self, function):
        message = "Unknown Function: {}".format(function)
        super().__init__(message)

class UnknownObjectiveException(Exception):
    def __init__(self, objective):
        message = "Unknown Objective: {}\n".format(objective)
        message += "Try 'scoreboard objectives add {}' to add the objective.".format(objective)
        super().__init__(message)

class TooManyTargetsException(Exception):
    def __init__(self):
        message = "Error: Too many targets matched selector"
        super().__init__(message)
    
class NoTargetsException(Exception):
    def __init__(self):
        message = "Error: No targets matched selector"
        super().__init__(message)

class InvalidSubfunctionException(Exception):
    def __init__(self, name):
        message = "Invalid Subfunction: {}\n".format(name)
        super().__init__(message)

class InvalidResourcePackException(Exception):
    def __init__(self, name):
        message = "Invalid Resource Pack: {}\n".format(name)
        super().__init__(message)