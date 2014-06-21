_ = lodash

createButton = (parameters) ->
	group = new Kinetic.Group({
		x: parameters.x,
		y: parameters.y,
	})

	text = new Kinetic.Text({
		text: parameters.text,
		fontSize: 15,
		fontFamily: 'Calibri',
		fill: '#555',
		width: parameters.width,
		padding: 10,
		align: 'center',
		name: 'text'
	})

	rect = new Kinetic.Rect({
		stroke: '#555',
		strokeWidth: 2,
		fill: '#ddd',
		width: parameters.width,
		height: text.height(),
		name: 'background',
		cornerRadius: 10
	})

	group.on('mouseover', ->
		rect.setStrokeWidth(5)
		group.getParent().draw()
	)
	group.on('mouseout', ->
		rect.setStrokeWidth(2)
		group.getParent().draw()
	)

	group.add(rect)
	group.add(text)
	group.height(rect.height())

	group


addBorder = (layer) ->
	border = new Kinetic.Line({
		points: [0, 0, layer.width(), 0, layer.width(), layer.height(), 0, layer.height(), 0, 0],
		dash: [20, 5],
		stroke: 'black',
		strokeWidth: 5
	})
	layer.add border
	layer.draw()


addTooltip = (shape, text) ->
	widget = new Kinetic.Text({
		text: text,
		fontSize: 17, fontFamily: 'Calibri',
		width: 100,
		align: 'center'
	})
  
	shape.on('mouseover', ->
		parent = this.getParent()
		widget.setPosition({
			x: this.getPosition().x - widget.getWidth()/2,
			y: this.getPosition().y - (this.getHeight()/2 + 30)
		})
		widget.fill(this.stroke())
		parent.add(widget)
		parent.draw()
	)
  
	shape.on('mouseout', ->
		widget.remove()
		this.getParent().getParent().draw()
	)


createInteractiveFor = (shape, layer) ->
	group = new Kinetic.Group({
		x: layer.getWidth()/2,
		y: layer.getHeight()/2,
		draggable: true
	})

	group.dragBoundFunc((newPos) ->
		oldPos = this.getAbsolutePosition()
		constrainPosition(newPos, oldPos, this, null)
	)

	shape.name('figure')
	group.add(shape)

	addAnchor(group, 'topLeft')
	addAnchor(group, 'topRight')
	addAnchor(group, 'bottomLeft')
	addAnchor(group, 'bottomRight')

	updateAllAnchors(group)

	return group


constrainPosition = (newPos, oldPos, group, blah) ->
	#size = group.find('.figure')[0].size()
	radius = group.find('.figure')[0].radius()
	size = null
	if (blah == null)
		size = {width: radius*2, height: radius*2}
	else
		size = blah
	container = group.find('.figure')[0].getLayer()

	objectTopLeft = {
		x: (newPos.x - size.width/2),
		y: (newPos.y - size.height/2)
	}  

	containerPos = container.getAbsolutePosition()
	containerTopLeft = {
		x: (containerPos.x - container.offsetX()),
		y: (containerPos.y - container.offsetY())
	}

	result = {x: newPos.x, y: newPos.y, changed: false}

	beforeFirst = objectTopLeft.x < containerTopLeft.x
	afterLast = objectTopLeft.x + size.width > containerTopLeft.x + container.getWidth()
	ignoreX = beforeFirst || afterLast
	if (ignoreX)
		result.x = oldPos.x
		result.changed = true

	aboveFirst = objectTopLeft.y < containerTopLeft.y
	belowLast = objectTopLeft.y + size.height > containerTopLeft.y + container.getHeight()
	ignoreY = aboveFirst || belowLast
	if (ignoreY)
		result.y = oldPos.y
		result.changed = true

	result


anchorPositionsFor = (center, size) ->
	{
		topLeft: {
			x: center.x - size.width/2,
			y: center.y - size.height/2
		},
		topRight: {
			x: center.x + size.width/2,
			y: center.y - size.height/2
		},
		bottomLeft: {
			x: center.x - size.width/2,
			y: center.y + size.height/2
		},
		bottomRight: {
			x: center.x + size.width/2,
			y: center.y + size.height/2
		}
	}


updateAllAnchors = (group) ->
	anchorNames = ['topLeft', 'topRight', 'bottomLeft', 'bottomRight']
	figure = group.find('.figure')[0]
	newPositions = anchorPositionsFor(figure.getPosition(), figure.size())
	
	_.forEach(anchorNames, (name) ->
		pos = newPositions[name]
		anchor = group.find(".#{name}")[0].setPosition(pos)
	)

addAnchor = (group, name) ->
	stage = group.getStage()
	layer = group.getLayer()

	anchor = new Kinetic.Circle({
		stroke: '#666',
		fill: '#ddd',
		strokeWidth: 2,
		radius: 8,
		name: name,
		draggable: true
	})

	anchor.dragBoundFunc((newPos) ->
		oldPos = this.getAbsolutePosition()
		result = constrainPosition(newPos, oldPos, group, null)

		center = group.getAbsolutePosition()
		radius = _.max([Math.abs(center.x - newPos.x), Math.abs(center.y - newPos.y)])
		size = {width: radius*2, height: radius*2}
		if (radius < 5)
			return oldPos

		positions = anchorPositionsFor(center, size)
		allInside = _.every(positions, (pos) ->
			console.log(pos)
			!constrainPosition(pos, pos, group, {width: 10, height: 10}).changed
		)
		if (allInside)
			#group.find('.figure')[0].size(size)
			group.find('.figure')[0].radius(radius)
			newPos
		else
			oldPos
	)
	anchor.on('dragmove', ->
		updateAllAnchors(group)
		layer.draw()
	)
	anchor.on('mousedown touchstart', ->
		group.setDraggable(false)
	)
	anchor.on('dragend', ->
		group.setDraggable(true)
	)


	# add hover styling
	anchor.on('mouseover', ->
		layer = this.getLayer()
		document.body.style.cursor = 'pointer'
		this.setStrokeWidth(4)
		this.getParent().draw()
	)
	anchor.on('mouseout', ->
		layer = this.getLayer()
		document.body.style.cursor = 'default'
		this.strokeWidth(2)
		this.getParent().draw()
	)

	group.add(anchor)
	anchor


@Widgets ?= {}
_.merge(@Widgets, {
	createButton: createButton
	createInteractiveFor: createInteractiveFor
	addBorder: addBorder
	addTooltip: addTooltip
})