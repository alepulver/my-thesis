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
			if not check_name(name):
				return
			names.append(name)
			remaining -= 1
			
			if remaining == 0:
				# Screen 1 to 2 transition
				widget = second_step()
				root.clear_widgets()
				root.add_widget(widget)
		
		# Step 1 custom action
		def check_name(name):
			return len(name > 3)
		
		# Screen 2 setup
		def second_step():
			layout = BoxLayout(orientation='vertical')
			for n in names:
				label = Label(text=n)
				layout.add_widget(label)
			
			inner_layout = BoxLayout(orientation='horizontal')
			button_next = Button(text='Next screen')
			button_prev = Button(text='Prev screen')
			inner_layout.add_widget(button_prev)
			inner_layout.add_widget(button_next)
			button_next.bind(on_press=lambda x: on_next_pressed())
			button_prev.bind(on_press=lambda x: on_prev_pressed())
			
			layout.add_widget(inner_layout)
			
			return layout
	
		# Screen 2 to 3 transition
		def on_next_pressed():		
			widget = third_step()
			root.clear_widgets()
			root.add_widget(widget)

		# Screen 2 to 1 transition
		def on_prev_pressed():
			nonlocal remaining, names
			remaining = 3
			names = []
			
			widget = first_step()
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
