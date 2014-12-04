class Events:
    def __init__(self, elements):
        self.elements = elements

    def color_changes(self, stage):
        counts = {}
        for e in self.elements:
            counts[e] = 0

        events = stage._data['results']['drawing']['events']
        for e in events:
            if e['type'] == 'color':
                counts[e['arg']] += 1
        return counts

    def resizes(self, stage):
        pass

    def moves(self, stage):
        pass

    def active_time(self, stage):
        pass

    def selection_order(self, stage):
        pass


class Geometry:
    def __init__(self, stage):
        self.stage = stage
        self.variables = {}

    def case_present_past_future(self, other):
        pass

    def case_days_of_week(self, other):
        pass

    def case_parts_of_day(self, other):
        pass

    def case_seasons_of_year(self, other):
        pass

    def case_timeline(self, other):
        pass
