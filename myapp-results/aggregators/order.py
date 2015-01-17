import itertools as it
import difflib


class Order:
    def order_for(self, stage, elements):
        self.elements = elements
        return stage.visit(self)

    #def case_present_past_future(self, stage):
    #    pass

    #def case_seasons_of_year(self, stage):
    #    pass

    def case_days_of_week(self, stage):
        parts = self.elements
        monday_first = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        sunday_first = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        if parts == monday_first:
            return 'monday_first'
        elif parts == sunday_first:
            return 'sunday_first'
        else:
            return 'not_ordered'

    def case_parts_of_day(self, stage):
        parts = it.cycle(self.elements)
        parts = it.dropwhile(lambda x: x != 'morning', parts)
        morning = next(parts)
        assert(morning == "morning")
        after_morning = next(parts)

        if after_morning == 'afternoon':
            return 'counterclockwise'
        else:
            return 'clockwise'

    def case_timeline(self, stage):
        if stage.rotation() < 90 or stage.rotation() > 270:
            return 'left_right'
        else:
            return 'right_left'

    @staticmethod
    def matching_score(shown, selected):
        assert(len(shown) == len(selected))
        matcher = difflib.SequenceMatcher()
        matcher.set_seqs(shown, selected)
        return matcher.ratio()
