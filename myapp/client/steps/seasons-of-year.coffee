_ = lodash

seasonsOfYear = () ->
	epochs = {
		winter: "Invierno",
		summer: "Verano",
		spring: "Primavera",
		autum: "Otoño"
	}
	create_panels = () -> Steps.createPanels epochs
	step = new Steps.HandleControlFlow(create_panels, "seasons-of-year")
	step

@Steps ?= {}
_.merge(@Steps, {
	seasonsOfYear: seasonsOfYear
})