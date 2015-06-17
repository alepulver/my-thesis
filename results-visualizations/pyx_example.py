import math
from pyx import canvas, path, deco, color

c = canvas.canvas()
#c.stroke(path.line(0, 0, 3, 0))
#c.stroke(path.rect(0, 1, 1, 1))
c.fill(path.circle(0, 0, 1), [deco.filled([color.rgb.green])])

N = 5

for i in range(N+1):
    x = i/N * math.pi * 2
    c.stroke(path.line(0, 0, math.sin(x), math.cos(x)))

    for d in range(1, 10):
        x = (i+.5)/N * math.pi * 2
        c.fill(path.circle(d/10*math.sin(x), d/10*math.cos(x), 0.05), [deco.filled([color.rgb.blue])])

#c.writeEPSfile("path")
c.writePDFfile("path")
#c.writeSVGfile("path")