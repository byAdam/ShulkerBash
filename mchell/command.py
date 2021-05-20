from app import main_app as app

class CommandInfo:
    def __init__(self, raw, execute_by=False, execute_at=False):
        self.raw = raw
        self.execute_at = execute_at
        self.execute_by = execute_by

        self.command = self.get_command()

    def execute(self):
        if self.command:
            self.command.execute(self.execute_at, self.execute_by)

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

    def execute(self, execute_at, execute_by):
        pass