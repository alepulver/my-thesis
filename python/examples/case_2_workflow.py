from kivy.app import App

from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget

class Workflow:
	def __init__(self):
		self.root = FloatLayout()
		self.steps = []
		self.step_index = -1
		self.data = {}
	
	def add_step(self, step):
		step.register_workflow(self)
		self.steps.append(step)
	
	def widget(self):
		return self.root
	
	def storage(self):
		return self.data
		
	def start(self):
		assert(len(self.steps) > 0)
		self.next_step()
	
	def next_step(self):
		assert(self.step_index < len(self.steps))
		self.step_index += 1
		step = self.steps[self.step_index]
		step.workflow_init()
		
		self.root.clear_widgets()
		self.root.add_widget(step.widget())
	
	def prev_step(self):
		assert(self.step_index > 0)
		self.step_index -= 1
		step = self.steps[self.step_index]
		step.workflow_init()
		
		self.root.clear_widgets()
		self.root.add_widget(step.widget())

class WorkflowStep:
	def __init__(self):
		pass
	
	def register_workflow(self, workflow):
		self.workflow = workflow
	
	def workflow_init(self):
		pass

# Screen 1
class AskSomeNames(WorkflowStep):
	def __init__(self, quantity, check_name):
		# Starter to screen 1 communication
		self.quantity = quantity
		self.check_name = check_name
	
	def reset(self):
		# Screen 1 to 2 communication
		self.remaining = self.quantity
		self.workflow.storage()['names'] = []
	
	def workflow_init(self):
		self.reset()
		
		self.layout = BoxLayout(orientation='vertical')
		self.text_input = TextInput(font_size=100, size_hint_y=None, height=150)
		self.accept_button = Button(text='Accept name')
		
		self.accept_button.bind(on_release=lambda x: self.on_name_entered(self.text_input.text))
		self.layout.add_widget(self.text_input)
		self.layout.add_widget(self.accept_button)
		
	def on_name_entered(self, name):
		assert(self.remaining > 0)
		if not self.check_name(name):
			return
		# Screen 1 to 2 communication
		self.workflow.storage()['names'].append(name)
		self.remaining -= 1
		if self.remaining == 0:
			self.workflow.next_step()

	def widget(self):
		return self.layout

# Stage 2
class ShowList(WorkflowStep):
	def workflow_init(self):
		self.layout = BoxLayout(orientation='vertical')
		
		#  Screen 1 to 2 communication
		for n in self.workflow.storage()['names']:
			label = Label(text=n)
			self.layout.add_widget(label)
		
		inner_layout = BoxLayout(orientation='horizontal')
		button_next = Button(text='Next screen')
		button_prev = Button(text='Prev screen')
		inner_layout.add_widget(button_next)
		inner_layout.add_widget(button_prev)
		
		button_next.bind(on_press=lambda x: self.workflow.next_step())
		button_prev.bind(on_press=lambda x: self.workflow.prev_step())
		
		self.layout.add_widget(inner_layout)
	
	def widget(self):
		return self.layout

# Stage 3
class PromptForExit(WorkflowStep):
	def widget(self):
		button = Button(text='Click to exit')
		button.bind(on_press=lambda x: exit())
			
		return button

class TutorialApp(App):
	def build(self):
		workflow = Workflow()
		
		ask_names = AskSomeNames(3, lambda x: len(x) > 3)
		workflow.add_step(ask_names)
		
		show_names = ShowList()
		workflow.add_step(show_names)
		
		prompt_for_exit = PromptForExit()
		workflow.add_step(prompt_for_exit)
		
		workflow.start()
		return workflow.widget()

if __name__ == "__main__":
	TutorialApp().run()
