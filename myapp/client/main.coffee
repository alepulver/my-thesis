_ = lodash

startMainApp = ->
	local_id = ReactiveStore.get("local_id") || ""
	if (local_id == "")
		ReactiveStore.set("local_id", Random.secret())

	Session.set("current_experiment", Meteor.uuid())

	steps = [
		new Steps.Introduction(),
		new Steps.QuestionsBegin(),
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
		#HTTP.call("POST", "http://api.twitter.com/xyz",
		#	{data: @results}, (error, result) -> true)
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
			# FIXME: remove "participant", as it can be obtained from the introduction of every experiment
			participant: Session.get("current_user"),
			experiment: Session.get("current_experiment"),
			stage: @current_step.name,
			start_time: @current_start_time,
			end_time: end_time,
			results: results
		}
		Results.insert(step_results)
		@results.push(step_results)

		if @current_index >= _.size(@steps)-1
			this.finish()
		else
			this.nextStep()

