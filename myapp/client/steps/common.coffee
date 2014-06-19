_ = lodash

class HandleCF
	constructor: (@create_panels, @name) ->
		# do nothing

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
		@workflow.stepFinished({
			results: @results,
			randomSeqs: @randomSeqs
		})

	choose_selectPeriod: (epoch) ->
		@panels.circles.addCircle(epoch, @epochs[epoch])
		@state = new CFStateModify this
		@state.start()

	modify_acceptCurrent: (name, circle) ->
		@results.push({
			position: circle.getPosition(),
			color: circle.stroke(),
			radius: circle.radius(),
			name: name
		})
		
		if @panels.choose.remaining > 0
			this.next()
		else
			this.finish()

	modify_changeColor: (color) ->
		@panels.circles.setColor color
		@panels.choose.colorSelected color


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
		panels.circles.setNotifier(null)

	selectPeriod: (epoch) ->
		@handler.choose_selectPeriod epoch


class CFStateModify extends CFState
	start: ->
		panels = @handler.panels
		handler = @handler

		panels.choose.setNotifier(null)
		panels.color.setNotifier((x) -> handler.state.changeColor x)
		panels.circles.setNotifier(
			(name, circle) -> handler.state.acceptCurrent(name, circle))

	changeColor: (color) ->
		@handler.modify_changeColor color
	
	acceptCurrent: (name, circle) ->
		@handler.modify_acceptCurrent name, circle


createPanels = (choices) ->
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
	colors = ['black', 'yellow', 'brown', 'violet', 'grey', 'red', 'green', 'blue']
	colors = _.shuffle(colors)
	color_menu = new Panels.Colors(colors, color_layer)
	stage.add(color_layer)

	circles_layer = new Kinetic.Layer({
		x: 0,
		y: 200,
		width: 800,
		height: 500
	})
	circles_panel = new Panels.Circles(circles_layer)
	stage.add(circles_layer)

	text_layer = new Kinetic.Layer({
		x: 0,
		y: 200,
		width: 800,
		height: 100
	})
	text_canvas = new Panels.Text(text_layer)
	#stage.add(text_layer)

	stage.draw()

	{choose: choose_panel, color: color_menu, circles: circles_panel, text: text_canvas, choices: choices}


@Steps ?= {}
_.merge(@Steps, {
	HandleControlFlow: HandleCF
	createPanels: createPanels
})