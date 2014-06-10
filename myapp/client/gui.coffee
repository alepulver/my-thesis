_ = lodash

class ChoosePanel
	constructor: (choices, @layer) ->
		self = this
		@choices = _.mapValues(choices, (text) ->
			{text: text, button: null, dot: null}
		)
		@remaining = _.size(@choices)
		@current = null
		@notifier = null
		
		p = 0.1
		_.forOwn(@choices, (data, key) ->
			button = new MyButton({
      			text: data.text,
      			x: 30,
      			y: self.layer.getHeight()*p,
      			width: 100
			})
			button.on('mousedown', ->
				self.itemStarted(key)
			)
			data.button = button
			self.layer.add button

			dot = new Kinetic.Circle(
				x: 15
				y: self.layer.height()*p + button.height()/2
				radius: 5
				stroke: 'black'
			)
			data.dot = dot
			self.layer.add dot

			p += 0.8/_.size(self.choices)
		)

	setNotifier: (@notifier) ->
		@layer.listening(@notifier != null)

	itemStarted: (key) ->
		@active_item = key
		@remaining--

		@choices[key].dot.fill('black')
		@choices[key].button.listening(false)
		@choices[key].button.find('.background')[0].fill('#bbb')
		@layer.draw()

		@notifier(key) if @notifier != null

	itemEnded: ->


	colorSelected: (color) ->
		shape = @choices[@active_item].dot
		shape.fill(color)
		shape.getParent().draw()


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