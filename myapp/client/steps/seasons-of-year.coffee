_ = lodash

seasonsOfYear = () ->
	choices = {
		winter: "Invierno",
		summer: "Verano",
		spring: "Primavera",
		autum: "Otoño"
	}
	colors = ['black', 'yellow', 'brown', 'violet', 'grey', 'red', 'green', 'blue']
	create_panels = () -> Steps.createPanels choices, colors, Panels.Drawing, Widgets.Rect
	step = new Steps.HandleControlFlow(create_panels, "seasons-of-year")
	step

@Steps ?= {}
_.merge(@Steps, {
	seasonsOfYear: seasonsOfYear
})