_ = lodash

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


###
	anchor.on('mousedown touchstart', ->
		group.setDraggable(false)
	)
	anchor.on('dragend', ->
		group.setDraggable(true)
	)
###


class InteractiveShape
	getContainer: ->
		{
			x: @layer.getAbsolutePosition().x,
			y: @layer.getAbsolutePosition().y,
			width: @layer.width(),
			height: @layer.height()
		}

	addTooltip: (name) ->
		Widgets.addTooltip @commonShape.shape, name


class SquareBoundedIS extends InteractiveShape
	constructor: (@commonShape, @layer) ->
		@anchorNames = ['topLeft', 'topRight', 'bottomLeft', 'bottomRight']
		@anchorMargin = {x: 20, y: 20}
		self = this

		@group = new Kinetic.Group({
			x: @layer.width()/2,
			y: @layer.height()/2,
			draggable: true
		})

		@group.dragBoundFunc((newPos) ->
			self.mainDragBound newPos
		)

		#@commonShape.shape.name('figure')
		@group.add(@commonShape.shape)

		_.forEach(@anchorNames, (name) -> self.addAnchor name)

		this.updateAllAnchors()

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
			self.anchorDragBound this.getAbsolutePosition(), newPos
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

	anchorDragBound: (oldPos, newPos) ->
		center = {
			x: @group.getAbsolutePosition().x,
			y: @group.getAbsolutePosition().y
		}
		diff = {
			x: Math.abs(newPos.x - center.x) - Math.abs(oldPos.x - center.x),
			y: Math.abs(newPos.y - center.y) - Math.abs(oldPos.y - center.y)
		}
		shape = {
			x: @group.getAbsolutePosition().x,
			y: @group.getAbsolutePosition().y,
			width: @commonShape.width() + diff.x + @anchorMargin.x
			height: @commonShape.height() + diff.y + @anchorMargin.y
		}
		container = this.getContainer()

		fits = Widgets.boundingBoxFits shape, container
		if fits.all
			@commonShape.setSize {
				width: @commonShape.width() + diff.x,
				height: @commonShape.height() + diff.y
			}
			newPos
		else
			oldPos

	fixState: ->
		shape = @commonShape.shape
		shape.remove()
		@group.remove()
		shape.setPosition(@group.getPosition())
		@layer.add shape
		@layer.draw()

		shape

	setColor: (color) ->
		@commonShape.setColor color


degreesToRadians = (degrees) ->
	(degrees / 360) * 2*Math.PI


radiansToDegrees = (radians) ->
	(radians / (2*Math.PI)) * 360


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
		diffAngle = newPolar.angle - oldPolar.angle


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
		@shape.remove()
		@group.remove()
		@shape.setPosition(@group.getPosition())
		@layer.add @shape
		@layer.draw()

		@shape

	setColor: (color) ->
		@shape.fill color
		# XXX: for tooltip, which takes color from "stroke"
		@shape.stroke color


@Widgets ?= {}
_.merge(@Widgets, {
	Circle
	Rect
	SquareBoundedIS
	RadialSectorIS
})