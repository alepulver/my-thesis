_ = lodash

class QuestionsBegin
	constructor: ->
		@name = "questions_begining"
		self = this
		Template.questions_begining.events({
			'submit form': (event, template) -> self.formSubmitted(event, template)
		})

	start: (@workflow) ->
		# do nothing

	formSubmitted: (event, template) ->
		event.preventDefault()

		variables = ['name', 'age', 'sex', 'studying', 'working']
		results = {}
		_.each(variables, (field) ->
			results[field] = template.find("input[name=#{field}]").value
		)
    
		@workflow.stepFinished(results)


@Steps ?= {}
_.merge(@Steps, {
	QuestionsBegin: QuestionsBegin
})