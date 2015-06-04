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


class InteractiveShape
	#


class SquareBoundedIS extends InteractiveShape
	constructor: (@commonShape, @item, @panel) ->
		@layer = @panel.layer
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
			x: @layer.width()/2 + Tools.randBetween(-posMax.x, posMax.x),
			y: @layer.height()/2 + Tools.randBetween(-posMax.y, posMax.y),
			draggable: true
		})
		@group.on('dragmove', ->
			time = Tools.currentTime()
			self.panel.dragItem(self.item, {position: self.group.getPosition(), time: time})
		)
		@group.dragBoundFunc((newPos) ->
			self.mainDragBound newPos
		)

		#@commonShape.shape.name('figure')
		@group.add(@commonShape.shape)

		_.forEach(@anchorNames, (name) -> self.addAnchor name)

		this.updateAllAnchors()

		@addTooltip(@item.description)
		@panel.layer.add @group

	addTooltip: (name) ->
		Tools.addTooltip @commonShape.shape, name

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
		newPositions = Tools.boundingBoxPositionsFor shape

		_.forEach(@anchorNames, (name) ->
			pos = newPositions[name]
			anchor = self.group.find(".#{name}")[0].setPosition(pos)
		)

	addAnchor: (name) ->
		self = this
		anchor = Tools.createAnchor name
		
		anchor.dragBoundFunc((newPos) ->
			self.anchorDragBound this.getAbsolutePosition(), newPos, this.name()
		)
		anchor.on('dragmove', ->
			time = Tools.currentTime()
			self.panel.resizeItem(self.item, {size: self.commonShape.size(), time: time})
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
		Tools.constrainedPosUpdate shape, container, newPos

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
			x: Tools.sign((newPos.x - center.x) - (oldPos.x - center.x)),
			y: Tools.sign((newPos.y - center.y) - (oldPos.y - center.y))
		}
		shape = {
			x: @group.getAbsolutePosition().x + signedDiff.x/2,
			y: @group.getAbsolutePosition().y + signedDiff.y/2,
			width: @commonShape.width() + diff.x/2 + @anchorMargin.x
			height: @commonShape.height() + diff.y/2 + @anchorMargin.y
		}
		container = this.getContainer()

		fits = Tools.boundingBoxFits shape, container

		oldShape = shape = {
			x: @group.getAbsolutePosition().x,
			y: @group.getAbsolutePosition().y,
			width: @commonShape.width() + @anchorMargin.x,
			height: @commonShape.height() + @anchorMargin.y
		}
		oldBBox = Tools.boundingBoxPositionsFor oldShape

		if fits.all
			oldSize = @commonShape.size()
			@commonShape.setSize {
				width: @commonShape.width() + diff.x/2,
				height: @commonShape.height() + diff.y/2
			}
			newSize = @commonShape.size()

			newBBox = Tools.boundingBoxPositionsFor {
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

	select: ->
		@selectState(true)

	unselect: ->
		self = this
		@selectState(false)
		@group.on('dragstart.select click.select tap.select', ->
			self.panel.selectItem self.item
			self.group.off('.select')
		)

	selectState: (state) ->
		self = this
		_.forEach(@anchorNames, (name) ->
			anchor = self.group.find(".#{name}")[0]
			anchor.visible(state)
		)

	results: ->
		data = {
			position: @group.getPosition(),
		}
		_.merge(data, @commonShape.getData())
		data

	setColor: (color) ->
		@commonShape.setColor color


class RadialSectorIS extends InteractiveShape
	constructor: (@shape, @item, @panel, @length) ->
		@layer = @panel.layer
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

		@addTooltip(@item.description)
		@panel.layer.add @group

	addTooltip: (name) ->
		self = this

		positionFunc = (widget, shape) ->
			vector = {
				angle: shape.rotation() + shape.angle()/2,
				length: self.length * 1.25
			}
			offset = Tools.polarToCartesian(vector)
			{
				x: shape.x() + offset.x,
				y: shape.y() + offset.y
			}

		Tools.addTooltip @shape, name, positionFunc

	addAnchor: (name, dragBoundFunc) ->
		self = this
		anchor = Tools.createAnchor name
		
		anchor.dragBoundFunc((newPos) ->
			self[dragBoundFunc] this.getAbsolutePosition(), newPos, this
		)
		anchor.on('dragmove', ->
			time = Tools.currentTime()
			if (name == "rotation")
				self.panel.dragItem(self.item, {rotation: self.shape.rotation(), time: time})
			else
				self.panel.resizeItem(self.item, {angle: self.shape.angle(), time: time})
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
		newPolar = Tools.cartesianToPolar(newVector)
		oldPolar = Tools.cartesianToPolar(oldVector)
		diffAngle = Tools.angleDifference oldPolar.angle, newPolar.angle

		if (obj.name() == "angleOne")
			otherAngle = @shape.rotation() + @shape.angle()
		else
			otherAngle = @shape.rotation()

		da = Tools.angleDifference(oldPolar.angle, otherAngle)
		db = Tools.angleDifference(newPolar.angle, otherAngle)

		if (Math.abs(da) < 90 && da * db < 0)
			return oldPos
		if (Math.abs(db) < 5)
			return oldPos

		if (obj.name() == "angleOne")
			@shape.rotation(newPolar.angle)
			@shape.angle(@shape.angle() - diffAngle)
		else
			@shape.angle(@shape.angle() + diffAngle)

		tmp = Tools.polarToCartesian({angle: newPolar.angle, length: @anchorAngleDist})
		{x: tmp.x + center.x, y: tmp.y + center.y}

	anchorRotateDragBound: (oldPos, newPos, obj) ->
		center = @group.getAbsolutePosition()
		vector = {
			x: newPos.x - center.x,
			y: newPos.y - center.y
		}
		polar = Tools.cartesianToPolar(vector)
		@shape.rotation(polar.angle - @shape.angle()/2)
		tmp = Tools.polarToCartesian({angle: polar.angle, length: @anchorRotateDist})
		{x: tmp.x + center.x, y: tmp.y + center.y}

	updateAllAnchors: ->
		pos = {
			angle: @shape.rotation() + @shape.angle()/2,
			length: @anchorRotateDist
		}
		@anchors['rotation'].setPosition(Tools.polarToCartesian(pos))

		pos = {
			angle: @shape.rotation(),
			length: @anchorAngleDist
		}
		@anchors['angleOne'].setPosition(Tools.polarToCartesian(pos))
		
		pos = {
			angle: @shape.rotation() + @shape.angle(),
			length: @anchorAngleDist
		}
		@anchors['angleTwo'].setPosition(Tools.polarToCartesian(pos))
		
		@layer.draw()

	select: ->
		@selectState(true)

	unselect: ->
		self = this
		@selectState(false)
		@group.on('dragstart.select click.select tap.select', ->
			self.panel.selectItem self.item
			self.group.off('.select')
		)

	selectState: (state) ->
		self = this
		_.forEach(['rotation', 'angleOne', 'angleTwo'], (name) ->
			anchor = self.group.find(".#{name}")[0]
			anchor.visible(state)
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


class LineInLayerIS extends InteractiveShape
	constructor: (@panel) ->
		@layer = @panel.layer
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

	addAnchor: (name, dragBoundFunc) ->
		self = this
		anchor = Tools.createAnchor name
		
		anchor.dragBoundFunc((newPos) ->
			self.anchorDragBound this.getAbsolutePosition(), newPos, this
		)
		anchor.on('dragmove', ->
			time = Tools.currentTime()
			self.updateAllAnchors()
			
			self.panel.changeLine({
				length: self.shape.points()[2] * 2,
				time: time,
				orientation: self.group.rotation()
			})
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
		newVector.x = Tools.constrainBetween(newVector.x, -@box.width()/2, @box.width()/2)
		newVector.y = Tools.constrainBetween(newVector.y, -@box.height()/2, @box.height()/2)
		newPolar = Tools.cartesianToPolar(newVector)
		#newPolar.length = Math.min(newPolar.length, @max_length)
		oldPolar = Tools.cartesianToPolar(oldVector)
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
		@anchors['one'].setPosition(Tools.polarToCartesian(pos))

		pos = {
			angle: 180,
			length: @shape.points()[2]
		}
		@anchors['two'].setPosition(Tools.polarToCartesian(pos))

		@layer.draw()

	freeze: ->
		@anchors['one'].visible(false)
		@anchors['two'].visible(false)
		@layer.draw()

	results: ->
		{
			length: @shape.points()[2] * 2,
			rotation: @group.rotation()
		}		


class EventInTimelineIS extends InteractiveShape
	constructor: (@item, @timeline, @panel) ->
		self = this
		@line = @timeline.line
		@group = new Kinetic.Group({
			draggable: true
		})
		@group.x(Tools.randBetween(-@line.shape.points()[2], @line.shape.points()[2]))
		@group.on('dragmove', ->
			time = Tools.currentTime()
			position = self.group.x() / self.line.shape.points()[2]
			self.panel.dragItem(self.item, {position: position, time: time})
		)
		@bar = new Kinetic.Rect({
			x: 0, y: -15,
			width: 5,
			height: 30,
			fill: 'red'
		})
		rightSide = (Math.random() < 0.5)
		text = new Kinetic.Text({
			text: @item.description,
			fontSize: 15,
			fontFamily: 'Calibri',
			fill: '#555',
			width: 200,
			align: if (rightSide) then 'left' else 'right'
		})

		transform = text.getTransform()
		rotation = Tools.degreesInRange @line.group.rotation()
		invert = if (rotation > 0 && rotation < 180) then -1 else 1
		transform.rotate(Tools.degreesToRadians(90*invert))
		if (rightSide)
			transform.translate(30, 0)
		else
			transform.translate(-30-text.width(), 0)
		transform.translate(0, -10)

		@group.add @bar
		@group.add text
		@group.dragBoundFunc((newPos) ->
			self.dragBoundFunc this.getAbsolutePosition(), newPos, this
		)

		@line.group.add @group
		#@panel.layer.add @group
		@timeline.layer.draw()

	dragBoundFunc: (oldPos, newPos, obj) ->
		center = @line.group.getAbsolutePosition()
		vector = {
			x: newPos.x - center.x,
			y: newPos.y - center.y
		}
		polarVector = Tools.cartesianToPolar vector
		projection = Tools.polarToCartesian({
			angle: polarVector.angle - @line.group.rotation(),
			length: polarVector.length
		}).x

		dist = @line.shape.points()[2]
		projection = Tools.constrainBetween(projection, -dist, dist)

		@group.x(projection)
		#self.layer.draw()
		@group.getAbsolutePosition()

	select: ->
		@bar.fill('red')

	unselect: ->
		self = this
		@bar.fill('black')
		@group.on('dragstart.select click.select tap.select', ->
			self.panel.selectItem self.item
			self.group.off('.select')
		)

	results: ->
		{
			position: @group.x() / @line.shape.points()[2]
		}


@Widgets ?= {}
_.merge(@Widgets, {
	Circle
	Rect
	FilledRect
	SquareBoundedIS
	RadialSectorIS
	LineInLayerIS
	EventInTimelineIS
})