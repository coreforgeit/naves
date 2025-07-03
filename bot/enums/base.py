from enum import Enum


# Команды меню
class MenuCommand(Enum):
    START = ('start', '🔹 Главное меню ')

    def __init__(self, command, label):
        self.command = command
        self.label = label


class Action(Enum):
    BACK = 'back'
    TOP = 'top'
    ALL = 'all'


SPORT_EMOJI = {
    "футбол": "⚽️",
    "хоккей": "🏒",
    "баскетбол": "🏀",
    "американский футбол": "🏈",
    "теннис": "🎾",
    "волейбол": "🏐",
    "фигурное катание": "⛸",
}
