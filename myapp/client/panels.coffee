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
			show_order: @keys,
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
		@last_event_time = 0

	addItem: (item) ->
		time = Tools.currentTime()

		if (@current != null)
			@current.unselect()

		@current = @createShape(item, this)
		@shapes[item.name] = @current
		@layer.draw()

		@events.push({time: time, type: 'add', arg: item.name, data: @current.results()})

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

	dragItem: (item, data) ->
		curr_time = data.time
		prev_time = @last_event_time
		@last_event_time = curr_time
		if (curr_time - prev_time < Config.max_event_rate)
			return
		@events.push({type: 'drag', arg: item.name, data: data})

	resizeItem: (item, data) ->
		curr_time = data.time
		prev_time = @last_event_time
		@last_event_time = curr_time
		if (curr_time - prev_time < Config.max_event_rate)
			return
		@events.push({type: 'resize', arg: item.name, data: data})

	setColor: (item, color) ->
		if (@current == null)
			return

		@events.push({time: Tools.currentTime(), type: 'color', arg: item.name, color: color})
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
		@events = []
		@line = new Widgets.LineInLayerIS(this)
		@button = Tools.createButton({
			x: 50,
			y: 50,
			width: 100,
			text: 'Aceptar'
		})
		@button.on('mousedown tap', -> self.finishedLineAdjustments())

		@layer.add @line.box
		@layer.add @line.group
		@layer.add @button
		@layer.draw()

	changeLine: (element) ->
		@events.push element

	finishedLineAdjustments: ->
		#@end_time = Tools.currentTime()
		@line.freeze()
		@data = @line.results()
		@line.box.remove()
		@button.visible(false)
		@layer.draw()

		@handler.timelineAccepted()
		
	results: ->
		{
			events: @events,
			results: @data
		}


class ChooseExternalPanel
	constructor: (@choices, orders) ->
		self = this

		@show_order = Tools.randBetween(0, _.size(orders)-1)
		@questions = orders[@show_order]
		@remaining = _.size(@choices)
		@events = []
		
		Template['timeline'].items = () ->
			_.map(self.questions, (key) ->
				{code: key, name: self.choices[key]})

	start: (@handler) ->
		self = this

		_.forEach(_.keys(@choices), (key) ->
			$("button##{key}").click(() ->
				#$("button##{key}").hide()
				$("button##{key}").css('visibility', 'hidden')
				self.itemStarted key
			)
		)

		$('#selection_panel').show()

	itemStarted: (key) ->
		@remaining--
		@events.push({time: Tools.currentTime(), type: 'choose', arg: key})
		@handler.itemAdded({name: key, description: @choices[key]})

		if (@remaining == 0)
			@showFinish()

	colorSelected: (color) ->
		#

	showFinish: ->
		self = this
		@button = Tools.createButton({
			x: 450,
			y: 50,
			width: 100,
			text: 'Aceptar'
		})
		@button.on('mousedown tap', -> self.finishClicked())

		# FIXME: make this better
		layer = @handler.panels.timeline.layer
		layer.add @button
		layer.draw()

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
			show_order: @show_order,
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