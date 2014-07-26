_ = lodash

class QuestionsHowForced
	constructor: ->
		@name = "questions_how_forced"
		self = this

	start: (@workflow) ->
		self = this
		@choices = ['Tamaño', 'Ubicación', 'Color']
		@stage = new Kinetic.Stage({
			container: 'container',
			width: 800, height: 800
		})
		@layer = new Kinetic.Layer({
			x: 0,
			y: 0,
			width: 800,
			height: 800
		})
		@panel = new Panels.SliderChoose @choices, @layer
		@stage.add(@layer)
		@panel.start((results) -> self.ended results)

	ended: (results) ->
		results['stage_as_json'] = @stage.toJSON()
		@workflow.stepFinished(results)


@Steps ?= {}
_.merge(@Steps, {
	QuestionsHowForced
})