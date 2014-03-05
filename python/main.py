from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line
import math

shared_data = {'color': (1,0,0)}

class SelectionButtons:
	pass

class MyPaintWidget(RelativeLayout):
	def __init__(self, **args):
		super().__init__(**args)
		self.max_figures = 3
		self.figures = []
		self.pressing = False

	def on_touch_down(self, touch):
		if self.ignoring_touches():
			return

		with self.canvas:
			Color(*shared_data['color'])
			touch.ud['line'] = Line(points=(touch.x, touch.y))

		# Button widget doesn't define on_touch_*, so they will be passed to canvas under them
		self.pressing = True
		return True

	def on_touch_move(self, touch):
		if self.ignoring_touches():
			return

		touch.ud['line'].points += [touch.x, touch.y]
		
		return True

	def on_touch_up(self, touch):
		def distance(a, b):
			return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1]))
		
		if self.ignoring_touches() or not self.pressing:
			return

		self.figures.append(touch.ud['line'])
		self.pressing = False
		
		#print(type(touch.ud['line'].points))
		#print(touch.ud['line'].points)
		d = distance(touch.ud['line'].points[0:2], touch.ud['line'].points[-2:])
		if d > 30:
			print('distance %s' % d)
			self.undo()
			popup = Popup(title='Test popup', content=Label(text='Hello world'), size=(200,200))
			popup.open()
			#self.add_widget(popup)

		
		return True

	def ignoring_touches(self):
		return len(self.figures) == self.max_figures
	
	def undo(self):
		if len(self.figures) > 0:
			self.canvas.remove(self.figures.pop())
	
	def clear(self):
		self.canvas.clear()
		self.figures = []


class MyColorPalette(RelativeLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		myhash = {}

		def the_callback(instance):
			shared_data['color'] = myhash[instance]
			return True

		colors = [(1,0,0), (0,1,0), (0,0,1)]
		for (i,c) in enumerate(colors):
			pos_hint = {'center_x': 0.5*float(1)/len(colors) + float(i)/len(colors), 'center_y:': 0.5}
			button = Button(text=str(i), size_hint=(0.9/len(colors), 0.7), pos_hint=pos_hint)
			myhash[button] = c
			self.add_widget(button)
			button.bind(on_release=the_callback)
			#button.bind(on_press=callback)

class MyRoot(Widget):
	pass

class MyPaintApp(App):
	def build(self):
		return MyRoot()

if __name__ == '__main__':
	MyPaintApp().run()
