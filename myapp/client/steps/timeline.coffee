_ = lodash


createPanelsTimeline = (choices, orders, createShape) ->
	params = {
		x: 0,
		y: 0,
		width: 800,
		height: 800
	}

	layout =
		data:
			timeline: params
			drawing: params

	{
		timeline: new Panels.Timeline(layout)
		drawing: new Panels.Drawing(createShape, layout)
		choose: new Panels.ChooseExternal(choices, orders)
	}


timeline = () ->
	choices = {
		year_1900: "Año 1900",
		the_beatles: "The Beatles",
		my_birth: "Mi nacimiento",
		my_childhood: "Mi niñez",
		my_youth: "Mi juventud",
		today: "Hoy",
		my_third_age: "Mi vejez",
		year_2100: "Año 2100",
		wwii: "2da guerra mundial"
	}

	orders = [
		[
			'year_1900', 'wwii', 'the_beatles',
			'my_birth', 'my_childhood', 'my_youth',
			'today', 'my_third_age', 'year_2100'
		],
		[
			'today', 'wwii', 'my_youth',
			'my_birth', 'year_2100', 'the_beatles',
			'year_1900', 'my_childhood', 'my_third_age',
		]
	]

	create_shape = (item, panel) ->
		timeline = panel.handler.panels.timeline
		new Widgets.EventInTimelineIS(item, timeline, panel)

	panels = createPanelsTimeline(choices, orders, create_shape)
	
	new Steps.HandleTimelineControlFlow("timeline", panels)


@Steps ?= {}
_.merge(@Steps, {
	timeline
})