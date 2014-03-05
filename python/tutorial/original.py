from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button

class TutorialApp(App):
	def build(self):
		# Globals for communication between screens
		names = []
		root = FloatLayout()
		remaining = 3
		
		# Screen 1
		def first_step():
			layout = BoxLayout(orientation='vertical')
			text_input = TextInput(font_size=100, size_hint_y=None, height=150)
			accept_button = Button(text='Accept name')
		
			accept_button.bind(on_release=lambda x: on_name_entered(text_input.text))
			layout.add_widget(text_input)
			layout.add_widget(accept_button)
			
			return layout
		
		# Screen 1 action
		def on_name_entered(name):
			nonlocal remaining
			
			assert(remaining > 0)
			names.append(name)
			remaining -= 1
			
			if remaining == 0:
				# Screen 1 to 2 transition
				widget = second_step()
				root.clear_widgets()
				root.add_widget(widget)
		
		# Screen 2 setup
		def second_step():
			layout = BoxLayout(orientation='vertical')
			for n in names:
				label = Label(text=n)
				layout.add_widget(label)
			button = Button(text='Next screen')
			button.bind(on_press=lambda x: on_exit_pressed())
			layout.add_widget(button)
			
			return layout
	
		# Screen 2 to 3 transition
		def on_exit_pressed():
			widget = third_step()
			root.clear_widgets()
			root.add_widget(widget)

		# Screen 3 setup
		def third_step():
			button = Button(text='Click to exit')
			button.bind(on_press=lambda x: exit())
			
			return button

		start = first_step()
		root.add_widget(start)
		return root

if __name__ == "__main__":
	TutorialApp().run()
