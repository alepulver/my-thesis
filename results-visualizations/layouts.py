import pyx


class Layout:
    pass


class CircularLayout(Layout):
    pass


class RectangularLayout(Layout):
    def __init__(self, width, height):
        assert(width > 0)
        assert(height > 0)

        self.width = width
        self.height = height

    def draw(self, clusters, canvas):
        group = 0
        for c in clusters.values():
            index = 0
            for e in c:
                row = index // self.width
                column = index % self.width

                figure = pyx.canvas.canvas()
                e['stage'].draw(figure)
                transform = pyx.trafo.scale(0.01, 0.01)
                transform = transform.translated(group * self.width * 12 + column * 10, row * 6.5)
                canvas.insert(figure, [transform])

                index += 1
            group += 1