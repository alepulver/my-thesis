_ = lodash

currentTime = () ->
	(new Date()).getTime()


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
		@panels = @create_panels()
		@epochs = @panels.choices
		@results = {}
		@show_order = {
			colors: @panels.color.colors,
			choices: @panels.choose.keys
		}
		@selected_order = []
		this.next()

	next: ->
		@state = new CFStateChoose this
		@state.start()

	finish: ->
		if (@done)
			return
		@done = true
		@workflow.stepFinished({
			results: @results,
			show_order: @show_order.choices,
			color_order: @show_order.colors,
			selected_order: @selected_order,
			stage_as_json: @panels.stage.toJSON(),
			begin_click_time: @begin_click_time
		})

	choose_selectPeriod: (epoch) ->
		@current_result = {
			start_time: currentTime()
		}
		@selected_order.push(epoch)

		@panels.shapes.addShape(epoch, @epochs[epoch])
		@state = new CFStateModify this
		@state.start()

	modify_acceptCurrent: (name, data) ->
		@current_result['end_time'] = currentTime()
		_.merge(@current_result, data)
		@results[name] = @current_result
		
		if @panels.choose.remaining > 0
			this.next()
		else
			@state = new CFSStateFinish this
			@state.start()

	modify_changeColor: (color) ->
		@panels.shapes.setColor color
		@panels.choose.colorSelected color

	finish_selectExit: ->
		this.finish()


class CFState
	constructor: (@handler) ->
		# do nothing


class CFStateChoose extends CFState
	start: ->
		panels = @handler.panels
		handler = @handler
		
		panels.choose.setNotifier(
			(epoch) -> handler.state.selectPeriod epoch)
		panels.color.setNotifier(null)
		panels.shapes.setNotifier(null)

	selectPeriod: (epoch) ->
		@handler.choose_selectPeriod epoch


class CFStateModify extends CFState
	start: ->
		panels = @handler.panels
		handler = @handler

		panels.choose.setNotifier(null)
		panels.color.setNotifier((x) -> handler.state.changeColor x)
		panels.shapes.setNotifier(
			(name, data) -> handler.state.acceptCurrent(name, data))

	changeColor: (color) ->
		@handler.modify_changeColor color
	
	acceptCurrent: (name, data) ->
		@handler.modify_acceptCurrent name, data


class CFSStateFinish extends CFState
	start: ->
		panels = @handler.panels
		handler = @handler

		panels.choose.setNotifier(null)
		panels.color.setNotifier(null)
		panels.shapes.askFinish(-> handler.state.selectExit())

		$('#instructions').hide()
		$('#finished').show()
		#window.scrollTo(0,0)

	selectExit: ->
		@handler.finish_selectExit()


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