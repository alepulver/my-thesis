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

	askToPositionEvent: (name) ->
		$('#selection_panel').hide()
		self = this
		@current_start_time = Steps.currentTime()
		@current_event = name
		@selected_order.push(name)

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
			this.showFinish()

	showFinish: ->
		self = this
		@button = Tools.createButton({
			x: 50,
			y: 50,
			width: 100,
			text: 'Aceptar'
		})
		@button.on('mousedown', -> self.finishClicked())
		@layer.add @button
		@layer.draw()

	finishedShowingFinalPicture: ->
		###
		# XXX: avoid error when mouseout arrives later
		@button.off('mouseover')
		@button.off('mouseout')
		@button.remove()
		@layer.draw()
		###

		this.finish()


createPanelsTimeline = (choices, createShape) ->
	params = {
		x: 0,
		y: 0,
		width: 800,
		height: 800
	}

	layout =
		data:
			timeline: params
			drawing: params

	{
		timeline: new Panels.Timeline(layout)
		drawing: new Panels.Drawing(createShape, layout)
		choose: new Panels.ChooseExternal(choices)
	}


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

	create_shape = (item, panel) ->
		shape = new Kinetic.Wedge({
			x: 0, y: 0,
			radius: 200, angle: randBetween(30, 80),
			fill: 'black', stroke: 'black', strokeWidth: 0,
			rotation: randBetween(0, 360),
			opacity: 0.85
		})
		interactive_shape = new Widgets.RadialSectorIS(shape, item, panel, 200)
		interactive_shape

	panels = createPanelsTimeline(choices, create_shape)
	
	new Steps.HandleTimelineControlFlow("timeline", panels)


@Steps ?= {}
_.merge(@Steps, {
	timeline
})