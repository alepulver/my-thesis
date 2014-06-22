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
		px = 0
		total = 0
		@keys = _.keys(@choices)
		@keys = _.shuffle(@keys)
		_.forEach(@keys, (key) ->
			if (total == 4)
				px += 170
				p = 0.1
				total -= 4
			data = self.choices[key]
			button = Widgets.createButton({
      			text: data.text,
      			x: px + 30,
      			y: self.layer.getHeight()*p,
      			width: 100
			})
			button.on('mousedown', ->
				self.itemStarted(key)
			)
			data.button = button
			self.layer.add button

			dot = new Kinetic.Circle(
				x: px + 15
				y: self.layer.height()*p + button.height()/2
				radius: 5
				stroke: 'black'
			)
			data.dot = dot
			self.layer.add dot

			p += 0.8/_.min([_.size(self.choices), 4])
			total++
		)

	setNotifier: (@notifier) ->
		#@layer.listening(@notifier != null)
		@layer.visible(@notifier != null)
		@layer.draw()

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


class DrawingPanel
	constructor: (@layer, @shapeClass) ->
		#@shapes = []
		@current = null
		
		background = new Kinetic.Rect({
			fill: '#eeffee',
			width: @layer.getWidth(),
			height: @layer.getHeight()
		})
		#@layer.add(background)
		Widgets.addBorder @layer

	addShape: (@name, @tooltip) ->
		self = this
		
		@current = new @shapeClass()
		Widgets.addTooltip(@current.shape, tooltip)
		@wrapper = Widgets.createInteractiveFor(@current, @layer)
		
		@button = Widgets.createButton({
			#x: 100,
			#y: @layer.getHeight()-100,
			x: 50,
			y: -100,
			width: 100,
			text: 'Aceptar'
		})
		@button.on('mousedown', -> self.acceptedShape())

		@layer.add @button
		@layer.add @wrapper
		@layer.draw()

		@current.shape

	acceptedShape: ->
		# XXX: avoid error when mouseout arrives later
		@button.off('mouseover')
		@button.off('mouseout')
		@button.remove()
		@wrapper.remove()

		finalShape = @current.shape
		finalShape.setPosition(@wrapper.getPosition())
		@layer.add(finalShape)
		@layer.draw();
		@notifier(@name, finalShape, @current.size()) if @notifier != null


	setColor: (color) ->
		@current.shape.setStroke color
		@current.shape.draw()

	setNotifier: (@notifier) ->
		@layer.listening(@notifier != null)
		@layer.draw()


class ColorsPanel
	constructor: (@colors, @layer) ->
		@notifier = null;
		@buttons = [];

		position = 0;
		self = this;
		_.each(@colors, (color) ->
			rect = new Kinetic.Rect({
				x: position, y: 5,
				width: 20, height: 20,
				fill: color
			})
			rect.on('mousedown', -> self.notify(color))
			rect.on('mouseover', ->
				rect.setStroke('black')
				rect.setStrokeWidth(3)
				rect.draw()
			)
			rect.on('mouseout', ->
				rect.setStroke('transparent')
				rect.setStrokeWidth(0)
				rect.getParent().draw()
			)
			self.buttons.push(rect);
			self.layer.add(rect);
			position += 25;
		)

		@layer.draw()

	notify: (color) ->
		if (@notifier != null)
			@notifier(color)

	setNotifier: (@notifier) ->
		if (@notifier != null)
			@layer.show()
		else
			@layer.hide()
		@layer.draw()


class TextPanel
	constructor: (@layer) ->



@Panels ?= {}
_.merge(@Panels,
	Choose: ChoosePanel
	Drawing: DrawingPanel
	Colors: ColorsPanel
	Text: TextPanel
)