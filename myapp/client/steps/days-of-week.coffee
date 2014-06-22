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
	colors = ['black', 'yellow', 'brown', 'violet', 'grey', 'red', 'green', 'blue']
	create_panels = () -> Steps.createPanels choices, colors, Panels.Drawing, Widgets.Rect
	step = new Steps.HandleControlFlow(create_panels, "days-of-week")
	step

@Steps ?= {}
_.merge(@Steps, {
	daysOfWeek: daysOfWeek
})