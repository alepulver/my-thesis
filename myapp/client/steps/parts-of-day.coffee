_ = lodash

partsOfDay = () ->
	choices = {
		morning: "Mañana",
		afternoon: "Tarde",
		night: "Noche",
	}
	create_panels = () -> Steps.createPanels choices, Steps.colors, Panels.Drawing, Widgets.Line
	step = new Steps.HandleControlFlow(create_panels, "parts-of-day")
	step

@Steps ?= {}
_.merge(@Steps, {
	partsOfDay: partsOfDay
})