_ = lodash

class HandleTimelineCF
	constructor: (@choices, @colors, @name) ->
		self = this
		@done = false
		@questions = _.keys(@choices)
		if (Math.random() < 0.5)
			# XXX: JS doesn't have seed, try "seedrandom"
			@questions = [
				'today',
				'life',
				'my_birth',
				'renaissance',
				'universe',
				'my_childhood',
				'year_one',
				'my_youth',
				'beatles',
				'my_third_age'
			]

		@selected_order = []
		Template[@name].items = () ->
			_.map(self.questions, (key) ->
				{code: key, name: self.choices[key]})

	changeState: (stateClass) ->
		@state = new stateClass this
		@state.start()

	start: (@workflow) ->
		self = this
		$('#start').click(() ->
			$('#start').hide()
			self.begin_click_time = Steps.currentTime()
			self.beginExperiment()
		)
		_.forEach(@questions, (key) ->
			$("button##{key}").click(() ->
				$("button##{key}").hide()
				self.askToPositionEvent key
			)
		)
		# XXX: just to fill space so that screen elements don't resize later
		Steps.createStage()

	beginExperiment: ->
		#$('#start').hide()
		@stage = Steps.createStage()
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
			choices: @questions
		}
		this.askLineAdjustments()

	finish: ->
		if (@done)
			return
		@done = true
		@workflow.stepFinished({
			results: @results,
			line: @result_line,
			#color_order: @show_order.colors,
			show_order: @show_order.choices,
			selected_order: @selected_order,
			stage_as_json: @stage.toJSON(),
			begin_click_time: @begin_click_time
		})

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
		
		$('#selection_panel').show()
		#this.askToPositionEvent()

	askToPositionEvent: (name) ->
		$('#selection_panel').hide()
		self = this
		@current_start_time = Steps.currentTime()
		@current_event = name
		@selected_order.push(name)

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
			text: @choices[name],
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
			###
			inRange = (x) ->
				dist = self.line.shape.points()[2]
				(-dist < projection and dist > projection)
			###
			inRange = (x) -> true
			dist = self.line.shape.points()[2]
			projection = Widgets.constrainBetween(projection, -dist, dist)

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

		@results[@current_event] = {
			start_time: @current_start_time,
			end_time: Steps.currentTime(),
			position: @current.x() / @line.shape.points()[2]
		}

		@remaining--
		@position++
		if @remaining > 0
			$('#selection_panel').show()
		else
			this.showFinalPicture()

	showFinalPicture: ->
		self = this
		@button = Widgets.createButton({
			x: 50,
			y: 50,
			width: 100,
			text: 'Continuar'
		})
		@button.on('mousedown', -> self.finishedShowingFinalPicture())
		@layer.add @button
		@layer.draw()

		$('#instructions').hide()
		$('#finished').show()
		#window.scrollTo(0,0)

	finishedShowingFinalPicture: ->
		# XXX: avoid error when mouseout arrives later
		@button.off('mouseover')
		@button.off('mouseout')
		@button.remove()
		@layer.draw()

		this.finish()


timeline = () ->
	choices = {
		universe: "el origen del universo",
		life: "el origen de la vida",
		year_one: "el año 1 (hoy es 2014)",
		renaissance: "el Renacimiento",
		beatles: "los Beatles",
		my_birth: "mi nacimiento",
		my_childhood: "mi niñez",
		my_youth: "mi juventud",
		today: "hoy",
		my_third_age: "mi vejez"
	}

	step = new HandleTimelineCF(choices, Steps.colors, "timeline")
	step

@Steps ?= {}
_.merge(@Steps, {
	timeline
})