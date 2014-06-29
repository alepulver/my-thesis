_ = lodash

class Shape
	width: ->
		this.size().width

	height: ->
		this.size().height


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
		#desired = Math.sqrt(Math.pow(size.width/2, 2) + Math.pow(size.height/2, 2))
		desired = _.min([size.width/2, size.height/2])
		radius = _.max([desired, 3])
		@shape.radius(radius)

	setColor: (color) ->
		@shape.setStroke color


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
new Kinetic.Wedge({
			x: 0, y: 0,
			radius: 100, angle: 60,
			fill: 'red', stroke: 'black', strokeWidth: 4,
			rotation: 0,
			fillAlpha: 0.4
		})
###

###
	anchor.on('mousedown touchstart', ->
		group.setDraggable(false)
	)
	anchor.on('dragend', ->
		group.setDraggable(true)
	)
###


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


class InteractiveShape
	#

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

		@commonShape.shape.name('figure')
		@group.add(@commonShape.shape)

		_.forEach(@anchorNames, (name) -> self.addAnchor name)

		this.updateAllAnchors()

	addTooltip: (name) ->
		Widgets.addTooltip @commonShape.shape, name

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
		container = {
			x: @layer.getAbsolutePosition().x,
			y: @layer.getAbsolutePosition().y,
			width: @layer.width(),
			height: @layer.height()
		}
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
		container = {
			x: @layer.getAbsolutePosition().x,
			y: @layer.getAbsolutePosition().y,
			width: @layer.width(),
			height: @layer.height()
		}

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

@Widgets ?= {}
_.merge(@Widgets, {
	Circle: Circle
	Rect: Rect
	Line: Line
	SquareBoundedIS
})