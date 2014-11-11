import json


class Stage:
    def __init__(self, data):
        self._data = data

    def stage_name(self):
        return type(self).stage_name()

    @classmethod
    def visit_header(cls, other):
        return getattr(other, 'case_%s' % cls.stage_name())(cls)

    def visit(self, other):
        return getattr(other, 'case_%s' % self.stage_name())(self)

    def experiment_id(self):
        return self._data['experiment']

    def time_start(self):
        return self._data['start_time']

    def time_duration(self):
        return self._data['end_time'] - self._data['start_time']

    def size_in_bytes(self):
        return len(json.dumps(self._data))


class Introduction(Stage):
    @staticmethod
    def stage_name():
        return 'introduction'

    def ip_address(self):
        return self._data['results']['ip_address']

    def user_agent(self):
        return self._data['results']['user_agent']

    def participant(self):
        return self._data['results']['participant']

    def local_id(self):
        return self._data['results']['local_id']


class QuestionsBegin(Stage):
    @staticmethod
    def stage_name():
        return 'questions_begining'

    def name(self):
        return self._data['results']['name']

    def age(self):
        return self._data['results']['age']

    def sex(self):
        return self._data['results']['sex']

    # XXX: TEDx does not have "working"/"studying", but the others may be too few to analyze


class PresentPastFuture(Stage):
    @staticmethod
    def stage_name():
        return 'present_past_future'

    @staticmethod
    def stage_elements():
        return ['present', 'past', 'future']


class SeasonsOfYear(Stage):
    @staticmethod
    def stage_name():
        return 'seasons_of_year'

    @staticmethod
    def stage_elements():
        return ['summer', 'autum', 'winter', 'spring']


class DaysOfWeek(Stage):
    @staticmethod
    def stage_name():
        return 'days_of_week'

    @staticmethod
    def stage_elements():
        return ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


class PartsOfDay(Stage):
    @staticmethod
    def stage_name():
        return 'parts_of_day'

    @staticmethod
    def stage_elements():
        return ['morning', 'afternoon', 'night']


class Timeline(Stage):
    @staticmethod
    def stage_name():
        return 'timeline'

    @staticmethod
    def stage_elements():
        return ['my_birth', 'my_childhood', 'my_youth', 'today', 'my_third_age', 'year_1900', 'year_2100', 'wwii', 'the_beatles']


class QuestionsEnd(Stage):
    @staticmethod
    def stage_name():
        return 'questions_ending'

    def represents_time(self):
        return self._data['results']['represents_time']

    def cronotype(self):
        return self._data['results']['daynight']

    def choice_size(self):
        return self._data['results']['slider-size'] / 10

    def choice_color(self):
        return self._data['results']['slider-color'] / 10

    def choice_position(self):
        return self._data['results']['slider-position'] / 10


def stage_from(stage_row):
    stage_classes = [
        Introduction,
        QuestionsBegin,
        PresentPastFuture,
        SeasonsOfYear,
        DaysOfWeek,
        PartsOfDay,
        Timeline,
        QuestionsEnd
    ]

    cls = list(c for c in stage_classes if c.stage_name() == stage_row['stage'])
    if len(cls) > 0:
        return cls[0](stage_row)
    else:
        raise 'unknown stage'
