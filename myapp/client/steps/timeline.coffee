_ = lodash

class HandleTimelineCF
	constructor: (@choices, @colors, @name) ->
		@done = false

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
		@background = new Kinetic.Rect({
			x: 0, y: 0,
			width: 800, height: 800
		})
		@stage.add @layer
		@layer.add @background

		@results = []
		@randomSeqs = {
			#colors: @panels.color.colors,
			#choices: @panels.choose.keys
		}
		this.askLineAdjustments()

	askLineAdjustments: ->
		self = this
		@remaining = _.size(@choices)
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
		self = this
		group = new Kinetic.Rect({
			#
		})
		@current = new Kinetic.Rect({
			x: 0, y: -15,
			width: 5,
			height: 30,
			fill: 'red'
		})
		@line.group.add @current
		@correct = false
		@layer.draw()

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
			inRange = (x) ->
				dist = self.line.shape.points()[2]
				(-dist < projection and dist > projection)

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

		###
		@results.push({
			position: shape.getPosition(),
			color: shape.stroke(),
			size: size,
			name: name
		})
		###
		@remaining--
		if @remaining > 0
			this.askToPositionEvent()
		else
			this.showFinalPicture()

	showFinalPicture: ->
		self = this
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
		@layer.draw()

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
		if (@done)
			return
		@done = true
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