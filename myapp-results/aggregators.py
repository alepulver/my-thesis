class Events:
    def __init__(self, stage):
        self.stage = stage
        self.elements = stage.stage_elements()

    def color_changes(self):
        stage = self.stage
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

    def selection_order(self):
        stage = self.stage
        result = []
        events = stage._data['results']['choose']['events']
        for e in events:
            if e['type'] == 'choose':
                result.append(e['arg'])
        return result

    def order_matching(self):
        stage = self.stage
        shown = stage._data['results']['choose']['show_order']
        selected = self.selection_order()
        totalOne = [1 if a == b else 0 for (a, b) in zip(shown, selected)]
        totalTwo = [1 if a == b else 0 for (a, b) in zip(shown, reversed(selected))]
        if totalOne > totalTwo:
            return sum(totalOne) / len(totalOne)
        else:
            return -sum(totalTwo) / len(totalTwo)


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
