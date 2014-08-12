_ = lodash

randBetween = (min, max) ->
	Math.floor(Math.random() * (max - min + 1)) + min


sign = (x) ->
	if (x > 0)
		1
	else if (x < 0)
		-1
	else
		0


class Shape
	width: ->
		this.size().width

	height: ->
		this.size().height


class Circle extends Shape
	constructor: ->
		@shape = new Kinetic.Circle({
			x: 0, y: 0,
			radius: 70,
			stroke: 'black', strokeWidth: 6,
			fill: 'transparent',
			name: 'image'
		})

	size: ->
		{
			width: @shape.radius()*2,
			height: @shape.radius()*2
		}

	setSize: (size) ->
		#desired = Math.sqrt(Math.pow(size.width/2, 2) + Math.pow(size.height/2, 2))
		desired = _.min([size.width/2, size.height/2])
		radius = _.max([desired, 3])
		@shape.radius(radius)

	setColor: (color) ->
		@shape.setStroke color

	getData: ->
		{
			radius: @shape.radius(),
			color: @shape.getStroke()
		}


class Rect extends Shape
	constructor: (rect) ->
		@shape = new Kinetic.Rect({
			x: 0, y: 0,
			width: 100, height: 100,
			offsetX: 50, offsetY: 50,
			stroke: 'black', strokeWidth: 6,
			fill: 'transparent',
			name: 'image'
		})

	size: ->
		@shape.size()


	setSize: (desiredSize) ->
		size = {
			width: _.max([desiredSize.width, 5]),
			height: _.max([desiredSize.height, 5])
		}
		@shape.size(size)
		@shape.offsetX(size.width/2)
		@shape.offsetY(size.height/2)

	setColor: (color) ->
		@shape.setStroke color

	getData: ->
		{
			size: @shape.size()
			color: @shape.getStroke()
		}


class FilledRect extends Shape
	constructor: (rect) ->
		@shape = new Kinetic.Rect({
			x: 0, y: 0,
			width: 50, height: 100,
			offsetX: 25, offsetY: 50,
			strokeWidth: 0, stroke: 'black',
			fill: 'black',
			name: 'image'
		})

	size: ->
		@shape.size()


	setSize: (desiredSize) ->
		size = {
			width: 50,
			height: _.max([desiredSize.height, 10])
		}
		@shape.size(size)
		@shape.offsetX(size.width/2)
		@shape.offsetY(size.height/2)

	setColor: (color) ->
		# XXX: for addTooltip
		@shape.stroke color

		@shape.fill color

	getData: ->
		{
			size: @shape.size()
			color: @shape.fill()
		}


###
	anchor.on('mousedown touchstart', ->
		group.setDraggable(false)
	)
	anchor.on('dragend', ->
		group.setDraggable(true)
	)
###


class InteractiveShape
	#

class SquareBoundedIS extends InteractiveShape
	constructor: (@commonShape, @layer) ->
		@anchorNames = ['topLeft', 'topRight', 'bottomLeft', 'bottomRight']
		@anchorOpposites = {
			'topLeft': 'bottomRight',
			'topRight': 'bottomLeft',
			'bottomLeft': 'topRight',
			'bottomRight': 'topLeft'
		}
		@anchorMargin = {x: 20, y: 20}
		self = this

		posMax = {
			x: (@layer.width() - @commonShape.size().width - 20)/2,
			y: (@layer.height() - @commonShape.size().height - 20)/2,
		}

		@group = new Kinetic.Group({
			x: @layer.width()/2 + randBetween(-posMax.x, posMax.x),
			y: @layer.height()/2 + randBetween(-posMax.y, posMax.y),
			draggable: true
		})

		@group.dragBoundFunc((newPos) ->
			self.mainDragBound newPos
		)

		#@commonShape.shape.name('figure')
		@group.add(@commonShape.shape)

		_.forEach(@anchorNames, (name) -> self.addAnchor name)

		this.updateAllAnchors()

	addTooltip: (name) ->
		Widgets.addTooltip @commonShape.shape, name

	getContainer: ->
		{
			x: @layer.getAbsolutePosition().x,
			y: @layer.getAbsolutePosition().y,
			width: @layer.width(),
			height: @layer.height()
		}

	updateAllAnchors: ->
		self = this
		shape = {
			x: 0,
			y: 0,
			width: @commonShape.width() + @anchorMargin.x,
			height: @commonShape.height() + @anchorMargin.y
		}			
		newPositions = Widgets.boundingBoxPositionsFor shape

		_.forEach(@anchorNames, (name) ->
			pos = newPositions[name]
			anchor = self.group.find(".#{name}")[0].setPosition(pos)
		)

	addAnchor: (name) ->
		self = this
		anchor = new Kinetic.Circle({
			stroke: '#666',
			fill: '#ddd',
			strokeWidth: 2,
			radius: 8,
			name: name,
			draggable: true
		})
		Widgets.makeHoverable anchor, anchor
		
		anchor.dragBoundFunc((newPos) ->
			self.anchorDragBound this.getAbsolutePosition(), newPos, this.name()
		)
		anchor.on('dragmove', ->
			self.updateAllAnchors()
			self.layer.draw()
		)
		@group.add anchor

	mainDragBound: (newPos) ->
		shape = {
			x: @group.getAbsolutePosition().x,
			y: @group.getAbsolutePosition().y,
			width: @commonShape.width() + @anchorMargin.x,
			height: @commonShape.height() + @anchorMargin.y
		}
		container = this.getContainer()
		Widgets.constrainedPosUpdate shape, container, newPos

	anchorDragBound: (oldPos, newPos, name) ->
		self = this
		center = {
			x: @group.getAbsolutePosition().x,
			y: @group.getAbsolutePosition().y
		}
		diff = {
			x: Math.abs(newPos.x - center.x) - Math.abs(oldPos.x - center.x),
			y: Math.abs(newPos.y - center.y) - Math.abs(oldPos.y - center.y)
		}
		signedDiff = {
			x: sign((newPos.x - center.x) - (oldPos.x - center.x)),
			y: sign((newPos.y - center.y) - (oldPos.y - center.y))
		}
		shape = {
			x: @group.getAbsolutePosition().x + signedDiff.x/2,
			y: @group.getAbsolutePosition().y + signedDiff.y/2,
			width: @commonShape.width() + diff.x/2 + @anchorMargin.x
			height: @commonShape.height() + diff.y/2 + @anchorMargin.y
		}
		container = this.getContainer()

		fits = Widgets.boundingBoxFits shape, container

		oldShape = shape = {
			x: @group.getAbsolutePosition().x,
			y: @group.getAbsolutePosition().y,
			width: @commonShape.width() + @anchorMargin.x,
			height: @commonShape.height() + @anchorMargin.y
		}
		oldBBox = Widgets.boundingBoxPositionsFor oldShape

		if fits.all
			oldSize = @commonShape.size()
			@commonShape.setSize {
				width: @commonShape.width() + diff.x/2,
				height: @commonShape.height() + diff.y/2
			}
			newSize = @commonShape.size()

			newBBox = Widgets.boundingBoxPositionsFor {
				x: @group.getAbsolutePosition().x,
				y: @group.getAbsolutePosition().y,
				width: newSize.width + @anchorMargin.x
				height: newSize.height + @anchorMargin.y
			}
			oppositeCorner = self.anchorOpposites[name]
			diffPos = {
				x: oldBBox[oppositeCorner].x - newBBox[oppositeCorner].x,
				y: oldBBox[oppositeCorner].y - newBBox[oppositeCorner].y
			}

			###
			diffSize = {
				x: signedDiff.x * Math.abs(newSize.width - oldSize.width)/2,
				y: signedDiff.y * Math.abs(newSize.height - oldSize.height)/2
			}
			###
			self.group.move(diffPos)
			newPos
		else
			oldPos

	fixState: ->
		self = this

		###
		shape = @commonShape.shape
		shape.remove()
		@group.remove()
		shape.setPosition(@group.getPosition())
		#shape.draggable(true)
		@layer.add shape
		@layer.draw()
		###

		self = this
		_.forEach(@anchorNames, (name) ->
			anchor = self.group.find(".#{name}")[0]
			anchor.visible(false)
		)

		this

	unselect: ->
		self = this
		_.forEach(@anchorNames, (name) ->
			anchor = self.group.find(".#{name}")[0]
			anchor.visible(false)
		)
		@group.draggable(false)

	results: ->
		data = {
			position: @group.getPosition(),
		}
		_.merge(data, @commonShape.getData())
		data

	setColor: (color) ->
		@commonShape.setColor color


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


class RadialSectorIS extends InteractiveShape
	constructor: (@shape, @layer, @length) ->
		@anchors = {}
		@anchorAngleDist = @length * 0.8
		@anchorRotateDist = @length * 0.5
		self = this

		@group = new Kinetic.Group({
			x: @layer.width()/2,
			y: @layer.height()/2,
		})

		#@commonShape.shape.name('figure')
		@group.add(@shape)

		this.addAnchor 'rotation', 'anchorRotateDragBound'
		this.addAnchor 'angleOne', 'anchorAngleDragBound'
		this.addAnchor 'angleTwo', 'anchorAngleDragBound'

		this.updateAllAnchors()

	addTooltip: (name) ->
		self = this

		positionFunc = (widget, shape) ->
			vector = {
				angle: shape.rotation() + shape.angle()/2,
				length: self.length * 1.25
			}
			offset = polarToCartesian(vector)
			{
				x: shape.x() + offset.x,
				y: shape.y() + offset.y
			}

		Widgets.addTooltip @shape, name, positionFunc

	addAnchor: (name, dragBoundFunc) ->
		self = this
		anchor = new Kinetic.Circle({
			stroke: '#666',
			fill: '#ddd',
			strokeWidth: 2,
			radius: 8,
			name: name,
			draggable: true
		})
		Widgets.makeHoverable anchor, anchor
		
		anchor.dragBoundFunc((newPos) ->
			self[dragBoundFunc] this.getAbsolutePosition(), newPos, this
		)
		anchor.on('dragmove', ->
			self.updateAllAnchors()
		)
		@anchors[name] = anchor
		@group.add anchor

	anchorAngleDragBound: (oldPos, newPos, obj) ->
		center = @group.getAbsolutePosition()
		newVector = {
			x: newPos.x - center.x,
			y: newPos.y - center.y
		}
		oldVector = {
			x: oldPos.x - center.x,
			y: oldPos.y - center.y
		}
		newPolar = cartesianToPolar(newVector)
		oldPolar = cartesianToPolar(oldVector)
		diffAngle = angleDifference oldPolar.angle, newPolar.angle

		if (obj.name() == "angleOne")
			otherAngle = @shape.rotation() + @shape.angle()
		else
			otherAngle = @shape.rotation()

		da = angleDifference(oldPolar.angle, otherAngle)
		db = angleDifference(newPolar.angle, otherAngle)

		if (Math.abs(da) < 90 && da * db < 0)
			return oldPos
		if (Math.abs(db) < 5)
			return oldPos

		if (obj.name() == "angleOne")
			@shape.rotation(newPolar.angle)
			@shape.angle(@shape.angle() - diffAngle)
		else
			@shape.angle(@shape.angle() + diffAngle)

		tmp = polarToCartesian({angle: newPolar.angle, length: @anchorAngleDist})
		{x: tmp.x + center.x, y: tmp.y + center.y}

	anchorRotateDragBound: (oldPos, newPos, obj) ->
		center = @group.getAbsolutePosition()
		vector = {
			x: newPos.x - center.x,
			y: newPos.y - center.y
		}
		polar = cartesianToPolar(vector)
		@shape.rotation(polar.angle - @shape.angle()/2)
		tmp = polarToCartesian({angle: polar.angle, length: @anchorRotateDist})
		{x: tmp.x + center.x, y: tmp.y + center.y}

	updateAllAnchors: ->
		pos = {
			angle: @shape.rotation() + @shape.angle()/2,
			length: @anchorRotateDist
		}
		@anchors['rotation'].setPosition(polarToCartesian(pos))

		pos = {
			angle: @shape.rotation(),
			length: @anchorAngleDist
		}
		@anchors['angleOne'].setPosition(polarToCartesian(pos))
		
		pos = {
			angle: @shape.rotation() + @shape.angle(),
			length: @anchorAngleDist
		}
		@anchors['angleTwo'].setPosition(polarToCartesian(pos))
		
		@layer.draw()

	fixState: ->
		self = this
		#@shape.remove()
		#@group.remove()
		#@shape.setPosition(@group.getPosition())
		#@layer.add @shape
		#@layer.draw()
		
		_.forEach(["angleOne", "angleTwo"], (name) ->
			anchor = self.group.find(".#{name}")[0]
			anchor.visible(false)
		)

		this

	unselect: ->
		self = this
		_.forEach(@anchorNames, (name) ->
			anchor = self.group.find(".#{name}")[0]
			anchor.visible(false)
		)

	results: ->
		{
			rotation: @shape.rotation(),
			angle: @shape.angle(),
			color: @shape.stroke()
		}

	setColor: (color) ->
		@shape.fill color
		# XXX: for tooltip, which takes color from "stroke"
		@shape.stroke color


constrainBetween = (x, min, max) ->
	if (x < min)
		min
	else if (x > max)
		max
	else
		x


class LineInLayerIS extends InteractiveShape
	constructor: (@layer) ->
		@anchors = {}
		self = this

		@group = new Kinetic.Group({
			x: @layer.width()/2,
			y: @layer.height()/2
		})

		@shape = new Kinetic.Line({
			points: [-100, 0, 100, 0]
			stroke: 'black',
			strokeWidth: 2,
		})
		@group.add(@shape)

		@box = new Kinetic.Rect({
			x: @layer.width()/2,
			y: @layer.height()/2,
			width: @layer.width() * 0.7,
			height: @layer.height() * 0.7,
			stroke: 'black', strokeWidth: 2
		})
		@box.offsetX(@box.width()/2)
		@box.offsetY(@box.height()/2)

		this.addAnchor 'one'
		this.addAnchor 'two'

		this.updateAllAnchors()

	addTooltip: (name) ->
		Widgets.addTooltip @shape, name

	addAnchor: (name, dragBoundFunc) ->
		self = this
		anchor = new Kinetic.Circle({
			stroke: '#666',
			fill: '#ddd',
			strokeWidth: 2,
			radius: 8,
			name: name,
			draggable: true
		})
		Widgets.makeHoverable anchor, anchor
		
		anchor.dragBoundFunc((newPos) ->
			self.anchorDragBound this.getAbsolutePosition(), newPos, this
		)
		anchor.on('dragmove', ->
			self.updateAllAnchors()
		)
		@anchors[name] = anchor
		@group.add anchor

	anchorDragBound: (oldPos, newPos, obj) ->
		center = @group.getAbsolutePosition()
		newVector = {
			x: newPos.x - center.x,
			y: newPos.y - center.y
		}
		oldVector = {
			x: oldPos.x - center.x,
			y: oldPos.y - center.y
		}
		newVector.x = constrainBetween(newVector.x, -@box.width()/2, @box.width()/2)
		newVector.y = constrainBetween(newVector.y, -@box.height()/2, @box.height()/2)
		newPolar = cartesianToPolar(newVector)
		#newPolar.length = Math.min(newPolar.length, @max_length)
		oldPolar = cartesianToPolar(oldVector)
		diffAngle = newPolar.angle - oldPolar.angle

		length = Math.max(newPolar.length, 100)
		@group.rotate(diffAngle)
		@shape.points([-length, 0, length, 0])

		newPos

	updateAllAnchors: ->
		pos = {
			angle: 0,
			length: @shape.points()[2]
		}
		@anchors['one'].setPosition(polarToCartesian(pos))

		pos = {
			angle: 180,
			length: @shape.points()[2]
		}
		@anchors['two'].setPosition(polarToCartesian(pos))

		@layer.draw()

	fixState: ->
		@anchors['one'].remove()
		@anchors['two'].remove()
		@layer.draw()

		{
			length: @shape.points()[2] * 2,
			rotation: @group.rotation()
		}


@Widgets ?= {}
_.merge(@Widgets, {
	Circle
	Rect
	FilledRect
	SquareBoundedIS
	RadialSectorIS
	LineInLayerIS
	cartesianToPolar
	polarToCartesian
	degreesToRadians
	radiansToDegrees
	degreesInRange
	constrainBetween
})