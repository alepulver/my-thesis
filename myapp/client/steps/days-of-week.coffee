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
	create_panels = () -> Steps.createPanels choices, Steps.colors, Panels.Drawing, Widgets.Rect
	step = new Steps.HandleControlFlow(create_panels, "days_of_week")
	step

@Steps ?= {}
_.merge(@Steps, {
	daysOfWeek: daysOfWeek
})