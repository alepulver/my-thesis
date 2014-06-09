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


class CirclesPanel
	constructor: (@layer) ->
		@circles = []
		@current = null
		
		background = new Kinetic.Rect({
			fill: '#eeffee',
			width: @layer.getWidth(),
			height: @layer.getHeight()
		})
		@layer.add(background)

	addCircle: (@name, @tooltip) ->
		self = this
		
		@circle = new Kinetic.Circle({
			x: 0, y: 0,
			radius: 70,
			stroke: 'black', strokeWidth: 10,
			fill: 'transparent',
			name: 'image'
		})
		AddTooltip(@circle, tooltip)
		@wrapper = new MyResizableWrapper(@circle, @layer)
		
		@button = new MyButton({
			x: 100,
			y: @layer.getHeight()-100,
			width: 100,
			text: 'Accept'
		})
		@button.on('mousedown', -> self.acceptedCircle())

		@layer.add @button
		@layer.add @wrapper
		@layer.draw()

		@circle

	acceptedCircle: ->
		# XXX: avoid error when mouseout arrives later
		@button.off('mouseover')
		@button.off('mouseout')
		@button.remove()
		@wrapper.remove()

		@circle.setPosition(@wrapper.getPosition())
		@layer.add(@circle)
		@layer.draw();
		@notifier(@name, @circle)


	setColor: (color) ->
		@circle.setStroke color
		@circle.draw()

	setNotifier: (@notifier) ->



@csExport ?= {}
_.merge(@csExport,
	ChoosePanel: ChoosePanel
	CirclesPanel: CirclesPanel
)