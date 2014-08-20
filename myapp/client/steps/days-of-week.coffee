_ = lodash

create_handler_default = (choices, create_shape) ->
	() ->
		panels = Steps.createPanels choices, Steps.colors, Panels.DrawingNoOverlap, create_shape
		
		layer = panels.shapes.layer
		Widgets.addBorder layer

		panels

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

	create_shape = (item, panel) ->
		shape = new Widgets.FilledRect()
		interactive_shape = new Widgets.SquareBoundedIS(shape, item, panel)
		interactive_shape
	
	panels = Steps.createPanels(choices, Steps.colors, Panels.DrawingNoOverlap, create_shape)
	
	new Steps.HandleControlFlow("days_of_week", panels)


@Steps ?= {}
_.merge(@Steps, {
	daysOfWeek: daysOfWeek
})