_ = lodash

partsOfDay = () ->
	choices = {
		morning: "Mañana",
		afternoon: "Tarde",
		night: "Noche",
	}

	create_shape = (layer) ->
		shape = new Widgets.Circle()
		interactive_shape = new Widgets.SquareBoundedIS(shape, layer)
		interactive_shape

	create_panels = () ->
		panels = Steps.createPanels choices, Steps.colors, Panels.Drawing, create_shape
		
		layer = panels.shapes.layer
		circle = new Kinetic.Circle({
			x: layer.width/2, y: layer.height/2,
			radius: 200,
			stroke: 'black',
			strokeWidth: 2
		})
		layer.add circle

		panels

	step = new Steps.HandleControlFlow(create_panels, "parts_of_day")
	step

@Steps ?= {}
_.merge(@Steps, {
	partsOfDay: partsOfDay
})