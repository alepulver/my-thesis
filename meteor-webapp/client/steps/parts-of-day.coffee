_ = lodash

randBetween = (min, max) ->
	Math.floor(Math.random() * (max - min + 1)) + min

partsOfDay = () ->
	choices = {
		morning: "Mañana",
		afternoon: "Tarde",
		night: "Noche",
	}

	create_shape = (item, panel) ->
		shape = new Kinetic.Wedge({
			x: 0, y: 0,
			radius: 200, angle: randBetween(30, 80),
			fill: 'black', stroke: 'black', strokeWidth: 0,
			rotation: randBetween(0, 360),
			opacity: 0.85
		})
		interactive_shape = new Widgets.RadialSectorIS(shape, item, panel, 200)
		interactive_shape

	add_circle = (panel) ->
		layer = panel.layer
		circle = new Kinetic.Circle({
			x: layer.width()/2, y: layer.height()/2,
			radius: 200,
			stroke: 'black',
			strokeWidth: 2
		})
		layer.add circle

	panels = Steps.createPanels(choices, Steps.colors, Panels.Drawing, create_shape)
	add_circle panels.drawing
	
	new Steps.HandleControlFlow("parts_of_day", panels)


@Steps ?= {}
_.merge(@Steps, {
	partsOfDay: partsOfDay
})