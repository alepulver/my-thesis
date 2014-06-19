_ = lodash

startMainApp = ->
	steps = [
		new Steps.Introduction(),
		new Steps.PresentPastFuture(),
		#Steps.SeasonsOfYear,
		new Steps.Questions(),
		new Steps.Thanks()
	]

	workflow = new Workflow(steps, () -> true)
	workflow.start()

@startMainApp = startMainApp

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

			#@current_step.start(this)
			alert(@current_step.name)
			Template[@current_step.name].rendered = () ->
				alert(self.current_step.name)
				self.current_step.start(self)

			Session.set("active_stage", @current_step.name)

	stepFinished: (results) ->
		@results[@current_step.name] = results
		if @current_index >= _.size(@steps)
			this.finish()
		else
			this.nextStep()

