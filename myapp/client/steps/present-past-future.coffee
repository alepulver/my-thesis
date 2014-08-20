_ = lodash

presentPastFuture = () ->
	choices = {
		present: "Presente",
		past: "Pasado",
		future: "Futuro"
	}
	
	create_shape = (item, panel) ->
		shape = new Widgets.Circle()
		interactive_shape = new Widgets.SquareBoundedIS(shape, item, panel)
		interactive_shape

	panels = Steps.createPanels(choices, Steps.colors, Panels.Drawing, create_shape)
	
	new Steps.HandleControlFlow("present_past_future", panels)


@Steps ?= {}
_.merge(@Steps, {
	presentPastFuture: presentPastFuture
})
