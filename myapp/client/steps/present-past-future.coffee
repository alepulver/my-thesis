_ = lodash

presentPastFuture = () ->
	choices = {
		present: "Presente",
		past: "Pasado",
		future: "Futuro"
	}
	create_panels = () -> Steps.createPanels choices, Steps.colors, Panels.Drawing, Widgets.Circle
	step = new Steps.HandleControlFlow(create_panels, "present_past_future")
	step


@Steps ?= {}
_.merge(@Steps, {
	presentPastFuture: presentPastFuture
})
