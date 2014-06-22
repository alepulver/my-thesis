_ = lodash

partsOfDay = () ->
	choices = {
		morning: "Mañana",
		afternoon: "Tarde",
		night: "Noche",
	}
	colors = ['black', 'yellow', 'brown', 'violet', 'grey', 'red', 'green', 'blue']
	create_panels = () -> Steps.createPanels choices, colors, Panels.Drawing, Widgets.Line
	step = new Steps.HandleControlFlow(create_panels, "parts-of-day")
	step

@Steps ?= {}
_.merge(@Steps, {
	partsOfDay: partsOfDay
})