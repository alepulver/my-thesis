import json
import itertools as it


def stage_from(stage_row):
    stage_classes = all_stages()

    cls = list(c for c in stage_classes if c.stage_name() == stage_row['stage'])
    if len(cls) > 0:
        return cls[0](stage_row)
    else:
        raise 'unknown stage'


def all_stages():
    return [
        Introduction,
        QuestionsBegin,
        PresentPastFuture,
        SeasonsOfYear,
        DaysOfWeek,
        PartsOfDay,
        Timeline,
        QuestionsEnd
    ]


def fix_angle(angle):
    while angle < 0:
        angle += 360
    while angle >= 360:
        angle -= 360
    return angle


class Stage:
    def __init__(self, data):
        self._data = data

    def stage_name(self):
        return type(self).stage_name()

    @classmethod
    def visit_class(cls, other):
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
        total = len(json.dumps(self._data))
        if 'stage_as_json' in self._data['results']:
            total -= len(json.dumps(self._data['results']['stage_as_json']))
        return total


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
        if 'local_id' in self._data['results']:
            return self._data['results']['local_id']
        else:
            return 'unknown'


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

    #def working(self):
    #    return self._data['results']['working']

    #def studying(self):
    #    return self._data['results']['studying']


class PresentPastFuture(Stage):
    @staticmethod
    def stage_name():
        return 'present_past_future'

    @staticmethod
    def stage_elements():
        return ['present', 'past', 'future']

    @staticmethod
    def stage_dimensons():
        return {"x": 0, "y": 0}

    def element_data(self, element):
        section = self._data['results']['drawing']['shapes'][element]

        return {
            "center_x": section['position']['x'],
            "center_y": section['position']['y'],
            "color": section['color'],
            "radius": section['radius']
        }


class SeasonsOfYear(Stage):
    @staticmethod
    def stage_name():
        return 'seasons_of_year'

    @staticmethod
    def stage_elements():
        return ['summer', 'autum', 'winter', 'spring']

    def element_data(self, element):
        section = self._data['results']['drawing']['shapes'][element]

        return {
            "center_x": section['position']['x'],
            "center_y": section['position']['y'],
            "size_x": section['size']['width'],
            "size_y": section['size']['height'],
            "color": section['color']
        }

    def overlap(self):
        pass


class DaysOfWeek(Stage):
    @staticmethod
    def stage_name():
        return 'days_of_week'

    @staticmethod
    def stage_elements():
        return ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    def element_data(self, element):
        section = self._data['results']['drawing']['shapes'][element]

        return {
            "center_x": section['position']['x'],
            "center_y": section['position']['y'],
            #"size_x": 50,
            "size_y": section['size']['height'],
            "color": section['color']
        }


class PartsOfDay(Stage):
    @staticmethod
    def stage_name():
        return 'parts_of_day'

    @staticmethod
    def stage_elements():
        return ['morning', 'afternoon', 'night']

    def element_data(self, element):
        section = self._data['results']['drawing']['shapes'][element]
        rotation = section['rotation'] + fix_angle(section['angle']) / 2

        return {
            "rotation": fix_angle(rotation),
            "size": fix_angle(section['angle']),
            "color": section['color']
        }

    def order(self):
        parts = [(p, self.element_data(p)['rotation']) for p in self.stage_elements()]
        parts.sort(key = lambda x: x[1])
        parts = it.cycle(map(lambda x: x[0], parts))
        parts = it.dropwhile(lambda x: x != 'morning', parts)

        morning = next(parts)
        assert(morning == "morning")
        after_morning = next(parts)

        if after_morning == 'afternoon':
            return 'clockwise'
        else:
            return 'counterclockwise'


class Timeline(Stage):
    @staticmethod
    def stage_name():
        return 'timeline'

    @staticmethod
    def stage_elements():
        return [
            'my_birth', 'my_childhood', 'my_youth', 'today',
            'my_third_age', 'year_1900', 'year_2100', 'wwii', 'the_beatles'
        ]

    def element_data(self, element):
        section = self._data['results']['drawing']['shapes'][element]
        position = (section['position'] + 1) / 2

        if self.is_inverted():
            position = 1 - position

        return {
            "position": position
        }

    def length(self):
        return self._data['results']['timeline']['results']['length']

    def rotation(self):
        angle = fix_angle(self._data['results']['timeline']['results']['rotation'])
        if angle >= 0 and angle < 90:
            return angle
        if angle >= 90 and angle < 180:
            return angle - 180
        elif angle >= 180 and angle < 270:
            return angle - 180
        elif angle >= 270 and angle < 360:
            return angle - 360

    def button_order(self):
        value = self._data['results']['choose']['show_order']
        if value == 0:
            return 'chronological'
        elif value == 1:
            return 'unsorted'
        else:
            raise 'unsupported button show order'

    def is_inverted(self):
        angle = fix_angle(self._data['results']['timeline']['results']['rotation'])
        return angle >= 90 and angle < 270


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


class EventAggregator:
    def __init__(self, stage):
        self._stage = stage

