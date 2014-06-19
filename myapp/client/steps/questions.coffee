_ = lodash

class Questions
	constructor: ->
		@name = "questions"
		self = this
		Template.questions.events({
			'submit form': (event, template) -> self.formSubmitted(event, template)
		})

	start: (@workflow) ->
		# do nothing

	formSubmitted: (event, template) ->
		event.preventDefault()

		variables = ['name', 'age', 'sex', 'studying', 'working', 'daynight']
		results = {}
		_.each(variables, (field) ->
			results[field] = template.find("input[name=#{field}]")
		)
		results['comments'] = template.find("textarea[name=comments]")
    
		@workflow.stepFinished(results)


@Steps ?= {}
_.merge(@Steps, {
	Questions: Questions
})