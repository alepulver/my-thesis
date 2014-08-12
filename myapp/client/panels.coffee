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
			button.on('mousedown tap', -> self.itemStarted(key))
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
	constructor: (@layer, @createShape) ->
		@current = null
		@shapes = []

	###
	selectItem: (@name, tooltip) ->
		if (_.has(@shapes, @name))
			@addShape @name, tooltip
		else
			@current = @shapes[@name]

	###

	addShape: (@name, tooltip) ->
		self = this
	
		@current = @createShape(@layer)
		@shapes.push @current
		@current.addTooltip(tooltip)
		
		@button = Widgets.createButton({
			x: 50,
			y: -100,
			width: 100,
			text: 'Aceptar'
		})
		@button.on('mousedown tap', -> self.acceptedShape())

		@layer.add @button
		@layer.add @current.group
		@layer.draw()

		@current

	acceptedShape: ->
		# XXX: avoid error when mouseout arrives later
		@button.off('mouseover')
		@button.off('mouseout')
		@button.remove()

		result = @current.fixState()
		@notifier(@name, result) # if @notifier != null

	###
	askAccept: ->
		@button = Widgets.createButton({
			x: 450,
			y: -100,
			width: 100,
			text: 'Aceptar'
		})
		@button.on('mousedown tap', -> self.acceptedShape())

		@layer.add @button		
	###

	setColor: (color) ->
		@current.setColor color
		@layer.draw()

	setNotifier: (@notifier) ->
		@layer.listening(@notifier != null)
		@layer.draw()

	askFinish: (@end_notifier) ->
		self = this

		_.forEach(@shapes, (x) ->
			x.unselect()
		)
		
		@button = Widgets.createButton({
			x: 50,
			y: -100,
			width: 100,
			text: 'Continuar'
		})
		@button.on('mousedown tap', -> self.finishClicked())

		@layer.add @button
		@layer.draw()

	finishClicked: ->
		# XXX: avoid error when mouseout arrives later
		@button.off('mouseover')
		@button.off('mouseout')
		@button.remove()
		@layer.draw()

		@end_notifier()


class DrawingPanelNoOverlap extends DrawingPanel
	noIntersections: ->
		self = this

		rectForShape = (thing) ->
			cs = thing.commonShape
			{
				x: cs.shape.getAbsolutePosition().x,
				y: cs.shape.getAbsolutePosition().y,
				width: cs.width(),
				height: cs.height()
			}

		haveToExit = false
		_.forEach(self.shapes, (shapeOne) ->
			rectOne = rectForShape shapeOne

			_.forEach(self.shapes, (shapeTwo) ->
				if (shapeOne != shapeTwo)
					rectTwo = rectForShape shapeTwo
					if (Widgets.rectCollision rectOne, rectTwo)
						# XXX: return binds locally
						haveToExit = true
						return
			)
		)
		!haveToExit


	acceptedShape: ->
		if (this.noIntersections())
			super()
		else
			alert("Las figuras no pueden superponerse, por favor ubícala en otro lugar")


class ColorsPanel
	constructor: (@colors, @layer) ->
		@notifier = null
		@buttons = []

		position = 0
		horizMax = 4
		currentHoriz = 0
		offsetY = 0

		self = this;
		_.each(@colors, (color) ->
			rect = new Kinetic.Rect({
				x: position, y: offsetY + 10,
				width: 30, height: 30,
				fill: color
			})
			rect.on('mousedown tap', -> self.notify(color))
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
			position += 40;
			currentHoriz++

			if (currentHoriz == horizMax)
				currentHoriz = 0
				offsetY += 40
				position = 0
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


class SliderChoosePanel
	constructor: (@questions, @layer) ->
		@current_index = 0
		@choices = _.shuffle(@questions)
		@remaining = _.size(@choices)
		@data = {
			show_order: @choices,
			results: {}
		}
	
	start: (@notifier) ->
		self = this
		@gui_items = []
		offset = 0
		
		_.forEach(@choices, (choice) ->
			group = new Kinetic.Group({
				x: self.layer.width()/2,
				y: offset + 75
			})

			item = new Widgets.inputSlider(group, choice)

			self.layer.add group
			self.gui_items.push(item)
			offset += 160
		)
		self.layer.draw()

		this.askForClick()

	finish: ->
		@notifier(@data)

	askForClick: ->
		self = this
		@current_result = {
			start_time: Steps.currentTime()
		}
		@gui_items[@current_index].enable((position) -> self.sliderClicked position)

	sliderClicked: (position) ->
		_.merge(@current_result, {
			end_time: Steps.currentTime(),
			value: position
		})
		@data.results[@choices[@current_index]] = @current_result

		@current_index++
		@remaining--

		if (@remaining > 0)
			this.askForClick()
		else
			this.finish()


class TextPanel
	constructor: (@layer) ->


@Panels ?= {}
_.merge(@Panels,
	Choose: ChoosePanel
	Drawing: DrawingPanel
	DrawingNoOverlap: DrawingPanelNoOverlap
	Colors: ColorsPanel
	Text: TextPanel
	SliderChoose: SliderChoosePanel
)