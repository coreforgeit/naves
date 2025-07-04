from enum import Enum


class UserState(Enum):
    SEARCH = 'search'


class SearchStep(Enum):
    START = 'start'
    SPORT = 'sport'
    TOURNAMENT = 'tournament'
    MATCH = 'match'
    RESULT = 'result'
