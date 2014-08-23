_ = lodash

class QuestionsBegin
	constructor: ->
		@name = "questions_begining"
		self = this
		Template.questions_begining.events({
			'success.form.bv': (event, template) -> self.formSubmitted(event, template)
		})
		Template.questions_begining.askAddresses = ->
			return Config.askAddresses

	start: (@workflow) ->
		notSelected =
			message: 'No seleccionaste ninguna opción'
			callback: (value, validator) ->
				value != null
		
		$('form[id="myform"]').bootstrapValidator(
			feedbackIcons:
				valid: 'glyphicon glyphicon-ok'
				invalid: 'glyphicon glyphicon-remove'
				validating: 'glyphicon glyphicon-refresh'

			fields:
				name:
					validators:
						notEmpty:
							message: 'Por favor ingresá tu nombre, no es necesario el apellido'
				email:
					validators:
						emailAddress:
							message: 'No es una dirección de mail válida, puede omitirse si lo preferís'
				age:
					validators:
						notEmpty:
							message: 'Por favor ingresá tu edad'
				sex:
					validators:
						callback: notSelected
				studying:
					validators:
						callback: notSelected
				working:
					validators:
						callback: notSelected
		)

	formSubmitted: (event, template) ->
		event.preventDefault()

		results = {}
		variables = ['name', 'age']
		if (Config.askAddresses)
			variables += ['email', 'facebook', 'twitter']

		_.each(variables, (field) ->
			results[field] = template.find("input[id=#{field}]").value
		)
		variables = ['sex', 'studying', 'working']
		_.each(variables, (field) ->
			results[field] = template.find("select[id=#{field}]").value
		)

		###
		if (@alreadyDone results.email)
			Session.set("active_stage", "already_completed")
		else
			@workflow.stepFinished(results)
		###

		@workflow.stepFinished(results)

	alreadyDone: (email) ->
		if (email == "")
			false
		else
			pattern = {'stage': @name, 'results.email': email}
			already_done = Results.find(pattern).fetch()
			_.size(already_done) > 0


@Steps ?= {}
_.merge(@Steps, {
	QuestionsBegin: QuestionsBegin
})