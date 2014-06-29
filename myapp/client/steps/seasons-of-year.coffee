_ = lodash

seasonsOfYear = () ->
	choices = {
		winter: "Invierno",
		summer: "Verano",
		spring: "Primavera",
		autum: "Otoño"
	}

	create_shape = (layer) ->
		shape = new Widgets.Rect()
		interactive_shape = new Widgets.SquareBoundedIS(shape, layer)
		interactive_shape
	
	create_panels = Steps.create_handler_default(choices, create_shape)

	step = new Steps.HandleControlFlow(create_panels, "seasons_of_year")
	step

@Steps ?= {}
_.merge(@Steps, {
	seasonsOfYear: seasonsOfYear
})