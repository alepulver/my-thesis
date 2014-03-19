from kivy.app import App

from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup

class Workflow:
	def __init__(self):
		self.root = FloatLayout()
		self.states = {}
		self.stack = []
		self.data = {}
	
	def add_state(self, step, name):
		self.states[name] = step
	
	def set_handler(self, handler):
		self.handler = handler

	def call_state(self, name, parameters=None):
		self.stack.append([name, parameters])
	
	def return_state(self, parameters):
		self.handler(self, self.current_state, parameters)
		self.next_step()
	
	def storage(self):
		return self.data
		
	def start(self):
		assert(len(self.stack) > 0)
		self.next_step()
		return self.root
	
	def next_step(self):
		assert(len(self.stack) > 0)
		name, parameters = self.stack.pop()
		self.current_state = name
		step = self.states[name]
		widget = step.called_with(self, parameters)
		
		self.root.clear_widgets()
		self.root.add_widget(widget)

class WorkflowStep:
	# XXX: should this be replaced by __init__?
	def called_with(self, workflow, parameters):
		raise NotImplementedError()
	
	def ret(self, parameters):
		self.workflow.return_state(parameters)
	
	def resumed_with(self, workflow, parameters):
		raise NotImplementedError()
	
	def pause(self, parameters):
		raise NotImplementedError()

# Screen 1
class AskSomeNames(WorkflowStep):	
	def reset(self):
		# Screen 1 to 2 communication
		self.remaining = self.quantity
		self.names = []
	
	def called_with(self, workflow, parameters):
		# Starter to screen 1 communication
		self.quantity = parameters['quantity']
		self.check_name = parameters['check_name']
		
		self.workflow = workflow
		self.reset()
		
		self.layout = BoxLayout(orientation='vertical')
		self.text_input = TextInput(font_size=100, size_hint_y=None, height=150)
		self.accept_button = Button(text='Accept name')
		
		self.accept_button.bind(on_release=lambda x: self.on_name_entered(self.text_input.text))
		self.layout.add_widget(self.text_input)
		self.layout.add_widget(self.accept_button)
		
		return self.layout
		
	def on_name_entered(self, name):
		assert(self.remaining > 0)
		if not self.check_name(name):
			popup = Popup(title='Invalid name', content=Label(text='It should have more than 3 characters, press "Esc" to continue'), size=(200,200))
			popup.open()
			return
		# Screen 1 to 2 communication
		self.names.append(name)
		self.remaining -= 1
		if self.remaining == 0:
			self.ret({'names': self.names})

	def check_name(self, name):
		return len(name) > 3

# Stage 2
class ShowList(WorkflowStep):
	def called_with(self, workflow, parameters):
		self.workflow = workflow
		self.layout = BoxLayout(orientation='vertical')
		
		#  Screen 1 to 2 communication
		for n in parameters['names']:
			label = Label(text=n)
			self.layout.add_widget(label)
		
		inner_layout = BoxLayout(orientation='horizontal')
		button_next = Button(text='Next screen')
		button_prev = Button(text='Prev screen')
		inner_layout.add_widget(button_next)
		inner_layout.add_widget(button_prev)
		
		button_next.bind(on_press=lambda x: self.ret('next'))
		button_prev.bind(on_press=lambda x: self.ret('prev'))
		
		self.layout.add_widget(inner_layout)
		return self.layout

# Stage 3
class PromptForExit(WorkflowStep):
	def called_with(self, workflow, parameters):
		button = Button(text='Click to exit')
		button.bind(on_press=lambda x: exit())
			
		return button

class TutorialApp(App):
	def build(self):
		def handler(workflow, name, parameters):
			if name == 'ask_names':
				workflow.call_state('show_names', parameters)
			elif name == 'show_names':
				if parameters == 'prev':
					workflow.call_state('ask_names', {'quantity': 3, 'check_name': lambda x: len(x) > 3})
				elif parameters == 'next':
					workflow.call_state('prompt_for_exit')

		workflow = Workflow()
		
		ask_names = AskSomeNames()
		workflow.add_state(ask_names, 'ask_names')
		
		show_names = ShowList()
		workflow.add_state(show_names, 'show_names')
		
		prompt_for_exit = PromptForExit()
		workflow.add_state(prompt_for_exit, 'prompt_for_exit')
		
		workflow.call_state('ask_names', {'quantity': 3, 'check_name': lambda x: len(x) > 3})
		workflow.set_handler(handler)
		return workflow.start()

if __name__ == "__main__":
	TutorialApp().run()
