from enum import Enum


# калбеки
class CB(Enum):
    COM_START = 'com_start'

    SEARCH_START = 'search_start'
    SEARCH_TOURNAMENT = 'search_tournament'
    SEARCH_MATCH = 'search_match'
    SEARCH_GET_RESULT = 'search_get_result'

    # FORECAST_TOP = 'forecast_top'

