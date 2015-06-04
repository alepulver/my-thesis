_ = lodash


questionsBegin = ->
  # FIXME: does not work because of updating later
	###
	current_user = Session.get("current_user") || "none"
	if (current_user == "none")
		new QuestionsBegin()
	else
		new QuestionsBeginTEDX()
	###
	new QuestionsBeginTEDX()


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
		variables = ['name', 'age', 'email']
		if (Config.askAddresses)
			variables += ['facebook', 'twitter']

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


class QuestionsBeginTEDX
	constructor: ->
		@name = "questions_begining"

	start: (@workflow) ->
		@readVariables()

	readVariables: ->
		url_params = Session.get("url_params")
		console.log(url_params)

		get_param = (name) ->
			if (_.isUndefined(url_params[name]))
				"none"
			else
				url_params[name]

		variables = {'name': 'name', 'age': 'age', 'sex': 'sex', 'studying': 'study', 'working': 'work'}
		results = {}
		_.forEach(_.keys(variables), (key) ->
			results[key] = get_param variables[key]
		)
		@workflow.stepFinished(results)


@Steps ?= {}
_.merge(@Steps, {
	questionsBegin
})
