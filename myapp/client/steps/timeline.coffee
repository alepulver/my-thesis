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
		universe: "el origen del universo",
		life: "el origen de la vida",
		year_one: "el año 1 (hoy es 2014)",
		renaissance: "el Renacimiento",
		beatles: "los Beatles",
		my_birth: "mi nacimiento",
		my_childhood: "mi niñez",
		my_youth: "mi juventud",
		today: "hoy",
		my_third_age: "mi vejez"
	}

	orders = [
		[
			'universe', 'life', 'year_one', 'renaissance', 'beatles', 'my_birth',
			'my_childhood', 'my_youth', 'today', 'my_third_age'
		],
		[
			'today', 'life', 'my_birth', 'renaissance', 'universe',
			'my_childhood', 'year_one', 'my_youth', 'beatles', 'my_third_age'
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