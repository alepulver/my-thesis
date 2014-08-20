_ = lodash

seasonsOfYear = () ->
	choices = {
		winter: "Invierno",
		summer: "Verano",
		spring: "Primavera",
		autum: "Otoño"
	}

	create_shape = (item, panel) ->
		shape = new Widgets.Rect()
		interactive_shape = new Widgets.SquareBoundedIS(shape, item, panel)
		interactive_shape
	
	panels = Steps.createPanels(choices, Steps.colors, Panels.Drawing, create_shape)
	
	new Steps.HandleControlFlow("seasons_of_year", panels)


@Steps ?= {}
_.merge(@Steps, {
	seasonsOfYear: seasonsOfYear
})