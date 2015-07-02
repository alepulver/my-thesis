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

    def draw(self, canvas):
        raise NotImplementedError()


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
            canvas.draw(circle_path, [
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
            canvas.draw(rect_path, [
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

            canvas.draw(rect_path, [
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

            canvas.draw(wedge_path, [
                pyx.deco.filled([self.get_color('color', e), pyx.color.transparency(0.35)])
            ])


class Timeline(Stage):
    stage_code = 'timeline'
    elements = [
        'year_1900', 'wwii', 'the_beatles',
        'my_birth', 'my_childhood', 'my_youth',
        'today', 'my_third_age', 'year_2100'
    ]

    @classmethod
    def get_color_for(cls, element):
        colors = {
            'year_1900': 'black',
            'wwii': 'saddlebrown',
            'the_beatles': 'grey',
            'my_birth': 'yellow',
            'my_childhood': 'green',
            'my_youth': 'darkviolet',
            'today': 'red',
            'my_third_age': 'saddlebrown',
            'year_2100': 'black'
        }

        return cls.color_translation[colors[element]]

    def draw(self, canvas):
        line_length = float(self.row['line_length'])
        line_rotation = float(self.row['line_rotation'])
        normalization = 800/line_length

        canvas.stroke(pyx.path.rect(0, 0, 800, 500))

        figure = pyx.canvas.canvas()
        line_path = pyx.path.line(0, 0, 1, 0)
        figure.stroke(line_path, [pyx.style.linewidth(0.02*normalization)])

        for e in self.elements:
            position = self.get_numeric('position', e)
            color = self.get_color_for(e)
            line_path = pyx.path.line(position, 0.15*normalization, position, -0.15*normalization)
            figure.stroke(line_path, [pyx.style.linewidth(0.02*normalization), color])

        transform = pyx.trafo.trafo().\
            translated(-0.5, 0).\
            rotated(line_rotation).\
            scaled(line_length*0.9, line_length*0.9).\
            translated(400, 250)
        canvas.insert(figure, [transform])
