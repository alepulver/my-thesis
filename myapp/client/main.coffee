_ = lodash

startMainApp = ->
	local_id = ReactiveStore.get("local_id") || ""
	if (local_id == "")
		ReactiveStore.set("local_id", Random.secret())

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


@startMainApp = startMainApp


class Workflow
	constructor: (@steps, @finishNotifier) ->
		# do nothing

	start: ->
		@local_id = ReactiveStore.get("local_id")
		@current_index = -1
		@results = {}
		@results['start_time'] = Steps.currentTime()
		this.nextStep()

	finish: ->
		@results['finish_time'] = Steps.currentTime()
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
			@current_start_time = Steps.currentTime()

			Template[@current_step.name].rendered = () ->
				self.preStart()
				self.current_step.start(self)

			Session.set("active_stage", @current_step.name)

	stepFinished: (results) ->
		end_time = Steps.currentTime()

		Results.insert({
			participant: Session.get("current_user"),
			stage: @current_step.name,
			start_time: @current_start_time,
			end_time: end_time,
			local_id: @local_id,
			results: results
		})

		if @current_index >= _.size(@steps)-1
			this.finish()
		else
			this.nextStep()

