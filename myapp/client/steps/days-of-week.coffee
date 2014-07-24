_ = lodash

daysOfWeek = () ->
	choices = {
		monday: "Lunes",
		tuesday: "Martes",
		wednesday: "Miércoles",
		thursday: "Jueves",
		friday: "Viernes",
		saturday: "Sábado",
		sunday: "Domingo"
	}

	create_shape = (layer) ->
		shape = new Widgets.FilledRect()
		interactive_shape = new Widgets.SquareBoundedIS(shape, layer)
		interactive_shape
	
	create_panels = Steps.create_handler_default(choices, create_shape)

	step = new Steps.HandleControlFlow(create_panels, "days_of_week")
	step

@Steps ?= {}
_.merge(@Steps, {
	daysOfWeek: daysOfWeek
})