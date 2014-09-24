_ = lodash

startMainApp = ->
	local_id = ReactiveStore.get("local_id") || ""
	if (local_id == "")
		ReactiveStore.set("local_id", Random.secret())

	Session.set("current_experiment", Meteor.uuid())

	startResultsThing()

	steps = [
		new Steps.Introduction(),
		Steps.questionsBegin(),
		Steps.presentPastFuture(),
		Steps.seasonsOfYear(),
		Steps.daysOfWeek(),
		Steps.partsOfDay(),
		Steps.timeline(),
		new Steps.QuestionsEnd()
	]

	workflow = new Workflow(steps, finishedMainApp)
	workflow.start()


# XXX: ask why this does not work the "easy" way
startResultsThing = ->
	Template.results.rendered = ->
		Meteor.call('getSummary', (err, val) ->
			Session.set('summary', val))
	
	Template.results.data = ->
		Session.get('summary')


finishedMainApp = (results) ->
	Session.set("active_stage", "thanks")
	#Results.insert({complete: true, results: results})


@startMainApp = startMainApp


class Workflow
	constructor: (@steps, @finishNotifier) ->
		# do nothing

	start: ->
		@current_index = -1
		@results = []
		this.nextStep()

	finish: ->
		@externalSave('tedxcircles_experiments', @results)
		@finishNotifier(@results)

	preStart: ->
		if ($('.navbar').height() > 60)
			$('.navbar').hide()
			$('body').css('padding-top', 0)

	nextStep: ->
			self = this
			@current_index++
			assert(@current_index < _.size(@steps), "Workflow: nextStep index")
			@current_step = @steps[@current_index]
			@current_start_time = Tools.currentTime()

			Template[@current_step.name].rendered = () ->
				self.preStart()
				self.current_step.start(self)

			Session.set("active_stage", @current_step.name)

	stepFinished: (results) ->
		end_time = Tools.currentTime()

		step_results = {
			experiment: Session.get("current_experiment"),
			stage: @current_step.name,
			start_time: @current_start_time,
			end_time: end_time,
			results: results
		}
		Results.insert(step_results)
		@externalSave('tedxcircles_stages', step_results)
		
		@results.push(step_results)


		if @current_index >= _.size(@steps)-1
			this.finish()
		else
			this.nextStep()

	externalSave: (name, data) ->
		if (Config.secondary_save)
			contents =
				test_subject: "no sirve"
				experiment_name: name
				experiment_log: JSON.stringify(data)

			request = jQuery.ajax(
				url: "http://tedx.cloudapp.net/experiments/create/"
				type: "POST"
				data: JSON.stringify(contents)
				contentType: "application/json; charset=utf-8"
			)
			#request.fail((jqXHR, message) -> alert("Request failed: " + message))
