from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line

shared_data = {'color': (1,0,0)}

class SelectionButtons:
	pass

class MyPaintWidget(RelativeLayout):
	def __init__(self, **args):
		super(MyPaintWidget, self).__init__(**args)
		self.max_figures = 3
		self.figures = []

	def on_touch_down(self, touch):
		if self.ignoring_touches():
			return

		with self.canvas:
			Color(*shared_data['color'])
			touch.ud['line'] = Line(points=(touch.x, touch.y))
		
		return True

	def on_touch_move(self, touch):
		if self.ignoring_touches():
			return

		touch.ud['line'].points += [touch.x, touch.y]
		
		return True

	def on_touch_up(self, touch):
		if self.ignoring_touches():
			return

		self.figures.append(touch.ud['line'])
		
		return True

	def ignoring_touches(self):
		return len(self.figures) == self.max_figures
	
	def undo(self):
		self.figures.pop()


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

		painter = MyPaintWidget(pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(1,1))
		palette = MyColorPalette(pos_hint={'center_x': 0.3, 'center_y': 0.1}, size_hint=(0.3,0.05))
		undobtn = Button(text='Undo', size_hint=(0.07, 0.07), pos_hint={'center_x': 0.8, 'center_y': 0.1})
		clearbtn = Button(text='Clear', size_hint=(0.07, 0.07), pos_hint={'center_x': 0.9, 'center_y': 0.1})

		layout.add_widget(palette, 10)
		layout.add_widget(painter, 20)
		layout.add_widget(undobtn, 10)
		layout.add_widget(clearbtn, 10)
		
		def clear_canvas(obj):
			painter.canvas.clear()
		clearbtn.bind(on_release=clear_canvas)
		
		def undo_canvas(obj):
			painter.undo()
		undobtn.bind(on_release=undo_canvas)

		parent.add_widget(layout)
			   
		return parent


if __name__ == '__main__':
	MyPaintApp().run()
