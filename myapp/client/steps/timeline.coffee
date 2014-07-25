_ = lodash

class HandleTimelineCF
	constructor: (@questions, @colors, @name) ->
		self = this
		@done = false
		@choices = _.shuffle(@questions)
		Template[@name].items = () ->
			self.choices

	changeState: (stateClass) ->
		@state = new stateClass this
		@state.start()

	start: (@workflow) ->
		@stage = new Kinetic.Stage({
			container: 'container',
			width: 800,	height: 800
		})
		@layer = new Kinetic.Layer({
			x: 0,
			y: 0,
			width: 800,
			height: 800
		})
		@background = new Kinetic.Rect({
			x: 0, y: 0,
			width: 800, height: 800
		})
		@stage.add @layer
		@layer.add @background

		@results = {}
		@show_order = {
			#colors: @panels.color.colors,
			choices: @choices
		}
		this.askLineAdjustments()

	askLineAdjustments: ->
		self = this
		@current_start_time = Steps.currentTime()
		@position = 0
		@remaining = _.size(@choices)
		@line = new Widgets.LineInLayerIS(@layer)
		@button = Widgets.createButton({
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
		# XXX: avoid error when mouseout arrives later
		@button.off('mouseover')
		@button.off('mouseout')
		@button.remove()

		@result_line = {
			start_time: @current_start_time,
			end_time: Steps.currentTime()
		}
		
		data = @line.fixState()
		@line.box.remove()
		_.merge(@result_line, data)
		
		this.askToPositionEvent()

	askToPositionEvent: ->
		self = this
		@current_start_time = Steps.currentTime()

		group = new Kinetic.Group({
		})
		bar = new Kinetic.Rect({
			x: 0, y: -15,
			width: 5,
			height: 30,
			fill: 'red'
		})
		rightSide = (Math.random() < 0.5)
		text = new Kinetic.Text({
			text: @choices[@position],
			fontSize: 15,
			fontFamily: 'Calibri',
			fill: '#555',
			width: 200,
			align: if (rightSide) then 'left' else 'right'
		})

		transform = text.getTransform()
		rotation = Widgets.degreesInRange @line.group.rotation()
		invert = if (rotation > 0 && rotation < 180) then -1 else 1
		transform.rotate(Widgets.degreesToRadians(90*invert))
		if (rightSide)
			transform.translate(30, 0)
		else
			transform.translate(-30-text.width(), 0)
		transform.translate(0, -10)

		group.add bar
		group.add text
		@current = group

		@line.group.add @current
		@correct = false
		@layer.draw()

		@background.moveToTop()
		@background.on('mousemove', ->
			stage = this.getStage()
			pos = stage.getPointerPosition()

			center = self.line.group.getAbsolutePosition()
			vector = {
				x: pos.x - center.x,
				y: pos.y - center.y
			}
			polarVector = Widgets.cartesianToPolar vector
			projection = Widgets.polarToCartesian({
				angle: polarVector.angle - self.line.group.rotation(),
				length: polarVector.length
			}).x
			inRange = (x) ->
				dist = self.line.shape.points()[2]
				(-dist < projection and dist > projection)

			if (inRange(projection))
				self.correct = true
				self.current.x(projection)
				self.layer.draw()
			else
				self.correct = false
		)
		@background.on('mousedown', ->
			if (self.correct)
				self.finishedPositioningEvent()
		)

	finishedPositioningEvent: ->
		@background.off('mousemove')
		@background.off('mousedown')

		@results[@choices[@position]] = {
			start_time: @current_start_time,
			end_time: Steps.currentTime(),
			position: @current.x() / @line.shape.points()[2]
		}

		@remaining--
		@position++
		if @remaining > 0
			this.askToPositionEvent()
		else
			this.showFinalPicture()

	showFinalPicture: ->
		self = this
		@button = Widgets.createButton({
			x: 50,
			y: 50,
			width: 100,
			text: 'Finalizar'
		})
		@button.on('mousedown', -> self.finishedShowingFinalPicture())
		@layer.add @button
		@layer.draw()

	finishedShowingFinalPicture: ->
		# XXX: avoid error when mouseout arrives later
		@button.off('mouseover')
		@button.off('mouseout')
		@button.remove()
		@layer.draw()

		this.finish()

	finish: ->
		if (@done)
			return
		@done = true
		@workflow.stepFinished({
			results: @results,
			line: @result_line,
			#color_order: @show_order.colors,
			show_order: @show_order.choices
		})


timeline = () ->
	choices = [
		"el origen del universo",
		"el origen de la vida",
		"el año 1 (hoy es 2014)",
		"el Renacimiento",
		"los Beatles",
		"mi nacimiento",
		"mi niñez",
		"mi juventud",
		"hoy",
		"mi vejez"
	]

	step = new HandleTimelineCF(choices, Steps.colors, "timeline")
	step

@Steps ?= {}
_.merge(@Steps, {
	timeline
})