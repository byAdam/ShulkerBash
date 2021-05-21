from app import main_app as app

class CommandInfo:
    def __init__(self, raw, execute_at = (0, 0, 0), execute_by = None):
        self.raw = raw
        self.execute_at = execute_at
        self.execute_by = execute_by

        self.command = self.get_command()

    def execute(self):
        if self.command:
            self.command.execute_valid(self.execute_at, self.execute_by)

    def get_command(self):
        args = self.raw.split(" ")
        command = args[0]
        args = args[1:]

        if command in app.interpreter.commands:
            return app.interpreter.commands[command](args)
        else:
            print("Error: Unknown command")

class Command:
    def __init__(self, args):
        self.args = args
        self.valid = False
        self.process_args()

    def execute_valid(self, execute_at, execute_by):
        if self.valid:
            self.execute(execute_at, execute_by)
        else:
            print("Invalid Command")

    def process_args(self):
        ## Try find valid arguments for each scheme
        for scheme in self.schemes():
            self.pargs = self.process_args_with_scheme(scheme)

            if self.pargs is not None:
                break
        
        self.valid = self.pargs is not None

    def process_args_with_scheme(self, scheme):
        pargs = {}

        index = 0
        min_scheme = scheme[0]

        for arg in scheme[1:]:
            # Reached end of args
            if index >= len(self.args):
                break

            min_scheme -= 1
            name, value, index = arg.get_data(self.args, index)

            if value is not None:
                pargs[name] = value
            else:
                return None

        # If min scheme
        if min_scheme <= 0:
            return pargs

        return None

    def merge_coordinates(self, coords, execute_at):
        return (
            int(coords[0][1:]) + execute_at[0] if type(coords[0][0]) is str else coords[0],
            int(coords[1][1:]) + execute_at[1] if type(coords[1][0]) is str else coords[1],
            int(coords[2][1:]) + execute_at[2] if type(coords[2][0]) is str else coords[2]
        )