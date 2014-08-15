_ = lodash

currentTime = () ->
	now = new Date()
	now.getTime()


colors = ['black', 'yellow', 'saddlebrown', 'darkviolet', 'grey', 'red', 'green', 'blue']


class HandleCF
	constructor: (@create_panels, @name) ->
		@done = false

	changeState: (stateClass) ->
		@state = new stateClass this
		@state.start()

	start: (@workflow) ->
		self = this
		button = $('#start')
		button.click(() ->
			self.begin_click_time = currentTime()
			button.hide()
			self.beginExperiment()
		)
		# XXX: just to fill space so that screen elements don't resize later
		Steps.createStage()

	beginExperiment: ->
		self = this
		@panels = @create_panels(self)
		@panels.color.show()
		@panels.choose.show()
		@panels.shapes.show()

	finish: ->
		# XXX: avoid double entry in case template events collide
		if (@done)
			return
		@done = true

		@workflow.stepFinished({
			colors: @panels.color.results(),
			choose: @paners.choose.results(),
			shapes: @panels.shapes.results(),
			stage_as_json: @panels.stage.toJSON(),
			begin_click_time: @begin_click_time
		})

	itemAdded: (item) ->
		@panels.shapes.addShape item

	colorSelected: (color) ->
		@panels.shapes.setColor color
		@panels.choose.colorSelected color

	drawingAccepted: ->
		$('#instructions').hide()
		$('#finished').show()
		#window.scrollTo(0,0)

	continuePressed: ->
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
	stage = createStage()

	choose_layer = new Kinetic.Layer({
		x: 0,
		y: 0,
		width: 400,
		height: 200
	})
	choose_panel = new Panels.Choose(choices, choose_layer)
	stage.add(choose_layer)

	color_layer = new Kinetic.Layer({
		x: 400,
		y: 0,
		width: 400,
		height: 200
	})

	colors = _.shuffle(colors)
	color_menu = new Panels.Colors(colors, color_layer)
	stage.add(color_layer)

	shapes_layer = new Kinetic.Layer({
		x: 0,
		y: 200,
		width: 800,
		height: 500
	})
	shapes_panel = new drawingPanelClass(shapes_layer, createShape)
	stage.add(shapes_layer)

	text_layer = new Kinetic.Layer({
		x: 0,
		y: 200,
		width: 800,
		height: 100
	})
	text_canvas = new Panels.Text(text_layer)
	#stage.add(text_layer)

	stage.draw()

	{
		choose: choose_panel,
		color: color_menu,
		shapes: shapes_panel,
		text: text_canvas,
		choices: choices,
		stage: stage
	}


create_handler_default = (choices, create_shape) ->
	() ->
		panels = Steps.createPanels choices, Steps.colors, Panels.Drawing, create_shape
		
		layer = panels.shapes.layer
		Widgets.addBorder layer

		panels


@Steps ?= {}
_.merge(@Steps, {
	HandleControlFlow: HandleCF
	createPanels
	colors
	create_handler_default
	currentTime
	createStage
})