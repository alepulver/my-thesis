_ = lodash

presentPastFuture = () ->
	epochs = {
		present: "Presente",
		past: "Pasado",
		future: "Futuro"
	}
	create_panels = () -> Steps.createPanels epochs
	step = new Steps.HandleControlFlow(create_panels, "present-past-future")
	step


@Steps ?= {}
_.merge(@Steps, {
	presentPastFuture: presentPastFuture
})
