_ = lodash

class Introduction
	constructor: ->
		@name = "introduction"
		self = this
		Template.introduction.events({
			'click #start': (event, template) -> self.startPressed(event, template)
		})

	start: (@workflow) ->
		# do nothing

	startPressed: (event, template) ->
		event.preventDefault()
		@workflow.stepFinished({})


@Steps ?= {}
_.merge(@Steps, {
	Introduction: Introduction
})