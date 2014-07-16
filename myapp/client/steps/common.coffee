_ = lodash

colors = ['black', 'yellow', 'brown', 'darkviolet', 'grey', 'red', 'green', 'blue']

class HandleCF
	constructor: (@create_panels, @name) ->
		@done = false

	changeState: (stateClass) ->
		@state = new stateClass this
		@state.start()

	start: (@workflow) ->
		@panels = @create_panels()
		@epochs = @panels.choices
		@results = []
		@randomSeqs = {
			colors: @panels.color.colors,
			choices: @panels.choose.keys
		}
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
			randomSeqs: @randomSeqs
		})

	choose_selectPeriod: (epoch) ->
		@panels.shapes.addShape(epoch, @epochs[epoch])
		@state = new CFStateModify this
		@state.start()

	modify_acceptCurrent: (name, shape, size) ->
		@results.push({
			position: shape.getPosition(),
			color: shape.stroke(),
			size: size,
			name: name
		})
		
		if @panels.choose.remaining > 0
			this.next()
		else
			@state = new CFSStateFinish this
			@state.start()

	modify_changeColor: (color) ->
		@panels.shapes.setColor color
		@panels.choose.colorSelected color

	finish_selectExit: ->
		self = this
		# TODO: draw bar and wait for click
		#self.finishedAskingSubjectData(event, template)

	questions_submitForm: (template) ->
		#event.preventDefault()
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
			(name, shape) -> handler.state.acceptCurrent(name, shape))

	changeColor: (color) ->
		@handler.modify_changeColor color
	
	acceptCurrent: (name, shape, size) ->
		@handler.modify_acceptCurrent name, shape, size


class CFSStateFinish extends CFState
	start: ->
		panels = @handler.panels
		handler = @handler

		panels.choose.setNotifier(null)
		panels.color.setNotifier(null)
		panels.shapes.askFinish(-> handler.state.selectExit())

	selectExit: ->
		@handler.finish_selectExit()


createPanels = (choices, colors, drawingPanelClass, createShape) ->
	stage = new Kinetic.Stage({
		container: 'container',
		width: 800,	height: 800
	})

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

	{choose: choose_panel, color: color_menu, shapes: shapes_panel, text: text_canvas, choices: choices}


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
})