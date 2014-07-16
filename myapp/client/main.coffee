_ = lodash

startMainApp = ->
	# TODO: record date, step permutation order, etc
	steps = [
		new Steps.Introduction(),
		#new Steps.QuestionsBegin(),
		#Steps.presentPastFuture(),
		#Steps.seasonsOfYear(),
		#Steps.daysOfWeek(),
		Steps.partsOfDay(),
		#Steps.timeline(),
		new Steps.QuestionsEnd()
	]

	workflow = new Workflow(steps, finishedMainApp)
	workflow.start()


finishedMainApp = (results) ->
	# TODO: add IP, date, etc
	Results.insert(results)
	Session.set("active_stage", "thanks")


@startMainApp = startMainApp
#@finishedMainApp = finishedMainApp

# TODO: time each stage
class Workflow
	constructor: (@steps, @finishNotifier) ->
		# do nothing
	start: ->
		@current_index = -1
		@results = {}
		this.nextStep()

	finish: ->
		@finishNotifier(@results)

	nextStep: ->
			self = this
			@current_index++
			assert(@current_index < _.size(@steps), "Workflow: nextStep index")
			@current_step = @steps[@current_index]

			Template[@current_step.name].rendered = () ->
				self.current_step.start(self)

			Session.set("active_stage", @current_step.name)

	stepFinished: (results) ->
		@results[@current_step.name] = results
		if @current_index >= _.size(@steps)-1
			this.finish()
		else
			this.nextStep()

