_ = lodash

randBetween = (min, max) ->
	Math.floor(Math.random() * (max - min + 1)) + min

partsOfDay = () ->
	choices = {
		morning: "Mañana",
		afternoon: "Tarde",
		night: "Noche",
	}

	create_shape = (layer) ->
		shape = new Kinetic.Wedge({
			x: 0, y: 0,
			radius: 200, angle: randBetween(50, 80),
			fill: 'black', stroke: 'black', strokeWidth: 0,
			rotation: randBetween(-120, -90),
			opacity: 0.5
		})
		interactive_shape = new Widgets.RadialSectorIS(shape, layer, 200)
		interactive_shape

	create_panels = () ->
		panels = Steps.createPanels choices, Steps.colors, Panels.Drawing, create_shape
		
		layer = panels.shapes.layer
		circle = new Kinetic.Circle({
			x: layer.width()/2, y: layer.height()/2,
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