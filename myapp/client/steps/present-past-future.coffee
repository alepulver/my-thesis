_ = lodash

presentPastFuture = () ->
	choices = {
		present: "Presente",
		past: "Pasado",
		future: "Futuro"
	}
	
	create_shape = (layer) ->
		shape = new Widgets.Circle()
		interactive_shape = new Widgets.SquareBoundedIS(shape, layer)
		interactive_shape

	create_panels = Steps.create_handler_default(choices, create_shape)
	
	step = new Steps.HandleControlFlow(create_panels, "present_past_future")
	step


@Steps ?= {}
_.merge(@Steps, {
	presentPastFuture: presentPastFuture
})
