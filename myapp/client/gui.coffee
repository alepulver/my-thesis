_ = lodash

class ChoosePanel
	constructor: (@choices, @layer) ->
		self = this
		@selected_choices = []
		@remaining = _.size(@choices)
		this.notifier = null
		
		p = 0.1
		_.forOwn(@choices, (text, key) ->
			button = new MyButton({
      			text: text,
      			x: 30,
      			y: self.layer.getHeight()*p,
      			width: 100
			})
			button.on('mousedown', ->
				self.button_pressed(key)
			)
			self.layer.add button
			p += 0.8/_.size(self.choices)
		)

	setNotifier: (notifier) ->
		@notifier = notifier

	button_pressed: (name) ->
		@notifier(name) if @notifier != null

	setColor: (color) ->
		0

@csExport ?= {}
_.merge(@csExport,
	ChoosePanel: ChoosePanel
)