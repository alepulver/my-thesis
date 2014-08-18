_ = lodash


colors = ['black', 'yellow', 'saddlebrown', 'darkviolet', 'grey', 'red', 'green', 'blue']


class HandleCF
	constructor: (@name, @panels) ->
		@done = false

	start: (@workflow) ->
		self = this

		# XXX: fill space now so that screen elements don't resize later
		@stage = createStage()

		$('#start').click(() ->
			self.begin_click_time = Tools.currentTime()
			$('#start').hide()
			self.beginExperiment()
		)

	beginExperiment: ->
		@panels.color.start(this)
		@panels.choose.start(this)
		@panels.drawing.start(this)
		@stage.draw()

	finish: ->
		# XXX: avoid double entry in case template events collide
		if (@done)
			return
		@done = true

		@workflow.stepFinished({
			colors: @panels.color.results(),
			choose: @panels.choose.results(),
			drawing: @panels.drawing.results(),
			stage_as_json: @stage.toJSON(),
			begin_click_time: @begin_click_time,
			accept_click_time: @accept_click_time
		})

	itemAdded: (item) ->
		@panels.drawing.addItem item
		@current_item = item

	itemSelected: (item) ->
		@current_item = item

	colorSelected: (color) ->
		@panels.drawing.setColor @current_item, color
		@panels.choose.colorSelected @current_item, color

	drawingAccepted: ->
		if (@panels.drawing.arrangementValid())
			@accept_click_time = Tools.currentTime()
			self = this
			@finish()


class HandleTimelineCF
	constructor: (@name, @panels) ->
		@done = false

	start: (@workflow) ->
		self = this

		# XXX: fill space now so that screen elements don't resize later
		@stage = createStage()

		$('#start').click(() ->
			self.begin_click_time = Tools.currentTime()
			$('#start').hide()
			self.beginExperiment()
		)

	beginExperiment: ->
		@panels.choose.start(this)
		@panels.timeline.start(this)
		@stage.draw()

	finish: ->
		# XXX: avoid double entry in case template events collide
		if (@done)
			return
		@done = true

		@workflow.stepFinished({
			timeline: @panels.timeline.results(),
			drawing: @panels.drawing.results(),
			stage_as_json: @stage.toJSON(),
			begin_click_time: @begin_click_time,
			accept_click_time: @accept_click_time
		})

	timelineAccepted: ->
		@panels.timeline.hide()
		@panels.drawing.start(this)

	itemAdded: (item) ->
		@panels.drawing.addItem item

	drawingAccepted: ->
		if (@panels.drawing.arrangementValid())
			@accept_click_time = Tools.currentTime()
			self = this
			@finish()


createStage = () ->
	width = $('#main-content').width()
	height = $(window).height() - 150
	#size = Math.min(width, height)
	# FIXME: need proportions instead of pixels to be used when drawing
	size = 800

	new Kinetic.Stage({
		container: 'container',
		width: size, height: size,
		scale: {x: size/800, y: size/800}
	})


createPanels = (choices, colors, drawingPanelClass, createShape) ->
	layout = new Layout()
	choose = new Panels.Choose(choices, layout)
	color = new Panels.Colors(colors, layout)
	drawing = new drawingPanelClass(createShape, layout)

	{
		choose
		color
		drawing
	}


class Layout
	constructor: ->
		@data =
			choose:
				x: 0
				y: 0
				width: 400
				height: 200
			color:
				x: 400
				y: 0
				width: 400
				height: 200
			drawing:
				x: 0
				y: 200
				width: 800
				height: 500
			text:
				x: 0
				y: 200
				width: 800
				height: 100


@Steps ?= {}
_.merge(@Steps, {
	HandleControlFlow: HandleCF
	HandleTimelineControlFlow: HandleTimelineCF
	createPanels
	colors
})