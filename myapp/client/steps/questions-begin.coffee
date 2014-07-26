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

		results = {}
		variables = ['name', 'age', 'email']
		_.each(variables, (field) ->
			results[field] = template.find("input[name=#{field}]").value
		)
		variables = ['sex', 'studying', 'working']
		_.each(variables, (field) ->
			results[field] = template.find("select[name=#{field}]").value
		)

		if (@alreadyDone results.email)
			Session.set("active_stage", "already_completed")
		else
			@workflow.stepFinished(results)

	alreadyDone: (email) ->
		if (email == "")
			false
		else
			already_done = Results.find({'stage': @name, 'results.email': email}).fetch()
			_.size(already_done) > 0


@Steps ?= {}
_.merge(@Steps, {
	QuestionsBegin: QuestionsBegin
})