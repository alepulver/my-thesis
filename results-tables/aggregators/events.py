from .order import Order


class Events:
    def __init__(self, stage):
        self.stage = stage
        self.elements = stage.stage_elements()

    def count_by_type(self, event_type):
        stage = self.stage
        counts = {}
        for e in self.elements:
            counts[e] = 0

        events = stage._data['results']['drawing']['events']
        for e in events:
            if e['type'] == event_type:
                counts[e['arg']] += 1
        return counts

    def time_spent(self):
        times = {}
        for e in self.elements:
            times[e] = 0

        current_element = None
        last_timestamp = 0

        events = self.stage._data['results']['drawing']['events']
        for e in events:
            if 'time' in e.keys():
                timestamp = e['time']
            elif 'time' in e['data'].keys():
                timestamp = e['data']['time']

            if current_element is not None:
                times[current_element] += timestamp - last_timestamp

            if e['type'] in ['add', 'select']:
                current_element = e['arg']

            last_timestamp = timestamp

        return times

    def selection_order(self):
        result = []
        events = self.stage._data['results']['choose']['events']
        for e in events:
            if e['type'] == 'choose':
                result.append(e['arg'])
        return result

    def order_matching(self):
        shown = self.stage._data['results']['choose']['show_order']
        selected = self.selection_order()
        return Order.matching_score(shown, selected)
