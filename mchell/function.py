from command import CommandInfo

class Function:
    def __init__(self, base_path, relative_path):
        self.base_path = base_path
        self.relative_path = relative_path

        self.load()

    def load(self):
        with open(self.base_path) as f:
            self.lines = [x.strip() for x in f.readlines()]

    def get_commands_for_stack(self, execute_at, execute_by):
        return [CommandInfo(line, execute_at, execute_by, self.relative_path) for line in reversed(self.lines)]