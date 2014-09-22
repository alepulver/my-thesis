_ = lodash

startMainApp = ->
	local_id = ReactiveStore.get("local_id") || ""
	if (local_id == "")
		ReactiveStore.set("local_id", Random.secret())

	Session.set("current_experiment", Meteor.uuid())

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
		if (Config.secondary_save)
			jQuery.post('http://tedx.cloudapp.net/experiments/create/',
				test_subject: "experimentos completos"
				experiment_name: "tedxcircles_experiments"
				experiment_log: JSON.stringify(@results)
			)
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
		@results.push(step_results)

		if (Config.secondary_save)
			jQuery.post('http://tedx.cloudapp.net/experiments/create/',
				test_subject: "etapas intermedias de los experimentos"
				experiment_name: "tedxcircles_stages"
				experiment_log: JSON.stringify(step_results)
			)

		if @current_index >= _.size(@steps)-1
			this.finish()
		else
			this.nextStep()

