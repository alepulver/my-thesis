_ = lodash

class HandleCF
	constructor: (@stage) ->
		self = this
		@epochs = {
			present: "Presente",
			past: "Pasado",
			future: "Futuro"
		}
		@panels = createPanels @stage, @epochs
		@results = []
		@randomSeqs = {
			colors: @panels.color.colors,
			choices: @panels.choose.keys
		}

		@state = new CFStateChooseTime this
		@panels.choose.setNotifier((epoch) -> self.state.selectPeriod epoch)
		@panels.color.setNotifier(null)
		@panels.circles.setNotifier((name, circle) -> self.state.acceptCurrent(name, circle))



	chooseTime_selectPeriod: (epoch) ->
		self = this
		@panels.choose.setNotifier(null)
		@panels.color.setNotifier((x) -> self.state.changeColor x)
		@panels.circles.addCircle(epoch, @epochs[epoch])
		@state = new CFStateModifyCircle this

	modifyCircle_acceptCurrent: (name, circle) ->
		self = this
		@results.push({
			position: circle.getPosition(),
			color: circle.stroke(),
			radius: circle.radius(),
			name: name
		})
		#@panels.circles.layer.add(circle)
		#@stage.draw()
		#@panels.circles.layer.draw
		
		if @panels.choose.remaining > 0
			@state = new CFStateChooseTime this
			@panels.choose.setNotifier((x) -> self.state.selectPeriod x)
			@panels.color.setNotifier(null)
		else
			@state = new CFStateAskData this
			Session.set('active_stage', 'questions')

	modifyCircle_changeColor: (color) ->
		@panels.circles.setColor color
		@panels.choose.colorSelected color

	askData_inputDone: (inputs) ->
		Results.insert({
			questions: inputs,
			results: @results,
			randomSeqs: @randomSeqs
		})
		Session.set('active_stage', 'results')


class CFState
	constructor: (@handler) ->
		0


class CFStateChooseTime extends CFState
	selectPeriod: (epoch) ->
		@handler.chooseTime_selectPeriod epoch


class CFStateModifyCircle extends CFState
	changeColor: (color) ->
		@handler.modifyCircle_changeColor color
	
	acceptCurrent: (name, circle) ->
		@handler.modifyCircle_acceptCurrent name, circle


class CFStateAskData extends CFState
	inputDone: (input) ->
		@handler.askData_inputDone input

@csExport ?= {}
_.merge(@csExport, {
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
	colors = ['black', 'yellow', 'brown', 'violet', 'grey', 'red', 'green', 'blue']
	colors = _.shuffle(colors)
	color_menu = new ColorChooser(colors, color_layer)
	stage.add(color_layer)

	circles_layer = new Kinetic.Layer({
		x: 0,
		y: 200,
		width: 800,
		height: 500
	})
	circles_panel = new csExport.CirclesPanel(circles_layer)
	stage.add(circles_layer)

	text_layer = new Kinetic.Layer({
		x: 0,
		y: 200,
		width: 800,
		height: 100
	})
	text_canvas = new TextCanvas(text_layer)
	#stage.add(text_layer)

	stage.draw()

	{choose: choose_panel, color: color_menu, circles: circles_panel, text: text_canvas}
