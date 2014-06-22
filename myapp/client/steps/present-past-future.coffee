_ = lodash

presentPastFuture = () ->
	choices = {
		present: "Presente",
		past: "Pasado",
		future: "Futuro"
	}
	colors = ['black', 'yellow', 'brown', 'violet', 'grey', 'red', 'green', 'blue']
	create_panels = () -> Steps.createPanels choices, colors, Panels.Drawing, Widgets.Circle
	step = new Steps.HandleControlFlow(create_panels, "present-past-future")
	step


@Steps ?= {}
_.merge(@Steps, {
	presentPastFuture: presentPastFuture
})
