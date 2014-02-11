from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line

shared_data = {'color': (1,0,0)}

class MyPaintWidget(RelativeLayout):
    def __init__(self, **args):
        super(MyPaintWidget, self).__init__(**args)
        pos_hint={'center_x': 0.9, 'center_y': 0.1}
        button = Button(text='undo', size_hint=(0.07, 0.07), pos_hint=pos_hint)
        self.add_widget(button)
        self.remaining = 3

    def on_touch_down(self, touch):
        if self.remaining <= 0:
            return

        color = (random(), 1, 1)
        with self.canvas:
            #Color(*color, mode='hsv')
            Color(*shared_data['color'])
            d = 30.
            #Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        if self.remaining <= 0:
            return

        touch.ud['line'].points += [touch.x, touch.y]

    def on_touch_up(self, touch):
        if self.remaining <= 0:
            return

        self.remaining -= 1
        if self.remaining == 0:
            print 'done'


class MyColorPalette(RelativeLayout):
    def __init__(self, **kwargs):
        super(MyColorPalette, self).__init__(**kwargs)

        myhash = {}

        def callback(instance):
            shared_data['color'] = myhash[instance]
            return True

        colors = [(1,0,0), (0,1,0), (0,0,1)]
        for (i,c) in enumerate(colors):
            pos_hint = {'center_x': 0.5*float(1)/len(colors) + float(i)/len(colors), 'center_y:': 0.5}
            button = Button(text=str(i), size_hint=(0.9/len(colors), 0.7), pos_hint=pos_hint)
            myhash[button] = c
            button.bind(on_press=callback)
            self.add_widget(button)


class MyPaintApp(App):

    def build(self):
        parent = Widget()

        layout = RelativeLayout(size=(800,800))

        #print(parent.size)
        painter = MyPaintWidget(pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(1,1))
        palette = MyColorPalette(pos_hint={'center_x': 0.3, 'center_y': 0.1}, size_hint=(0.3,0.05))
        clearbtn = Button(text='Clear')

        layout.add_widget(palette, 10)
        layout.add_widget(painter, 20)
        
        parent.add_widget(layout)

        def clear_canvas(obj):
            painter.canvas.clear()
        clearbtn.bind(on_release=clear_canvas)

        return parent


if __name__ == '__main__':
    MyPaintApp().run()