from kivy.app import App

from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup


class HandlerFlowControl:
	def __init__(self):
		self.root = FloatLayout()
		self.state = HandlerStateAskNames(self)
		self.state.start()
		
	def askNamesStart(self):
		# XXX: note we are using state to keep our local variables, otherwise there could be only one copy
		self.state.names = []
		layout = BoxLayout(orientation='vertical')
		text_input = TextInput(font_size=100, size_hint_y=None, height=150)
		accept_button = Button(text='Accept name')
		
		accept_button.bind(on_release=lambda x: self.state.nameEntered(text_input.text))
		layout.add_widget(text_input)
		layout.add_widget(accept_button)
		
		self.root.clear_widgets()
		self.root.add_widget(layout)
	
	def askNamesEnd(self):
		self.state = HandlerStateShowNames(self)
		self.state.start()
	
	def askNamesNameEntered(self, name):
		if len(name) > 3:
			self.state.names.append(name)
			
			if len(self.state.names) == 3:
				self.state = HandlerStateShowNames(self)
				self.state.start(self.state.names)
		else:
			# XXX: should be another state
			popup = Popup(title='Invalid name', content=Label(text='It should have more than 3 characters, press "Esc" to continue'), size=(200,200))
			popup.open()
	
	def showNamesStart(self, names):
		layout = BoxLayout(orientation='vertical')
		
		#  Screen 1 to 2 communication
		for n in names:
			label = Label(text=n)
			layout.add_widget(label)
		
		inner_layout = BoxLayout(orientation='horizontal')
		button_next = Button(text='Next screen')
		button_prev = Button(text='Prev screen')
		inner_layout.add_widget(button_next)
		inner_layout.add_widget(button_prev)
		
		button_next.bind(on_press=lambda x: self.state.next())
		button_prev.bind(on_press=lambda x: self.state.prev())
		
		layout.add_widget(inner_layout)
		
		self.root.clear_widgets()
		self.root.add_widget(layout)
	
	def showNamesEnd(self):
		pass
		
	def showNamesPressPrev(self):
		self.my_names = []
		self.state = HandlerStateAskNames(self)
		self.state.start()
	
	def showNamesPressNext(self):
		self.state = HandlerStatePromptForExit(self)
		self.state.start()

	def promptForExitStart(self):
		button = Button(text='Click to exit')
		button.bind(on_press=lambda x: exit())
		
		self.root.clear_widgets()
		self.root.add_widget(button)

	def promptForExitQuit(self):
		pass


# XXX: these can be implemented with pure metaprogramming, allowing to specify which events to ignore

class HandlerState:
	def __init__(self, handler):
		self.handler = handler
	
	def start(self):
		raise NotImplementedError()
	
	def end(self):
		raise NotImplementedError()


class HandlerStateAskNames(HandlerState):
	def start(self):
		self.handler.askNamesStart()
	
	def end(self):
		self.handler.askNamesEnd()
				
	def nameEntered(self, name):
		self.handler.askNamesNameEntered(name)


class HandlerStateShowNames(HandlerState):
	def start(self, names):
		self.handler.showNamesStart(names)
	
	def end(self):
		self.handler.showNamesEnd()
		
	def next(self):
		self.handler.showNamesPressNext()
	
	def prev(self):
		self.handler.showNamesPressPrev()


class HandlerStatePromptForExit(HandlerState):
	def start(self):
		self.handler.promptForExitStart()
	
	def end(self):
		self.handler.promptForExitEnd()
		
	def exit(self):
		self.handler.promptForExitQuit()


class TutorialApp(App):
	def build(self):
		fc = HandlerFlowControl()
		return fc.root


if __name__ == "__main__":
	TutorialApp().run()
