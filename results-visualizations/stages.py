import pyx
import math


def all_stages():
    return [PresentPastFuture, SeasonsOfYear, DaysOfWeek, PartsOfDay, Timeline]


class wedge(pyx.path.path):
    def __init__(self, x, y, radius, angle1, angle2):
        pyx.path.path.__init__(self,
            pyx.path.moveto(x, y),
            pyx.path.lineto(x + radius*math.cos(math.radians(angle1)), y + radius*math.sin(math.radians(angle1))),
            pyx.path.arc(x, y, radius, angle1, angle2),
            pyx.path.lineto(x, y),
            pyx.path.closepath()
        )


class Stage:
    @classmethod
    def stage_name(cls):
        return cls.stage_code

    color_translation = {
        'black': pyx.color.gray.black,
        'blue': pyx.color.rgb.blue,
        'darkviolet': pyx.color.cmyk.Plum,
        'green': pyx.color.rgb.green,
        'grey': pyx.color.cmyk.Gray,
        'red': pyx.color.rgb.red,
        'saddlebrown': pyx.color.cmyk.RawSienna,
        'yellow': pyx.color.cmyk.Yellow
    }
    border_size = 5

    def __init__(self, row):
        self.row = row

    def get_numeric(self, name, element):
        return float(self.row['{}_{}'.format(name, element)])

    def get_color(self, name, element):
        color_name = self.row['{}_{}'.format(name, element)]
        return self.color_translation[color_name]


class PresentPastFuture(Stage):
    stage_code = 'present_past_future'
    elements = ['past', 'present', 'future']

    def draw(self, canvas):
        canvas.stroke(pyx.path.rect(0, 0, 800, 500))
        for e in self.elements:
            circle_path = pyx.path.circle(
                self.get_numeric('center_x', e),
                500 - self.get_numeric('center_y', e),
                self.get_numeric('radius', e)
            )
            canvas.stroke(circle_path, [
                pyx.style.linewidth(self.border_size),
                pyx.deco.stroked([self.get_color('color', e)])
            ])


class SeasonsOfYear(Stage):
    stage_code = 'seasons_of_year'
    elements = ['summer', 'autum', 'winter', 'spring']

    def draw(self, canvas):
        canvas.stroke(pyx.path.rect(0, 0, 800, 500))
        for e in self.elements:
            rect_path = pyx.path.rect(
                self.get_numeric('center_x', e) - self.get_numeric('size_x', e)/2,
                500 - (self.get_numeric('center_y', e) + self.get_numeric('size_y', e)/2),
                self.get_numeric('size_x', e),
                self.get_numeric('size_y', e)
            )
            canvas.stroke(rect_path, [
                pyx.style.linewidth(self.border_size),
                pyx.deco.stroked([self.get_color('color', e)])
            ])


class DaysOfWeek(Stage):
    stage_code = 'days_of_week'
    elements = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    def draw(self, canvas):
        canvas.stroke(pyx.path.rect(0, 0, 800, 500))
        for e in self.elements:
            rect_path = pyx.path.rect(
                self.get_numeric('center_x', e) - 50/2,
                500 - (self.get_numeric('center_y', e) + self.get_numeric('size_y', e)/2),
                50,
                self.get_numeric('size_y', e)
            )

            canvas.fill(rect_path, [
                pyx.deco.filled([self.get_color('color', e)])
            ])


class PartsOfDay(Stage):
    stage_code = 'parts_of_day'
    elements = ['morning', 'afternoon', 'night']

    def draw(self, canvas):
        canvas.stroke(pyx.path.rect(0, 0, 800, 500))
        for e in self.elements:
            wedge_path = wedge(
                400, 250, 200,
                self.get_numeric('rotation', e) - self.get_numeric('size', e)/2,
                self.get_numeric('rotation', e) + self.get_numeric('size', e)/2
            )

            canvas.fill(wedge_path, [
                pyx.deco.filled([self.get_color('color', e), pyx.color.transparency(0.4)])
            ])


class Timeline(Stage):
    stage_code = 'timeline'