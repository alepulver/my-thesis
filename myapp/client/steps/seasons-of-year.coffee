_ = lodash

seasonsOfYear = () ->
	choices = {
		winter: "Invierno",
		summer: "Verano",
		spring: "Primavera",
		autum: "Otoño"
	}
	create_panels = () -> Steps.createPanels choices, Steps.colors, Panels.Drawing, Widgets.Rect
	step = new Steps.HandleControlFlow(create_panels, "seasons_of_year")
	step

@Steps ?= {}
_.merge(@Steps, {
	seasonsOfYear: seasonsOfYear
})