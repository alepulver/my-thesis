import pyx


def all_layouts():
    return [CircularLayout, RectangularLayout]


def available_names():
    return [e.name for e in all_layouts()]


def from_name(name):
    mapping = {e.name: e for e in all_layouts()}
    return mapping[name]


class Layout:
    pass


class CircularLayout(Layout):
    name = 'circular'

    def draw(self, sampler, canvas):
        pass


class RectangularLayout(Layout):
    name = 'rectangular'

    def __init__(self, width):
        assert(width > 0)

        self.width = width

    def draw(self, sampler, canvas):
        group = 0
        for c in sampler.cluster_names():
            index = 0
            for e in sampler.sample(c):
                row = index // self.width
                column = index % self.width

                figure = pyx.canvas.canvas()
                e['stage'].draw(figure)
                transform = pyx.trafo.scale(0.01, 0.01)
                transform = transform.translated(group * self.width * 12 + column * 10, row * 6.5)
                canvas.insert(figure, [transform])

                index += 1
            group += 1