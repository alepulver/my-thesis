_ = lodash

class Shape
	#

class Circle extends Shape
	constructor: (circle) ->
		if (_.isUndefined(circle))
			@shape = new Kinetic.Circle({
				x: 0, y: 0,
				radius: 70,
				stroke: 'black', strokeWidth: 6,
				fill: 'transparent',
				name: 'image'
			})
		else
			@shape = circle
	size: ->
		{
			width: @shape.radius()*2,
			height: @shape.radius()*2
		}

	setSize: (size) ->
		radius = _.min([size.width, size.height])
		@shape.radius(radius)


class Rect extends Shape
	constructor: (rect) ->
		if (_.isUndefined(rect))
			@shape = new Kinetic.Rect({
				x: 0, y: 0,
				width: 100, height: 100,
				offsetX: 50, offsetY: 50,
				stroke: 'black', strokeWidth: 6,
				fill: 'transparent',
				name: 'image'
			})
		else
			@shape = rect

	size: ->
		@shape.size()


	setSize: (size) ->
		@shape.size({width: size.width*2, height: size.height*2})
		@shape.offsetX(size.width)
		@shape.offsetY(size.height)


class Line extends Shape
	constructor: (line) ->
		if (_.isUndefined(line))
			@shape = new Kinetic.Line({
				points: [-50, -50, 50, 50]
				x: 0, y: 0,
				width: 100, height: 100,
				offsetX: 50, offsetY: 50,
				stroke: 'black', strokeWidth: 6,
				fill: 'transparent',
				name: 'image'
			})
		else
			@shape = line

	size: ->
		@shape.size()


	setSize: (size) ->
		@shape.size(size)
		@shape.offsetX(size.width/2)
		@shape.offsetY(size.height/2)


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


createInteractiveFor = (commonShape, layer) ->
	shape = commonShape.shape
	group = new Kinetic.Group({
		x: layer.getWidth()/2,
		y: layer.getHeight()/2,
		draggable: true
	})

	group.dragBoundFunc((newPos) ->
		oldPos = this.getAbsolutePosition()
		constrainPosition(newPos, oldPos, commonShape)
	)

	shape.name('figure')
	group.add(shape)

	addAnchor(group, commonShape, 'topLeft')
	addAnchor(group, commonShape, 'topRight')
	addAnchor(group, commonShape, 'bottomLeft')
	addAnchor(group, commonShape, 'bottomRight')

	updateAllAnchors(group, commonShape)

	return group


constrainPosition = (newPos, oldPos, commonShape) ->
	size = commonShape.size()
	container = commonShape.shape.getLayer()

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
	if (size.width == Infinity)
		error()

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


updateAllAnchors = (group, commonShape) ->
	anchorNames = ['topLeft', 'topRight', 'bottomLeft', 'bottomRight']
	newPositions = anchorPositionsFor(commonShape.shape.getPosition(), commonShape.size())

	_.forEach(anchorNames, (name) ->
		pos = newPositions[name]
		anchor = group.find(".#{name}")[0].setPosition(pos)
	)

addAnchor = (group, commonShape, name) ->
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
		#result = constrainPosition(newPos, oldPos, new Widgets.Circle(this))

		center = group.getAbsolutePosition()
		size = {
			width: Math.abs(center.x - newPos.x),
			height: Math.abs(center.y - newPos.y)
		}

		positions = anchorPositionsFor(center, size)
		allInside = _.every(positions, (pos) ->
			blah = new Circle(anchor)
			!constrainPosition(pos, pos, blah).changed
		)
		if (allInside)
			commonShape.setSize(size)
			newPos
		else
			oldPos
	)
	anchor.on('dragmove', ->
		updateAllAnchors(group, commonShape)
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
	Circle: Circle
	Rect: Rect
	Line: Line
})