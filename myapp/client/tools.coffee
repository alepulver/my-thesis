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

	makeHoverable group, rect

	group.add(rect)
	group.add(text)
	group.height(rect.height())

	group


addBorder = (layer) ->
	###
	border = new Kinetic.Line({
		points: [0, 0, layer.width(), 0, layer.width(), layer.height(), 0, layer.height(), 0, 0],
		dash: [20, 5],
		stroke: 'black',
		strokeWidth: 5
	})
	###
	border = new Kinetic.Rect({
		x: 2, y: 2,
		width: layer.width()-4, height: layer.height()-2,
		stroke: 'grey', strokeWidth: 4,
		fill: 'transparent'
	})
	layer.add border
	layer.draw()


defaultPosFunc = (widget, shape) ->
	{
		x: shape.getPosition().x,
		y: shape.getPosition().y - (shape.getHeight()/2 + 30)
	}


addTooltip = (shape, text, positionFunc = defaultPosFunc) ->
	widget = new Kinetic.Text({
		text: text,
		fontSize: 18, fontFamily: 'Calibri',
		width: 100,
		align: 'center',
		offsetX: 50
	})

	shape.on('mouseover', ->
		parent = this.getParent()
		widget.setPosition(positionFunc(widget, this))
		color = this.stroke()
		if (color == 'yellow')
			color = 'gold'
		widget.fill(color)
		parent.add(widget)
		parent.draw()
	)

	shape.on('mouseout', ->
		widget.remove()
		this.getParent().getParent().draw()
	)


boundingBoxPositionsFor = (shape) ->
	{
		topLeft: {
			x: shape.x - shape.width/2,
			y: shape.y - shape.height/2
		},
		topRight: {
			x: shape.x + shape.width/2,
			y: shape.y - shape.height/2
		},
		bottomLeft: {
			x: shape.x - shape.width/2,
			y: shape.y + shape.height/2
		},
		bottomRight: {
			x: shape.x + shape.width/2,
			y: shape.y + shape.height/2
		}
	}


boundingBoxFits = (shape, container) ->
	shapeBB = boundingBoxPositionsFor shape
	adjustedContainer = {
		x: container.x + container.width/2,
		y: container.y + container.height/2,
		width: container.width,
		height: container.height
	}
	containerBB = boundingBoxPositionsFor adjustedContainer

	isLeft = shapeBB.topLeft.x < containerBB.topLeft.x
	isRight = shapeBB.bottomRight.x > containerBB.bottomRight.x
	isUp = shapeBB.topLeft.y < containerBB.topLeft.y
	isDown = shapeBB.bottomRight.y > containerBB.bottomRight.y

	isHorizontalOff = isLeft || isRight
	isVerticalOff = isUp || isDown
	
	{
		x: !isHorizontalOff,
		y: !isVerticalOff,
		all: !(isHorizontalOff || isVerticalOff)
	}


rectCollision = (rect1, rect2) ->
	right = rect2.x > rect1.x+rect1.width
	left = rect2.x+rect2.width < rect1.x
	down = rect2.y > rect1.y+rect1.height
	up = rect2.y+rect2.height < rect1.y

	!(right || left || down || up)


constrainedPosUpdate = (shape, container, newPos) ->
	newShape = {
		x: newPos.x,
		y: newPos.y,
		width: shape.width,
		height: shape.height
	}
	result = boundingBoxFits newShape, container
	
	{
		x: (if result.x then newPos.x else shape.x),
		y: (if result.y then newPos.y else shape.y)
	}


makeHoverable = (group, shape) ->
	# add hover styling
	group.on('mouseover', ->
		#layer = this.getLayer()
		document.body.style.cursor = 'pointer'
		shape.strokeWidth(4)
		shape.getLayer().draw()
	)
	group.on('mouseout', ->
		#layer = this.getLayer()
		document.body.style.cursor = 'default'
		shape.strokeWidth(2)
		shape.getLayer().draw()
	)


constrainBetween = (x, min, max) ->
	if (x < min)
		min
	else if (x > max)
		max
	else
		x


degreesInRange = (degrees) ->
	# XXX: KineticJS angles can be negative
	while (degrees < 0)
		degrees += 360
	while (degrees >= 360)
		degrees -= 360
	degrees


angleDifference = (one, two) ->
	diffAngle = two - one
	while (diffAngle < -180)
		diffAngle += 360
	while (diffAngle > 180)
		diffAngle -= 360
	diffAngle


degreesToRadians = (degrees) ->
	degrees = degreesInRange degrees

	(degrees / 360) * 2*Math.PI


radiansToDegrees = (radians) ->
	result = (radians / (2*Math.PI)) * 360
	degreesInRange result


cartesianToPolar = (coords) ->
	{
		angle: radiansToDegrees(Math.atan2(coords.y, coords.x)),
		length: Math.sqrt(Math.pow(coords.x, 2) + Math.pow(coords.y, 2))
	}


polarToCartesian = (coords) ->
	angle = degreesToRadians(coords.angle)
	{
		x: coords.length * Math.cos(angle),
		y: coords.length * Math.sin(angle)
	}


randBetween = (min, max) ->
	Math.floor(Math.random() * (max - min + 1)) + min


sign = (x) ->
	if (x > 0)
		1
	else if (x < 0)
		-1
	else
		0


currentTime = () ->
	now = new Date()
	now.getTime()


@Tools ?= {}
_.merge(@Tools, {
	createButton
	addBorder
	addTooltip
	boundingBoxPositionsFor
	boundingBoxFits
	constrainedPosUpdate
	makeHoverable
	rectCollision
	constrainBetween
	degreesInRange
	angleDifference
	degreesToRadians
	radiansToDegrees
	cartesianToPolar
	polarToCartesian
	randBetween
	sign
	currentTime
})