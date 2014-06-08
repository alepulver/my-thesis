_ = lodash

class TimeRep
	constructor: (@name) ->
		@color = 'black'
		@shape = null


class HandleCF
	constructor: (@stage) ->
		self = this
		@epochs = {
			present: "Present",
			past: "Past",
			future: "Future"
		}
		@panels = createPanels @stage, @epochs

		@state = new CFStateChooseTime this
		@panels.choose.setNotifier((x) -> self.state.selectPeriod x)

	chooseTime_selectPeriod: (epoch) ->
		self = this
		@panels.choose.setNotifier(null)
		@panels.color.setNotifier((x) -> self.state.changeColor x)
		@panels.circles.new_circle(null, (x) -> self.state.acceptCurrent x)
		@state = new CFStateModifyCircle this

	modifyCircle_acceptCurrent: (circle) ->
		self = this
		@panels.circles.layer.add(circle)
		@stage.draw()
		#@panels.circles.layer.draw
		
		if @panels.choose.remaining > 0
			@state = new CFStateChooseTime this
			@panels.choose.setNotifier((x) -> self.state.selectPeriod x)

	modifyCircle_changeColor: (color) ->
		@panels.circles.setColor color
		@panels.choose.setColor color

	askData_inputDone: (input) ->
		0


class CFState
	constructor: (@handler) ->
		0


class CFStateChooseTime extends CFState
	selectPeriod: (epoch) ->
		@handler.chooseTime_selectPeriod epoch


class CFStateModifyCircle extends CFState
	changeColor: (color) ->
		@handler.modifyCircle_changeColor color
	
	acceptCurrent: (circle) ->
		@handler.modifyCircle_acceptCurrent circle


class CFStateAskData extends CFState
	inputDone: (input) ->
		@handler.askData_inputDone input

@csExport ?= {}
_.merge(@csExport, {
	TimeRep: TimeRep,
	HandleCF: HandleCF
})


createPanels = (stage, choices) ->
	choose_layer = new Kinetic.Layer({
		x: 0,
		y: 0,
		width: 400,
		height: 200
	})
	choose_panel = new csExport.ChoosePanel(choices, choose_layer)
	stage.add(choose_layer)

	color_layer = new Kinetic.Layer({
		x: 400,
		y: 0,
		width: 400,
		height: 200
	})
	color_menu = new ColorChooser(['#ff0000', '#00ff00', '#0000ff'], color_layer)
	stage.add(color_layer)

	circles_layer = new Kinetic.Layer({
		x: 0,
		y: 300,
		width: 800,
		height: 500
	})
	circles_canvas = new CanvasForCircles(circles_layer)
	stage.add(circles_layer)

	text_layer = new Kinetic.Layer({
		x: 0,
		y: 200,
		width: 800,
		height: 100
	})
	text_canvas = new TextCanvas(text_layer)
	stage.add(text_layer)

	stage.draw()

	{choose: choose_panel, color: color_menu, circles: circles_canvas, text: text_canvas}
