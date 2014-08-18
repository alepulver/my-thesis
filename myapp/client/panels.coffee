_ = lodash


class Panel
	start: (@handler) ->
		@handler.stage.add @layer

	hide: ->
		@layer.visible(false)

	show: ->
		@layer.visible(true)


class ChoosePanel extends Panel
	constructor: (choices, @layout) ->
		self = this

		@layer = new Kinetic.Layer(@layout.data.choose)
		@choices = _.mapValues(choices, (text) ->
			{text: text, button: null, dot: null}
		)
		@remaining = _.size(@choices)
		@current = null
		@events = []
		
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
			button = Tools.createButton({
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

	itemStarted: (key) ->
		@events.push({time: Tools.currentTime(), type: 'choose', arg: key})

		@remaining--

		@choices[key].dot.fill('black')
		@choices[key].button.listening(false)
		@choices[key].button.find('.background')[0].fill('#bbb')
		@layer.draw()

		@handler.itemAdded({name: key, description: @choices[key].text})

		if (@remaining == 0)
			@showFinish()

	colorSelected: (item, color) ->
		shape = @choices[item.name].dot
		shape.fill(color)
		shape.getParent().draw()

	showFinish: ->
		self = this
		@button = Tools.createButton({
			x: 450,
			y: 135,
			width: 100,
			text: 'Aceptar'
		})
		@button.on('mousedown tap', -> self.finishClicked())
		@layer.add @button
		@layer.draw()

	finishClicked: ->
		###
		# XXX: avoid error when mouseout arrives later
		@button.off('mouseover')
		@button.off('mouseout')
		@button.remove()
		@layer.draw()
		###

		@handler.drawingAccepted()

	results: ->
		{
			events: @events
		}


class DrawingPanel extends Panel
	constructor: (@createShape, @layout) ->
		@layer = new Kinetic.Layer(@layout.data.drawing)
		Tools.addBorder @layer
		@current = null
		@ignore_select = false
		@shapes = {}
		@events = []

	addItem: (item) ->
		@events.push({time: Tools.currentTime(), type: 'add', arg: item.name})

		if (@current != null)
			@current.unselect()

		@current = @createShape(item, this)
		@shapes[item.name] = @current
		@layer.draw()

		@current

	selectItem: (item) ->
		if (@ignore_select)
			return

		@events.push({time: Tools.currentTime(), type: 'select', arg: item.name})

		if (@current != null)
			@current.unselect()

		@current = @shapes[item.name]
		@current.select()
		@layer.draw()
		@handler.itemSelected item

	setColor: (color) ->
		@current.setColor color
		@layer.draw()

	freeze: ->
		@current.unselect()
		@current = null
		@ignore_select = true
		@layer.draw()

	results: ->
		data = _.mapValues(@shapes, (shape) -> shape.results())
		{
			events: @events,
			shapes: data
		}

	arrangementValid: ->
		true


class DrawingPanelNoOverlap extends DrawingPanel
	noIntersections: ->
		self = this

		rectForShape = (thing) ->
			cs = thing.commonShape
			{
				x: thing.group.getAbsolutePosition().x,
				y: thing.group.getAbsolutePosition().y,
				width: cs.width(),
				height: cs.height()
			}

		haveToExit = false
		_.forEach(self.shapes, (shapeOne) ->
			rectOne = rectForShape shapeOne

			_.forEach(self.shapes, (shapeTwo) ->
				if (shapeOne != shapeTwo)
					rectTwo = rectForShape shapeTwo
					if (Tools.rectCollision rectOne, rectTwo)
						# XXX: return binds locally
						haveToExit = true
						return
			)
		)
		!haveToExit

	arrangementValid: ->
		if (this.noIntersections())
			true
		else
			alert("Las figuras no pueden superponerse, por favor ubícala en otro lugar")
			false


class ColorsPanel extends Panel
	constructor: (@colors, @layout) ->
		@layer = new Kinetic.Layer(@layout.data.color)
		@events = []
		@buttons = []

		position = 0
		horizMax = 4
		currentHoriz = 0
		offsetY = 0

		self = this
		_.each(@colors, (color) ->
			rect = new Kinetic.Rect({
				x: position, y: offsetY + 10,
				width: 30, height: 30,
				fill: color
			})
			rect.on('mousedown tap', ->
				self.events.push({time: Tools.currentTime(), type: 'color', arg: color})
				self.handler.colorSelected(color)
			)
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

	results: ->
		{
			events: @events
		}


class TimelinePanel extends Panel
	constructor: (@layout) ->
		@layer = new Kinetic.Layer(@layout.data.timeline)
		@askLineAdjustments()

	askLineAdjustments: ->
		self = this
		@position = 0
		@line = new Widgets.LineInLayerIS(@layer)
		@button = Tools.createButton({
			x: 50,
			y: 50,
			width: 100,
			text: 'Aceptar'
		})
		@button.on('mousedown', -> self.finishedLineAdjustments())

		@layer.add @line.box
		@layer.add @line.group
		@layer.add @button
		@layer.draw()

	finishedLineAdjustments: ->
		@end_time = Tools.currentTime()

		data = @line.fixState()
		@line.box.remove()
		_.merge(@result_line, data)
		@handler.timelineAccepted()
		
	results: ->
		@data


class ChooseExternalPanel extends Panel
	constructor: (choices) ->
		self = this

		@choices = _.mapValues(choices, (text) ->
			0
		)
		@remaining = _.size(@choices)
		@current = null
		@events = []
		
		# ...

	itemStarted: (key) ->
		@events.push({time: Tools.currentTime(), type: 'choose', arg: key})

		@remaining--

		@choices[key].dot.fill('black')
		@choices[key].button.listening(false)
		@choices[key].button.find('.background')[0].fill('#bbb')
		@layer.draw()

		@handler.itemAdded({name: key, description: @choices[key].text})

		if (@remaining == 0)
			@showFinish()

	colorSelected: (color) ->
		shape = @choices[@active_item].dot
		shape.fill(color)
		shape.getParent().draw()

	showFinish: ->
		self = this
		@button = Tools.createButton({
			x: 450,
			y: 135,
			width: 100,
			text: 'Aceptar'
		})
		@button.on('mousedown tap', -> self.finishClicked())
		@layer.add @button
		@layer.draw()

	finishClicked: ->
		###
		# XXX: avoid error when mouseout arrives later
		@button.off('mouseover')
		@button.off('mouseout')
		@button.remove()
		@layer.draw()
		###

		@handler.drawingAccepted()

	results: ->
		{
			events: @events
		}


@Panels ?= {}
_.merge(@Panels,
	Choose: ChoosePanel
	ChooseExternal: ChooseExternalPanel
	Drawing: DrawingPanel
	DrawingNoOverlap: DrawingPanelNoOverlap
	Colors: ColorsPanel
	Timeline: TimelinePanel
)