class Stage:
    pass


def all_stages():
    return [PresentPastFuture]


class PresentPastFuture(Stage):
    @staticmethod
    def stage_name():
        return 'present_past_future'

    def __init__(self, row):
        self.row = row

    def draw(self, context):
        pass