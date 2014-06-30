_ = lodash

class HandleTimelineCF
	constructor: (@choices, @colors, @name) ->
		# do nothing

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
		@stage.add(@layer)

		@results = []
		@randomSeqs = {
			#colors: @panels.color.colors,
			#choices: @panels.choose.keys
		}
		this.askLineAdjustments()


	askLineAdjustments: ->
		self = this
		@line = new Widgets.LineInCircleIS(@layer)
		@button = Widgets.createButton({
			x: 50,
			y: 50,
			width: 100,
			text: 'Aceptar'
		})
		@button.on('mousedown', -> self.finishedLineAdjustments())

		@layer.add @line.group
		@layer.add @button
		@layer.draw()

	finishedLineAdjustments: ->
		# XXX: avoid error when mouseout arrives later
		@button.off('mouseover')
		@button.off('mouseout')
		@button.remove()

		results = @line.fixState()
		this.askToPositionEvent()

	askToPositionEvent: ->
		@layer.on('mousemove', ->
			stage = this.getStage()
			pos = stage.getPointerPosition()
			console.log(pos)
		)
		@layer.on('mousedown', ->
			stage = this.getStage()
			pos = stage.getPointerPosition()
			console.log(pos)
		)
		#


	finishedPositioningEvent: (data) ->
		@layer.off('mousemove')
		@layer.off('mousedown')

		@results.push({
			position: shape.getPosition(),
			color: shape.stroke(),
			size: size,
			name: name
		})
		remaining--
		if @remaining > 0
			this.askToPositionEvent()
		else
			this.showFinalPicture()

	showFinalPicture: ->
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

		this.askSubjectData()

	askSubjectData: ->
		self = this
		Template.experiment_questions.events({
			'submit form': (event, template) ->
				self.finishedAskingSubjectData(event, template)
		})
		Session.set("stage_questions", true)

	finishedAskingSubjectData: (event, template) ->
		event.preventDefault()
		this.finish()

	finish: ->
		@workflow.stepFinished({
			results: @results,
			randomSeqs: @randomSeqs
		})


timeline = () ->
	choices = [
		"el origen del universo",
		"el origen de la vida",
		"el nacimiento de Jesucristo",
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