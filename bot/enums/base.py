from enum import Enum


# Команды меню
class MenuCommand(Enum):
    START = ('start', '🔄 В начало')

    def __init__(self, command, label):
        self.command = command
        self.label = label
